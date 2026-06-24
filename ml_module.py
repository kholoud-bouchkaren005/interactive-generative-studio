from pathlib import Path

import numpy as np
from PIL import Image
from sklearn.cluster import KMeans


def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(int(rgb[0]), int(rgb[1]), int(rgb[2]))


def extract_dominant_colors(image_path, k=5):
    """Extract dominant colors from an image with K-means clustering.

    Args:
        image_path: Path to a PNG/JPG/WEBP image.
        k: Number of colors to extract.

    Returns:
        A list of dictionaries containing HEX, RGB, and percentage distribution.
    """
    image_path = Path(image_path)
    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    k = max(2, min(int(k), 10))

    image = Image.open(image_path).convert("RGB")
    image.thumbnail((300, 300))

    pixels = np.array(image).reshape(-1, 3)
    if len(pixels) == 0:
        raise ValueError("The uploaded image contains no readable pixels.")

    if len(pixels) > 12000:
        indexes = np.linspace(0, len(pixels) - 1, 12000).astype(int)
        pixels = pixels[indexes]

    model = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = model.fit_predict(pixels)
    centers = model.cluster_centers_.astype(int)
    counts = np.bincount(labels, minlength=k)
    total = counts.sum()
    sorted_indexes = np.argsort(counts)[::-1]

    palette = []
    for index in sorted_indexes:
        rgb = centers[index].tolist()
        palette.append(
            {
                "hex": rgb_to_hex(rgb),
                "rgb": rgb,
                "percentage": round((counts[index] / total) * 100, 2),
            }
        )

    return palette
