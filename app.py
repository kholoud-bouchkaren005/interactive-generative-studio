import os

from flask import Flask, render_template


template_dir = os.path.abspath("app/templates")
static_dir = os.path.abspath("app/static")

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)


MODULES = [
    {
        "axe": "Axe 1",
        "title": "Generative Art",
        "route": "generative",
        "description": "Procedural artworks built with loops, randomness, and OOP shapes.",
    },
    {
        "axe": "Axe 2",
        "title": "Data Art",
        "route": "data_art",
        "description": "Artistic visualizations generated from processed datasets.",
    },
    {
        "axe": "Axe 3",
        "title": "Image/Audio Tools",
        "route": "upload",
        "description": "Creative media upload workflows for filters and transformations.",
    },
    {
        "axe": "Axe 4",
        "title": "Interactive Canvas",
        "route": "canvas",
        "description": "Real-time drawing tools with sliders, palettes, and animation.",
    },
    {
        "axe": "Axe 6",
        "title": "ML Palette",
        "route": "ml_palette",
        "description": "Dominant color extraction with K-means clustering.",
    },
]


@app.route("/")
def home():
    return render_template("home.html", modules=MODULES)


@app.route("/generative")
@app.route("/axe1")
def generative():
    return render_template(
        "module_placeholder.html",
        axe="Axe 1",
        title="Generative Art",
        description="Team Axe 1 will connect the final generative artwork module here.",
    )


@app.route("/data-art")
@app.route("/axe2")
def data_art():
    return render_template(
        "module_placeholder.html",
        axe="Axe 2",
        title="Data Art",
        description="Team Axe 2 will connect the final data-driven visualization module here.",
    )


@app.route("/upload")
@app.route("/axe3")
def upload():
    return render_template(
        "module_placeholder.html",
        axe="Axe 3",
        title="Image/Audio Tools",
        description="Team Axe 3 will connect the final media editing module here.",
    )


@app.route("/canvas")
@app.route("/interactivity")
@app.route("/axe4")
def canvas():
    return render_template(
        "module_placeholder.html",
        axe="Axe 4",
        title="Interactive Canvas",
        description="Team Axe 4 will connect the final interactivity module here.",
    )


@app.route("/gallery")
def gallery():
    return render_template("gallery.html", modules=MODULES)


@app.route("/ml-palette")
@app.route("/axe6")
def ml_palette():
    return render_template(
        "module_placeholder.html",
        axe="Axe 6",
        title="ML Palette",
        description="Team Axe 6 will connect the final K-means color extraction module here.",
    )


if __name__ == "__main__":
    app.run(debug=True)
