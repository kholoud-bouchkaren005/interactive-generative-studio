import os
import sys

from flask import Flask, render_template, request


template_dir = os.path.abspath("app/templates")
static_dir = os.path.abspath("app/static")
sys.path.insert(0, os.path.abspath("app"))

from modules.data_visualization.data_art import THEMES, generate_data_art

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)


@app.route("/")
def home():
    return render_template("home.html")


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


if __name__ == "__main__":
    app.run(debug=True)
