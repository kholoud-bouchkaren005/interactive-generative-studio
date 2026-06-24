import os
import sys

from flask import Flask, render_template, request


template_dir = os.path.abspath("app/templates")
static_dir = os.path.abspath("app/static")
sys.path.insert(0, os.path.abspath("app"))

from modules.image_audio_processing.image_tools import apply_image_effect

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)


@app.route("/")
def home():
    return render_template("home.html")


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


if __name__ == "__main__":
    app.run(debug=True)
