from PIL import Image
import numpy as np
from sklearn.cluster import KMeans


def rgb_to_hex(color):
    return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))


def extract_palette(image_file, color_count=5):
    image = Image.open(image_file).convert("RGB")
    image.thumbnail((240, 240))

    pixels = np.array(image).reshape(-1, 3)
    if len(pixels) > 8000:
        sample_index = np.linspace(0, len(pixels) - 1, 8000).astype(int)
        pixels = pixels[sample_index]

    color_count = max(2, min(int(color_count), 8))
    model = KMeans(n_clusters=color_count, n_init=10, random_state=42)
    labels = model.fit_predict(pixels)
    centers = model.cluster_centers_.astype(int)
    counts = np.bincount(labels)
    order = np.argsort(counts)[::-1]

    total = counts.sum()
    palette = []
    for index in order:
        rgb = centers[index].tolist()
        palette.append({
            "hex": rgb_to_hex(rgb),
            "rgb": rgb,
            "percentage": round((counts[index] / total) * 100, 1),
        })

    return palette
