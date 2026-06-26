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
        "colors": ["#3b0d0c", "#8f2f16", "#d8792f", "#f0b15f", "#fff0b8"],
        "background": "#080403",
        "cmap_sequence": ["afmhot", "copper", "gist_heat"],
    },
    "sunset": {
        "colors": ["#2b0710", "#7c1f1f", "#c85d2b", "#e49a45", "#f6d186"],
        "background": "#0c0505",
        "cmap_sequence": ["inferno", "YlOrBr", "gist_heat"],
    },
    "forest": {
        "colors": ["#1b0f08", "#5b2a12", "#9c5c22", "#d69a4d", "#ead7a1"],
        "background": "#070504",
        "cmap_sequence": ["copper", "YlOrBr", "pink"],
    },
    "cosmos": {
        "colors": ["#14080d", "#4b1520", "#9e3326", "#d9843f", "#f8cf7a"],
        "background": "#050307",
        "cmap_sequence": ["magma", "inferno", "copper"],
    },
    "neon": {
        "colors": ["#180907", "#6c1d12", "#b5431e", "#e8893a", "#ffe1a3"],
        "background": "#060302",
        "cmap_sequence": ["gist_heat", "afmhot", "YlOrRd"],
    },
    "sapphire": {
        "colors": ["#030916", "#0d2a4d", "#1f5f8f", "#66a6c9", "#d5ecf6"],
        "background": "#020611",
        "cmap_sequence": ["Blues", "PuBu", "cividis"],
    },
    "gold": {
        "colors": ["#120903", "#4f2607", "#9a6218", "#d7a64a", "#fff2bd"],
        "background": "#070402",
        "cmap_sequence": ["YlOrBr", "copper", "afmhot"],
    },
    "verdant": {
        "colors": ["#06120a", "#1e4a2f", "#4f8b4d", "#98c66d", "#e3e6a5"],
        "background": "#030803",
        "cmap_sequence": ["Greens", "summer", "YlGn"],
    },
    "ruby": {
        "colors": ["#140406", "#541019", "#9e2d2f", "#d96b4b", "#ffd1a3"],
        "background": "#080203",
        "cmap_sequence": ["Reds", "YlOrRd", "gist_heat"],
    },
    "amethyst": {
        "colors": ["#0b0714", "#33194f", "#6c3d7d", "#a9789f", "#ead5c7"],
        "background": "#05030a",
        "cmap_sequence": ["Purples", "magma", "pink"],
    },
    "pearl": {
        "colors": ["#0b0a08", "#3f3529", "#7f705c", "#c8b796", "#fff4d6"],
        "background": "#050403",
        "cmap_sequence": ["bone", "pink", "copper"],
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
            "radius": rng.gamma(2.3, 52, particle_count).clip(24, 265),
            "speed": rng.uniform(0.12, 0.95, particle_count),
            "phase": rng.uniform(0, math.tau, particle_count),
            "size": rng.uniform(8, 54, particle_count),
            "color_offset": rng.uniform(0, 5, particle_count),
            "arm": rng.integers(0, 4, particle_count),
            "drift": rng.uniform(-16, 16, particle_count),
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

    fig, ax = plt.subplots(figsize=(11.25, 6.25), dpi=80)
    fig.patch.set_facecolor(background)
    ax.set_facecolor(background)
    ax.set_xlim(0, width)
    ax.set_ylim(height, 0)
    ax.axis("off")

    grid_x = np.linspace(0, width, 180)
    grid_y = np.linspace(0, height, 100)
    xx, yy = np.meshgrid(grid_x, grid_y)
    hue = np.sin(xx / width * math.pi + t * color_speed) * 0.5
    hue += np.cos(yy / height * math.pi + t * 0.7) * 0.35
    hue += np.sin((xx + yy) / width * math.pi * 1.7 - t * 0.45) * 0.25
    hue = (hue - hue.min()) / max(0.001, hue.max() - hue.min())
    cmap_name = theme["cmap_sequence"][int((t * color_speed) / 2) % len(theme["cmap_sequence"])]
    ax.imshow(hue, extent=[0, width, height, 0], cmap=cmap_name, alpha=0.34, interpolation="bilinear")

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
    galaxy_tilt = 0.42
    for row in particles.itertuples(index=False):
        spiral_angle = row.phase + row.radius * 0.018 + row.arm * math.tau / 4 + t * row.speed
        breathing = 1 + 0.035 * math.sin(t * 1.6 + row.phase)
        px = center_x + row.radius * breathing * math.cos(spiral_angle)
        py = center_y + row.radius * breathing * math.sin(spiral_angle) * galaxy_tilt + row.drift
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

    core_pulse = 1 + 0.12 * math.sin(t * 1.8)
    if beat_mode == "pulse" and frame_index % max(1, fps) < 3:
        core_pulse = 1.28
    theta = np.linspace(0, 5.8 * math.pi, 520)
    for arm in range(4):
        arm_phase = arm * math.tau / 4 + t * 0.28
        radius = np.linspace(12, 260 * core_pulse, theta.size)
        arm_noise = morph_intensity * 10 * np.sin(theta * 1.7 + t * 1.2 + arm)
        arm_x = center_x + (radius + arm_noise) * np.cos(theta + arm_phase)
        arm_y = center_y + (radius + arm_noise) * np.sin(theta + arm_phase) * galaxy_tilt
        arm_color = _color_at(colors, arm + t * color_speed * 0.45)
        ax.plot(arm_x, arm_y, color=arm_color, alpha=0.24, linewidth=9.5)
        ax.plot(arm_x, arm_y, color=tuple(min(1, channel + 0.14) for channel in arm_color), alpha=0.32, linewidth=2.2)

    core_color = _color_at(colors, t * color_speed + 3.2)
    for glow in range(6, 0, -1):
        glow_size = (glow * 62 * core_pulse) ** 2 / 120
        glow_alpha = 0.018 + (7 - glow) * 0.018
        glow_color = _color_at(colors, t * color_speed + glow * 0.3)
        ax.scatter([center_x], [center_y], s=glow_size, c=[glow_color + (glow_alpha,)], linewidths=0)
    ax.scatter(
        [center_x],
        [center_y],
        s=120 * core_pulse,
        c=[tuple(min(1, channel + 0.2) for channel in core_color) + (0.78,)],
        edgecolors=[core_color + (0.88,)],
        linewidths=0.8,
    )

    shimmer_x = np.arange(0, width, 28)
    shimmer_y = np.arange(0, height, 28)
    sx, sy = np.meshgrid(shimmer_x, shimmer_y)
    shimmer_alpha = np.maximum(0, np.sin(sx / 10 + t * 3)) * 0.3
    shimmer_colors = [(1, 1, 1, alpha * 0.42) for alpha in shimmer_alpha.flatten()]
    ax.scatter(sx.flatten(), sy.flatten(), s=5, c=shimmer_colors, linewidths=0)

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
        fig.savefig(
            buffer,
            format="png",
            dpi=80,
            bbox_inches="tight",
            pad_inches=0,
            facecolor=theme["background"],
        )
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
    wave_layers = density if density is not None else 5
    gif_bytes, stats = generate_pulsar_animation(
        theme_name=theme_name,
        wave_layers=wave_layers,
        particle_count=max(20, min(200, int(days) * 2)),
    )
    first_frame = Image.open(BytesIO(gif_bytes))
    png_buffer = BytesIO()
    first_frame.convert("RGB").save(png_buffer, format="PNG")
    image_base64 = base64.b64encode(png_buffer.getvalue()).decode("ascii")
    return image_base64, stats
