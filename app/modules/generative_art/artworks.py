import base64
import random
from dataclasses import dataclass
from io import BytesIO

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


SHAPE_CLASSES = [Circle, Square, Triangle, Line]


def generate_artwork(shape_count=60, max_size=48, palette_name="aurora", width=1000, height=650):
    shape_count = max(10, min(int(shape_count), 180))
    max_size = max(12, min(int(max_size), 110))
    palette = PALETTES.get(palette_name, PALETTES["aurora"])

    background_rgb = blend_with_white(hex_to_rgb(random.choice(palette)), 0.82)
    image = Image.new("RGB", (width, height), background_rgb)
    draw_context = ImageDraw.Draw(image, "RGBA")

    # Layer soft translucent bands first, then place OOP shapes above them.
    for _ in range(14):
        color = hex_to_rgb(random.choice(palette)) + (45,)
        y = random.randint(0, height)
        draw_context.line(
            [(0, y), (width, y + random.randint(-130, 130))],
            fill=color,
            width=random.randint(12, 36),
        )

    for _ in range(shape_count):
        shape_class = random.choice(SHAPE_CLASSES)
        color = hex_to_rgb(random.choice(palette)) + (random.randint(120, 230),)
        shape = shape_class(
            x=random.randint(0, width),
            y=random.randint(0, height),
            size=random.randint(12, max_size),
            color=color,
        )
        shape.draw(draw_context)

    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("ascii")
