import os
import sys

from flask import Flask, jsonify, redirect, render_template, request, url_for


template_dir = os.path.abspath("app/templates")
static_dir = os.path.abspath("app/static")
sys.path.insert(0, os.path.abspath("app"))

from modules.data_visualization.data_art import THEMES, generate_data_art
from modules.generative_art.artworks import PALETTES, generate_artwork
from modules.image_audio_processing.image_tools import apply_image_effect
from modules.ml_tools.color_extraction import extract_palette


app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)


MODULES = [
    {
        "key": "forma",
        "icon": "F",
        "title": "Forma",
        "route": "generative",
        "description": "Procedural geometry, infinite compositions",
    },
    {
        "key": "pulsar",
        "icon": "P",
        "title": "Pulsar",
        "route": "data_art",
        "description": "Weather rhythms turned into abstract landscapes",
    },
    {
        "key": "lens",
        "icon": "L",
        "title": "Lens",
        "route": "image_audio_tools",
        "description": "Upload, transform, and download creative filters",
    },
    {
        "key": "canvas",
        "icon": "C",
        "title": "Canvas",
        "route": "canvas",
        "description": "Draw, animate, and export in real time",
    },
    {
        "key": "chroma",
        "icon": "H",
        "title": "Chroma",
        "route": "ml_palette",
        "description": "Extract dominant colors with machine learning",
    },
]


@app.route("/")
def home():
    return render_template("home.html", modules=MODULES)


@app.route("/axe1")
@app.route("/generative")
def generative():
    return render_template(
        "generative.html",
        palettes=PALETTES.keys(),
        selected_palette="aurora",
        shape_count=60,
        max_size=48,
        artwork=None,
    )


@app.route("/generate", methods=["POST"])
def generate():
    shape_count = int(request.form.get("shape_count", 60))
    max_size = int(request.form.get("max_size", 48))
    palette = request.form.get("palette", "aurora")

    artwork = generate_artwork(
        shape_count=shape_count,
        max_size=max_size,
        palette_name=palette,
    )

    return render_template(
        "generative.html",
        palettes=PALETTES.keys(),
        selected_palette=palette,
        shape_count=shape_count,
        max_size=max_size,
        artwork=artwork,
    )


@app.route("/axe2")
@app.route("/data-art")
def data_art():
    return render_template(
        "data_art.html",
        themes=THEMES.keys(),
        selected_theme="ocean",
        days=45,
        density=6,
        artwork=None,
        stats=None,
    )


@app.route("/generate-data-art", methods=["POST"])
def generate_data_art_route():
    days = int(request.form.get("days", 45))
    density = int(request.form.get("density", 6))
    theme = request.form.get("theme", "ocean")

    artwork, stats = generate_data_art(days=days, theme_name=theme, density=density)

    return render_template(
        "data_art.html",
        themes=THEMES.keys(),
        selected_theme=theme,
        days=days,
        density=density,
        artwork=artwork,
        stats=stats,
    )


@app.route("/axe3")
@app.route("/upload")
def image_audio_tools():
    return render_template(
        "upload.html",
        selected_effect="grayscale",
        strength=4,
        output=None,
    )


@app.route("/apply-image-effect", methods=["POST"])
def apply_image_effect_route():
    image_file = request.files.get("image")
    effect = request.form.get("effect", "grayscale")
    strength = int(request.form.get("strength", 4))

    if not image_file or image_file.filename == "":
        return render_template(
            "upload.html",
            selected_effect=effect,
            strength=strength,
            output=None,
            error="Please upload an image first.",
        )

    output = apply_image_effect(image_file, effect=effect, strength=strength)

    return render_template(
        "upload.html",
        selected_effect=effect,
        strength=strength,
        output=output,
        error=None,
    )


@app.route("/axe4")
@app.route("/canvas")
@app.route("/interactivity")
def canvas():
    return render_template("canvas.html")


@app.route("/gallery")
def gallery():
    return render_template("gallery.html", modules=MODULES)


@app.route("/axe6")
@app.route("/ml-palette")
def ml_palette():
    return render_template("ml_palette.html")


@app.route("/extract-palette", methods=["POST"])
def extract_palette_route():
    image_file = request.files.get("image")
    if not image_file or image_file.filename == "":
        return jsonify({"error": "Please upload an image first."}), 400

    colors = int(request.form.get("colors", 5))
    palette = extract_palette(image_file, colors)
    return jsonify({"palette": palette})


@app.route("/legacy-home")
def legacy_home():
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
