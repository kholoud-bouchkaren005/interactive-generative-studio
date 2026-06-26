import base64
from io import BytesIO

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


THEMES = {
    "ocean": {
        "line": "#1f7a8c",
        "fill": "#3dd6d0",
        "accent": "#0b3954",
        "background": "#f4fbfb",
    },
    "sunset": {
        "line": "#e76f51",
        "fill": "#f7d060",
        "accent": "#8338ec",
        "background": "#fff8ef",
    },
    "forest": {
        "line": "#2d6a4f",
        "fill": "#95d5b2",
        "accent": "#1b4332",
        "background": "#f3fbf5",
    },
}


def build_weather_dataset(days=45, seed=7):
    rng = np.random.default_rng(seed)
    dates = pd.date_range("2026-01-01", periods=days, freq="D")
    day_index = np.arange(days)

    temperature = 18 + np.sin(day_index / 5) * 7 + rng.normal(0, 1.8, days)
    humidity = 58 + np.cos(day_index / 7) * 17 + rng.normal(0, 3.5, days)
    wind = 12 + np.sin(day_index / 3) * 5 + rng.normal(0, 1.4, days)

    data = pd.DataFrame(
        {
            "date": dates,
            "temperature": temperature,
            "humidity": humidity.clip(25, 95),
            "wind": wind.clip(1, 32),
        }
    )
    data["creative_index"] = (
        data["temperature"] * 0.48 + data["humidity"] * 0.32 + data["wind"] * 0.2
    )
    return data


def generate_data_art(days=45, theme_name="ocean", density=6):
    days = max(20, min(int(days), 90))
    density = max(3, min(int(density), 12))
    theme = THEMES.get(theme_name, THEMES["ocean"])
    data = build_weather_dataset(days=days, seed=days + density)

    x = np.arange(len(data))
    y = data["creative_index"].to_numpy()
    y_norm = (y - y.min()) / (y.max() - y.min())

    fig, ax = plt.subplots(figsize=(11, 6.5), dpi=120)
    fig.patch.set_facecolor(theme["background"])
    ax.set_facecolor(theme["background"])

    for layer in range(density):
        offset = layer * 0.08
        wave = y_norm + np.sin(x / (2.2 + layer * 0.18)) * 0.06 + offset
        alpha = 0.16 + layer * 0.035
        ax.fill_between(x, offset, wave, color=theme["fill"], alpha=min(alpha, 0.56))
        ax.plot(x, wave, color=theme["line"], linewidth=1.2, alpha=0.5)

    scatter_size = data["wind"].to_numpy() * 9
    ax.scatter(
        x,
        y_norm + 0.18,
        c=data["humidity"],
        s=scatter_size,
        cmap="viridis",
        alpha=0.72,
        edgecolors=theme["accent"],
        linewidths=0.35,
    )

    ax.set_title("Weather Rhythm Landscape", fontsize=20, weight="bold", color=theme["accent"])
    ax.set_xlabel("Timeline", color=theme["accent"])
    ax.set_ylabel("Creative weather index", color=theme["accent"])
    ax.grid(True, alpha=0.16)
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color(theme["accent"])
    ax.tick_params(colors=theme["accent"])

    stats = {
        "days": days,
        "avg_temperature": round(float(data["temperature"].mean()), 1),
        "avg_humidity": round(float(data["humidity"].mean()), 1),
        "avg_wind": round(float(data["wind"].mean()), 1),
    }

    buffer = BytesIO()
    fig.tight_layout()
    fig.savefig(buffer, format="png", bbox_inches="tight")
    plt.close(fig)

    image_base64 = base64.b64encode(buffer.getvalue()).decode("ascii")
    return image_base64, stats
