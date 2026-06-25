import base64
import math
import random
from dataclasses import dataclass
from io import BytesIO

import numpy as np
from PIL import Image, ImageDraw


PALETTES = {
    "aurora": ["#3dd6d0", "#8a5cf6", "#f7d060", "#ff7aa2", "#1f7a8c"],
    "sunset": ["#f72585", "#ff7a00", "#ffd166", "#8338ec", "#3a86ff"],
    "forest": ["#2d6a4f", "#40916c", "#95d5b2", "#d8f3dc", "#1b4332"],
    "mono": ["#111827", "#374151", "#6b7280", "#d1d5db", "#f9fafb"],
}


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


def blend_with_white(rgb, factor):
    return tuple(int(channel + (255 - channel) * factor) for channel in rgb)


def interpolate_color(start, end, factor):
    return tuple(int(start[i] + (end[i] - start[i]) * factor) for i in range(3))


def add_alpha(rgb, alpha):
    return rgb + (max(0, min(255, int(alpha))),)


def regular_polygon_points(cx, cy, radius, sides, rotation=0):
    return [
        (
            cx + math.cos(rotation + math.tau * index / sides) * radius,
            cy + math.sin(rotation + math.tau * index / sides) * radius,
        )
        for index in range(sides)
    ]


def build_dark_background(width, height, background_hex, glow_colors):
    base = np.array(hex_to_rgb(background_hex), dtype=np.float32)
    y, x = np.mgrid[0:height, 0:width]
    image_array = np.zeros((height, width, 3), dtype=np.float32)
    image_array[:, :] = base

    for color_hex, center_x, center_y, strength, radius in glow_colors:
        glow = np.array(hex_to_rgb(color_hex), dtype=np.float32)
        distance = ((x - center_x * width) ** 2 + (y - center_y * height) ** 2) ** 0.5
        mask = np.clip(1 - distance / (radius * max(width, height)), 0, 1) ** 2
        image_array += (glow - base) * mask[..., None] * strength

    vignette_distance = ((x - width / 2) ** 2 + (y - height / 2) ** 2) ** 0.5
    vignette = np.clip(vignette_distance / (0.76 * max(width, height)), 0, 1)
    image_array *= (1 - vignette[..., None] * 0.42)
    return Image.fromarray(np.clip(image_array, 0, 255).astype(np.uint8), "RGB")


@dataclass
class Shape:
    x: int
    y: int
    size: int
    color: str

    def draw(self, draw_context):
        raise NotImplementedError


class Circle(Shape):
    def draw(self, draw_context):
        radius = self.size // 2
        draw_context.ellipse(
            [self.x - radius, self.y - radius, self.x + radius, self.y + radius],
            fill=self.color,
            outline=None,
        )


class Square(Shape):
    def draw(self, draw_context):
        half = self.size // 2
        draw_context.rectangle(
            [self.x - half, self.y - half, self.x + half, self.y + half],
            fill=self.color,
        )


class Triangle(Shape):
    def draw(self, draw_context):
        half = self.size // 2
        points = [
            (self.x, self.y - half),
            (self.x + half, self.y + half),
            (self.x - half, self.y + half),
        ]
        draw_context.polygon(points, fill=self.color)


class Line(Shape):
    def draw(self, draw_context):
        half = self.size
        draw_context.line(
            [self.x - half, self.y - half, self.x + half, self.y + half],
            fill=self.color,
            width=max(2, self.size // 10),
        )


class RadialBurst(Shape):
    def __init__(self, x, y, size, color, palette, ray_count, length_range, angle_offset=0):
        super().__init__(x, y, size, color)
        self.palette = palette
        self.ray_count = ray_count
        self.length_range = length_range
        self.angle_offset = angle_offset

    def draw(self, draw_context):
        for index in range(self.ray_count):
            angle = self.angle_offset + math.tau * index / self.ray_count
            angle += random.uniform(-0.035, 0.035)
            length = random.uniform(*self.length_range)
            start_radius = random.uniform(self.size * 0.12, self.size * 0.55)
            width = random.uniform(2.5, max(5, self.size * 0.22))
            color = hex_to_rgb(random.choice(self.palette))
            alpha = random.randint(38, 112)

            base_x = self.x + math.cos(angle) * start_radius
            base_y = self.y + math.sin(angle) * start_radius
            tip_x = self.x + math.cos(angle) * length
            tip_y = self.y + math.sin(angle) * length
            side_angle = angle + math.pi / 2
            points = [
                (base_x + math.cos(side_angle) * width, base_y + math.sin(side_angle) * width),
                (base_x - math.cos(side_angle) * width, base_y - math.sin(side_angle) * width),
                (tip_x, tip_y),
            ]
            draw_context.polygon(points, fill=add_alpha(color, alpha))

            if index % 3 == 0:
                draw_context.line(
                    [(self.x, self.y), (tip_x, tip_y)],
                    fill=add_alpha(color, alpha * 0.65),
                    width=max(1, int(width / 3)),
                )


class FlowStroke(Shape):
    def __init__(self, x, y, size, color, angle, curvature=0.65, width=1):
        super().__init__(x, y, size, color)
        self.angle = angle
        self.curvature = curvature
        self.width = width

    def draw(self, draw_context):
        points = []
        steps = 9
        half = self.size / 2
        for index in range(steps):
            progress = index / (steps - 1)
            distance = (progress - 0.5) * self.size
            bend = math.sin(progress * math.pi) * self.curvature * self.size * 0.28
            px = self.x + math.cos(self.angle) * distance + math.cos(self.angle + math.pi / 2) * bend
            py = self.y + math.sin(self.angle) * distance + math.sin(self.angle + math.pi / 2) * bend
            px += math.cos(self.angle + math.pi / 2) * random.uniform(-half * 0.04, half * 0.04)
            py += math.sin(self.angle + math.pi / 2) * random.uniform(-half * 0.04, half * 0.04)
            points.append((px, py))

        draw_context.line(points, fill=self.color, width=self.width, joint="curve")


class MandalaRing(Shape):
    def __init__(self, x, y, size, color, palette, radius, sides, count, rotation=0):
        super().__init__(x, y, size, color)
        self.palette = palette
        self.radius = radius
        self.sides = sides
        self.count = count
        self.rotation = rotation

    def draw(self, draw_context):
        for index in range(self.count):
            angle = self.rotation + math.tau * index / self.count
            cx = self.x + math.cos(angle) * self.radius
            cy = self.y + math.sin(angle) * self.radius
            color = hex_to_rgb(self.palette[index % len(self.palette)])
            outer_rotation = angle + math.pi / 2
            points = regular_polygon_points(cx, cy, self.size, self.sides, outer_rotation)
            draw_context.polygon(points, fill=add_alpha(color, 74), outline=add_alpha(color, 170))

            inner_points = regular_polygon_points(cx, cy, self.size * 0.52, self.sides, outer_rotation + 0.18)
            draw_context.polygon(inner_points, fill=add_alpha(color, 42))


class OrganicBlob(Shape):
    def __init__(self, x, y, size, color, harmonics, phase, points=96):
        super().__init__(x, y, size, color)
        self.harmonics = harmonics
        self.phase = phase
        self.points = points

    def draw(self, draw_context):
        polygon = []
        for theta in np.linspace(0, math.tau, self.points, endpoint=False):
            radius = self.size
            for harmonic, amplitude, phase_shift in self.harmonics:
                radius += math.sin(harmonic * theta + self.phase + phase_shift) * amplitude
            polygon.append((
                self.x + math.cos(theta) * radius,
                self.y + math.sin(theta) * radius,
            ))
        draw_context.polygon(polygon, fill=self.color)


SHAPE_CLASSES = [Circle, Square, Triangle, Line]


def draw_flow_field(draw_context, width, height, palette, shape_count, max_size, alpha_range):
    scale = random.uniform(92, 150)
    step = max(18, int(58 - shape_count * 0.22))
    length = max(26, max_size * random.uniform(1.1, 1.9))

    for y in range(-step, height + step, step):
        for x in range(-step, width + step, step):
            jitter_x = x + random.uniform(-step * 0.35, step * 0.35)
            jitter_y = y + random.uniform(-step * 0.35, step * 0.35)
            angle = math.sin(jitter_x / scale) * math.cos(jitter_y / (scale * 0.86)) * math.pi
            angle += math.sin((jitter_x + jitter_y) / (scale * 1.7)) * 0.85
            palette_index = int((jitter_x / max(1, width)) * (len(palette) - 1))
            color = hex_to_rgb(palette[max(0, min(len(palette) - 1, palette_index))])
            alpha = random.randint(*alpha_range)
            stroke = FlowStroke(
                x=jitter_x,
                y=jitter_y,
                size=length * random.uniform(0.72, 1.28),
                color=add_alpha(color, alpha),
                angle=angle,
                curvature=random.uniform(-1.0, 1.0),
                width=random.choice([1, 1, 2]),
            )
            stroke.draw(draw_context)


def draw_blob_field(draw_context, width, height, palette, count, max_size, alpha_range):
    for _ in range(count):
        base_size = random.uniform(max_size * 0.55, max_size * 2.4)
        harmonics = [
            (harmonic, random.uniform(base_size * 0.03, base_size * 0.13), random.uniform(0, math.tau))
            for harmonic in range(3, random.randint(5, 8))
        ]
        blob = OrganicBlob(
            x=random.uniform(-max_size, width + max_size),
            y=random.uniform(-max_size, height + max_size),
            size=base_size,
            color=add_alpha(hex_to_rgb(random.choice(palette)), random.randint(*alpha_range)),
            harmonics=harmonics,
            phase=random.uniform(0, math.tau),
        )
        blob.draw(draw_context)


def draw_mandala(draw_context, width, height, palette, shape_count, max_size):
    center_x = width * random.uniform(0.45, 0.55)
    center_y = height * random.uniform(0.43, 0.57)
    ring_count = 4 + int((shape_count / 180) * 4)
    maximum_radius = min(width, height) * random.uniform(0.34, 0.47)

    for ring_index in range(ring_count):
        progress = (ring_index + 1) / ring_count
        radius = maximum_radius * progress
        sides = 3 + (ring_index % 6)
        count = max(8, int(10 + progress * 28 + shape_count * 0.06))
        shape_size = max(8, max_size * (1.1 - progress * 0.62))
        ring = MandalaRing(
            x=center_x,
            y=center_y,
            size=shape_size,
            color=palette[ring_index % len(palette)],
            palette=palette,
            radius=radius,
            sides=sides,
            count=count,
            rotation=random.uniform(0, math.tau),
        )
        ring.draw(draw_context)

    for radius in np.linspace(max_size * 0.8, maximum_radius * 1.08, ring_count + 3):
        color = hex_to_rgb(random.choice(palette))
        draw_context.ellipse(
            [center_x - radius, center_y - radius, center_x + radius, center_y + radius],
            outline=add_alpha(color, 44),
            width=1,
        )


def draw_sunset_burst(draw_context, width, height, palette, shape_count, max_size):
    focal_points = [
        (width * random.uniform(0.44, 0.58), height * random.uniform(0.50, 0.62)),
    ]
    for _ in range(1 + shape_count // 90):
        focal_points.append((
            width * random.uniform(0.24, 0.76),
            height * random.uniform(0.34, 0.70),
        ))

    for index, (x, y) in enumerate(focal_points):
        ray_count = min(60, max(24, shape_count // max(1, len(focal_points)) + random.randint(8, 20)))
        burst = RadialBurst(
            x=x,
            y=y,
            size=max_size * random.uniform(0.48, 0.95),
            color=random.choice(palette),
            palette=palette,
            ray_count=ray_count,
            length_range=(
                min(width, height) * random.uniform(0.20, 0.36),
                max(width, height) * random.uniform(0.58, 0.92),
            ),
            angle_offset=random.uniform(0, math.tau),
        )
        burst.draw(draw_context)

        core_color = hex_to_rgb(palette[index % len(palette)])
        for radius in np.linspace(max_size * 0.4, max_size * 3.2, 8):
            draw_context.ellipse(
                [x - radius, y - radius, x + radius, y + radius],
                fill=add_alpha(core_color, max(8, 95 - radius * 0.6)),
            )


def generate_artwork(shape_count=60, max_size=48, palette_name="aurora", width=1000, height=650):
    shape_count = max(10, min(int(shape_count), 180))
    max_size = max(12, min(int(max_size), 110))
    palette = PALETTES.get(palette_name, PALETTES["aurora"])
    background_map = {
        "aurora": "#070b14",
        "sunset": "#0d0510",
        "forest": "#050d07",
        "mono": "#050505",
    }
    background = background_map.get(palette_name, "#070b14")
    glow_colors = [
        (palette[0], 0.20, 0.24, 0.18, 0.52),
        (palette[min(1, len(palette) - 1)], 0.82, 0.30, 0.14, 0.46),
        (palette[-1], 0.52, 0.82, 0.12, 0.54),
    ]
    image = build_dark_background(width, height, background, glow_colors)
    draw_context = ImageDraw.Draw(image, "RGBA")

    if palette_name == "sunset":
        draw_blob_field(
            draw_context,
            width,
            height,
            [palette[0], palette[1], palette[2], palette[3]],
            count=max(8, shape_count // 5),
            max_size=max_size * 1.3,
            alpha_range=(18, 48),
        )
        draw_sunset_burst(draw_context, width, height, palette, shape_count, max_size)
    elif palette_name == "forest":
        draw_blob_field(
            draw_context,
            width,
            height,
            palette,
            count=max(15, min(42, shape_count // 3)),
            max_size=max_size,
            alpha_range=(34, 96),
        )
        draw_mandala(draw_context, width, height, palette, shape_count, max_size)
    elif palette_name == "mono":
        draw_flow_field(draw_context, width, height, palette[::-1], shape_count, max_size, (58, 168))
        for offset in range(0, height, max(32, max_size)):
            color = add_alpha(hex_to_rgb(random.choice(palette[2:])), 24)
            draw_context.arc(
                [width * 0.08, offset - height * 0.45, width * 0.92, offset + height * 0.55],
                start=190,
                end=350,
                fill=color,
                width=1,
            )
    else:
        draw_blob_field(
            draw_context,
            width,
            height,
            [palette[0], palette[1], palette[3], palette[4]],
            count=max(18, min(46, shape_count // 3 + 14)),
            max_size=max_size,
            alpha_range=(34, 104),
        )
        draw_flow_field(draw_context, width, height, [palette[0], palette[1], palette[3], palette[4]], shape_count, max_size, (48, 138))
        for _ in range(max(2, shape_count // 45)):
            burst = RadialBurst(
                x=random.uniform(width * 0.18, width * 0.82),
                y=random.uniform(height * 0.18, height * 0.82),
                size=max_size * 0.45,
                color=random.choice(palette),
                palette=[palette[0], palette[1], palette[3]],
                ray_count=random.randint(20, 34),
                length_range=(max_size * 1.2, max_size * 4.4),
                angle_offset=random.uniform(0, math.tau),
            )
            burst.draw(draw_context)

    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("ascii")
