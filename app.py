import base64
import os
import sys

from flask import Flask, Response, jsonify, redirect, render_template, request, session, url_for


template_dir = os.path.abspath("app/templates")
static_dir = os.path.abspath("app/static")
sys.path.insert(0, os.path.abspath("app"))

from modules.data_visualization.data_art import ANIMATION_THEMES, generate_pulsar_animation
from modules.generative_art.artworks import PALETTES, generate_artwork
from modules.image_audio_processing.image_tools import apply_image_effect, image_to_base64, load_image_source
from modules.ml_tools.color_extraction import extract_palette


app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.secret_key = os.environ.get("SECRET_KEY", "interactive-generative-studio-dev")
generated_dir = os.path.join(static_dir, "generated")
os.makedirs(generated_dir, exist_ok=True)
LENS_SOURCE_PATH = os.path.join(generated_dir, "lens_source.png")


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
        "description": "Living generative pulses exported as animated GIFs",
    },
    {
        "key": "lens",
        "icon": "S",
        "title": "Styler",
        "route": "image_audio_tools",
        "description": "Change the style of an image with creative filters",
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
        "icon": "P",
        "title": "Palette Studio",
        "route": "ml_palette",
        "description": "Turn any image into a reusable color palette",
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
        themes=list(ANIMATION_THEMES.keys()),
        selected_theme="aurora",
        duration=6,
        fps=24,
        wave_layers=5,
        particle_count=80,
        color_speed=1.0,
        morph_intensity=1.0,
        symmetry=1,
        beat_mode="smooth",
        animation=None,
        stats=None,
    )


@app.route("/generate-data-art", methods=["POST"])
def generate_data_art_route():
    theme = request.form.get("theme", "aurora")
    duration = int(request.form.get("duration", 6))
    fps = int(request.form.get("fps", 24))
    wave_layers = int(request.form.get("wave_layers", 5))
    particle_count = int(request.form.get("particle_count", 80))
    color_speed = float(request.form.get("color_speed", 1.0))
    morph_intensity = float(request.form.get("morph_intensity", 1.0))
    symmetry = int(request.form.get("symmetry", 1))
    beat_mode = request.form.get("beat_mode", "smooth")

    gif_bytes, stats = generate_pulsar_animation(
        theme_name=theme,
        duration=duration,
        fps=fps,
        wave_layers=wave_layers,
        particle_count=particle_count,
        color_speed=color_speed,
        morph_intensity=morph_intensity,
        symmetry=symmetry,
        beat_mode=beat_mode,
    )
    animation_b64 = base64.b64encode(gif_bytes).decode("ascii")

    return render_template(
        "data_art.html",
        themes=list(ANIMATION_THEMES.keys()),
        selected_theme=theme,
        duration=duration,
        fps=fps,
        wave_layers=wave_layers,
        particle_count=particle_count,
        color_speed=color_speed,
        morph_intensity=morph_intensity,
        symmetry=symmetry,
        beat_mode=beat_mode,
        animation=animation_b64,
        stats=stats,
    )


@app.route("/download-pulsar", methods=["POST"])
def download_pulsar():
    theme = request.form.get("theme", "aurora")
    duration = int(request.form.get("duration", 6))
    fps = int(request.form.get("fps", 24))
    wave_layers = int(request.form.get("wave_layers", 5))
    particle_count = int(request.form.get("particle_count", 80))
    color_speed = float(request.form.get("color_speed", 1.0))
    morph_intensity = float(request.form.get("morph_intensity", 1.0))
    symmetry = int(request.form.get("symmetry", 1))
    beat_mode = request.form.get("beat_mode", "smooth")

    gif_bytes, _ = generate_pulsar_animation(
        theme_name=theme,
        duration=duration,
        fps=fps,
        wave_layers=wave_layers,
        particle_count=particle_count,
        color_speed=color_speed,
        morph_intensity=morph_intensity,
        symmetry=symmetry,
        beat_mode=beat_mode,
    )
    return Response(
        gif_bytes,
        mimetype="image/gif",
        headers={"Content-Disposition": f"attachment; filename=pulsar_{theme}.gif"},
    )


@app.route("/axe3")
@app.route("/upload")
def image_audio_tools():
    saved_image = None
    if session.get("lens_image_saved") and os.path.exists(LENS_SOURCE_PATH):
        saved_image = image_to_base64(load_image_source(LENS_SOURCE_PATH))

    return render_template(
        "upload.html",
        selected_effect="grayscale",
        strength=4,
        output=None,
        saved_image=saved_image,
    )


@app.route("/apply-image-effect", methods=["POST"])
def apply_image_effect_route():
    image_file = request.files.get("image")
    effect = request.form.get("effect", "grayscale")
    strength = int(request.form.get("strength", 4))
    saved_image = None

    if image_file and image_file.filename != "":
        base_image = load_image_source(image_file)
        base_image.thumbnail((1100, 760))
        base_image.save(LENS_SOURCE_PATH, format="PNG")
        session["lens_image_saved"] = True
    elif session.get("lens_image_saved") and os.path.exists(LENS_SOURCE_PATH):
        base_image = load_image_source(LENS_SOURCE_PATH)
    else:
        return render_template(
            "upload.html",
            selected_effect=effect,
            strength=strength,
            output=None,
            saved_image=None,
            error="Please upload an image first.",
        )

    saved_image = image_to_base64(base_image)
    output = apply_image_effect(base_image, effect=effect, strength=strength)

    return render_template(
        "upload.html",
        selected_effect=effect,
        strength=strength,
        output=output,
        saved_image=saved_image,
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
