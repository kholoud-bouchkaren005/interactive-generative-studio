import os
import sys

from flask import Flask, render_template, request


template_dir = os.path.abspath("app/templates")
static_dir = os.path.abspath("app/static")
sys.path.insert(0, os.path.abspath("app"))

from modules.generative_art.artworks import PALETTES, generate_artwork

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)


@app.route("/")
def home():
    return render_template("home.html")


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


if __name__ == "__main__":
    app.run(debug=True)
