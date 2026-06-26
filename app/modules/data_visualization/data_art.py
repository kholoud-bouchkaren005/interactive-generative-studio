import base64
import math
import random
from io import BytesIO

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image


ANIMATION_THEMES = {
    "aurora": {
        "colors": ["#3dd6d0", "#8a5cf6", "#ff7aa2", "#1f7a8c", "#c77dff"],
        "background": "#070b14",
        "cmap_sequence": ["cool", "winter", "plasma"],
    },
    "sunset": {
        "colors": ["#f72585", "#ff7a00", "#ffd166", "#8338ec", "#ef233c"],
        "background": "#0d0510",
        "cmap_sequence": ["inferno", "hot", "autumn"],
    },
    "forest": {
        "colors": ["#2d6a4f", "#40916c", "#95d5b2", "#d8f3dc", "#52b788"],
        "background": "#050d07",
        "cmap_sequence": ["YlGn", "summer", "BuGn"],
    },
    "cosmos": {
        "colors": ["#240046", "#7b2fff", "#e0aaff", "#ff6b6b", "#ffd166"],
        "background": "#03000a",
        "cmap_sequence": ["plasma", "magma", "twilight"],
    },
    "neon": {
        "colors": ["#00f5d4", "#00bbf9", "#fee440", "#f15bb5", "#9b5de5"],
        "background": "#020202",
        "cmap_sequence": ["cool", "spring", "hsv"],
    },
}


SYMMETRY_LABELS = {
    1: "None",
    2: "Bilateral",
    4: "Quad",
    6: "Hexagonal",
}


def _clamp(value, minimum, maximum, cast):
    return max(minimum, min(cast(value), maximum))


def _hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[index:index + 2], 16) / 255 for index in (0, 2, 4))


def _color_at(colors, position):
    position = position % len(colors)
    low = int(math.floor(position))
    high = (low + 1) % len(colors)
    mix = position - low
    start = np.array(_hex_to_rgb(colors[low]))
    end = np.array(_hex_to_rgb(colors[high]))
    return tuple(start + (end - start) * mix)


def _build_particles(particle_count, seed):
    rng = np.random.default_rng(seed)
    return pd.DataFrame(
        {
            "radius": rng.uniform(50, 250, particle_count),
            "speed": rng.uniform(0.3, 2.0, particle_count),
            "phase": rng.uniform(0, math.tau, particle_count),
            "size": rng.uniform(10, 80, particle_count),
            "color_offset": rng.uniform(0, 5, particle_count),
        }
    )


def _symmetry_points(x, y, center_x, center_y, symmetry):
    if symmetry == 2:
        return [(x, y), (2 * center_x - x, y)]
    if symmetry == 4:
        return [(x, y), (2 * center_x - x, y), (x, 2 * center_y - y), (2 * center_x - x, 2 * center_y - y)]
    if symmetry == 6:
        points = []
        dx = x - center_x
        dy = y - center_y
        for step in range(6):
            angle = step * math.tau / 6
            points.append((
                center_x + dx * math.cos(angle) - dy * math.sin(angle),
                center_y + dx * math.sin(angle) + dy * math.cos(angle),
            ))
        return points
    return [(x, y)]


def _render_frame(
    frame_index,
    total_frames,
    theme,
    duration,
    fps,
    wave_layers,
    particles,
    color_speed,
    morph_intensity,
    symmetry,
    beat_mode,
):
    width, height = 900, 500
    t = frame_index / fps
    colors = theme["colors"]
    background = theme["background"]

    fig, ax = plt.subplots(figsize=(9, 5), dpi=100)
    fig.patch.set_facecolor(background)
    ax.set_facecolor(background)
    ax.set_xlim(0, width)
    ax.set_ylim(height, 0)
    ax.axis("off")

    grid_x = np.linspace(0, width, 180)
    grid_y = np.linspace(0, height, 100)
    xx, yy = np.meshgrid(grid_x, grid_y)
    hue = np.sin(xx / width * math.pi + t * color_speed) * 0.5
    hue += np.cos(yy / height * math.pi + t * 0.7) * 0.5
    hue = (hue - hue.min()) / max(0.001, hue.max() - hue.min())
    cmap_name = theme["cmap_sequence"][int((t * color_speed) / 2) % len(theme["cmap_sequence"])]
    ax.imshow(hue, extent=[0, width, height, 0], cmap=cmap_name, alpha=0.4, interpolation="bilinear")

    x = np.linspace(0, width, 520)
    previous_wave = np.full_like(x, height)
    beat = 1.0
    if beat_mode == "pulse" and frame_index % max(1, fps) < 3:
        beat = 2.0

    for layer in range(wave_layers):
        base_y = height * (0.22 + 0.58 * layer / max(1, wave_layers - 1))
        amplitude = (18 + layer * 6) * (1 + 0.3 * morph_intensity * math.sin(t * 2 + layer)) * beat
        if beat_mode == "chaos":
            amplitude *= random.uniform(0.78, 1.36)
        frequency = (0.009 + layer * 0.0026) * (1 + morph_intensity * 0.08)
        phase = layer * 0.85
        speed = 1.15 + layer * 0.18
        y = base_y + amplitude * np.sin(frequency * x + phase + t * speed)
        y += (amplitude * 0.32) * np.sin(frequency * 2.1 * x - t * (speed * 0.7))
        color = _color_at(colors, layer + t * color_speed * 0.65)
        ax.fill_between(x, y, previous_wave, color=color, alpha=0.16 + layer * 0.018)
        ax.plot(x, y, color=color, alpha=0.62, linewidth=1.15)
        previous_wave = y

    center_x = width / 2 + math.sin(t * 0.42) * 38
    center_y = height / 2 + math.cos(t * 0.36) * 24
    particle_x = []
    particle_y = []
    particle_size = []
    particle_color = []
    particle_edge = []
    for row in particles.itertuples(index=False):
        angle = row.phase + t * row.speed
        px = center_x + row.radius * math.cos(angle)
        py = center_y + row.radius * math.sin(angle) * 0.4
        for sx, sy in _symmetry_points(px, py, center_x, center_y, symmetry):
            particle_x.append(sx)
            particle_y.append(sy)
            particle_size.append(row.size)
            color = _color_at(colors, row.color_offset + t * color_speed)
            particle_color.append(color + (0.7,))
            particle_edge.append(tuple(min(1, channel + 0.24) for channel in color) + (0.82,))

    ax.scatter(
        particle_x,
        particle_y,
        s=particle_size,
        c=particle_color,
        edgecolors=particle_edge,
        linewidths=0.45,
    )

    theta = np.linspace(0, math.tau, 220)
    n = 3 + int(t / 2) % 5
    pulse_scale = 1.5 if beat_mode == "pulse" and frame_index % max(1, fps) < 3 else 1.0
    base_radius = 70 * pulse_scale
    rotation = t * 0.5
    radius = base_radius * (1 + morph_intensity * 0.3 * np.sin(n * theta + t * 1.5))
    form_x = center_x + radius * np.cos(theta + rotation)
    form_y = center_y + radius * np.sin(theta + rotation)
    form_color = _color_at(colors, t * color_speed + 1.5)
    ax.fill(form_x, form_y, color=form_color + (0.34,), linewidth=0)
    ax.plot(form_x, form_y, color=tuple(min(1, channel + 0.18) for channel in form_color), alpha=0.86, linewidth=1.6)

    shimmer_x = np.arange(0, width, 28)
    shimmer_y = np.arange(0, height, 28)
    sx, sy = np.meshgrid(shimmer_x, shimmer_y)
    shimmer_alpha = np.maximum(0, np.sin(sx / 10 + t * 3)) * 0.3
    ax.scatter(sx.flatten(), sy.flatten(), s=5, c="white", alpha=float(np.mean(shimmer_alpha)) * 0.42, linewidths=0)

    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    return fig


def generate_pulsar_animation(
    theme_name: str = "aurora",
    duration: int = 6,
    fps: int = 24,
    wave_layers: int = 5,
    particle_count: int = 80,
    color_speed: float = 1.0,
    morph_intensity: float = 1.0,
    symmetry: int = 1,
    beat_mode: str = "smooth",
) -> tuple[bytes, dict]:
    duration = _clamp(duration, 3, 12, int)
    fps = _clamp(fps, 12, 30, int)
    wave_layers = _clamp(wave_layers, 2, 10, int)
    particle_count = _clamp(particle_count, 20, 200, int)
    color_speed = _clamp(color_speed, 0.5, 3.0, float)
    morph_intensity = _clamp(morph_intensity, 0.5, 2.0, float)
    symmetry = int(symmetry) if int(symmetry) in SYMMETRY_LABELS else 1
    beat_mode = beat_mode if beat_mode in {"smooth", "pulse", "chaos"} else "smooth"
    theme_name = theme_name if theme_name in ANIMATION_THEMES else "aurora"
    theme = ANIMATION_THEMES[theme_name]
    total_frames = duration * fps
    particles = _build_particles(particle_count, seed=total_frames + wave_layers + symmetry)

    frames = []
    for frame_index in range(total_frames):
        fig = _render_frame(
            frame_index,
            total_frames,
            theme,
            duration,
            fps,
            wave_layers,
            particles,
            color_speed,
            morph_intensity,
            symmetry,
            beat_mode,
        )
        buffer = BytesIO()
        fig.savefig(buffer, format="png", dpi=80, facecolor=theme["background"])
        plt.close(fig)
        buffer.seek(0)
        frame = Image.open(buffer).convert("P", palette=Image.ADAPTIVE, colors=256)
        frames.append(frame)

    gif_buffer = BytesIO()
    frames[0].save(
        gif_buffer,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        duration=int(1000 / fps),
        loop=0,
        optimize=False,
    )
    gif_bytes = gif_buffer.getvalue()
    stats = {
        "frames": total_frames,
        "duration": duration,
        "fps": fps,
        "particles": particle_count,
        "waves": wave_layers,
        "theme": theme_name,
        "symmetry": SYMMETRY_LABELS[symmetry],
        "beat": beat_mode,
        "size_mb": round(len(gif_bytes) / 1024 / 1024, 2),
    }
    return gif_bytes, stats


def generate_data_art(days=45, theme_name="aurora", density=5):
    gif_bytes, stats = generate_pulsar_animation(
        theme_name=theme_name,
        duration=3,
        fps=12,
        wave_layers=density,
        particle_count=max(20, min(200, int(days) * 2)),
    )
    first_frame = Image.open(BytesIO(gif_bytes))
    png_buffer = BytesIO()
    first_frame.convert("RGB").save(png_buffer, format="PNG")
    image_base64 = base64.b64encode(png_buffer.getvalue()).decode("ascii")
    return image_base64, stats
