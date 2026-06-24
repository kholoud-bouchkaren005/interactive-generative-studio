from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

from ml_module import extract_dominant_colors


BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

app = Flask(__name__)
app.config["SECRET_KEY"] = "interactive-generative-studio-dev-key"
app.config["UPLOAD_FOLDER"] = UPLOAD_DIR


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def home():
    return redirect(url_for("canvas"))


# TODO Axe 1: Generative Art
# Partners can replace this placeholder with their Python/Pygame/Matplotlib artwork routes.
@app.route("/axe1")
def axe1_placeholder():
    return render_template(
        "placeholder.html",
        axe_title="Axe 1 - Generative Art",
        description="TODO: Add loops, randomness, OOP shapes, and generated artwork outputs here.",
    )


# TODO Axe 2: Data-Driven Creative Visualization
# Partners can plug Pandas/Matplotlib/Seaborn visualizations into this route.
@app.route("/axe2")
def axe2_placeholder():
    return render_template(
        "placeholder.html",
        axe_title="Axe 2 - Data Art",
        description="TODO: Add dataset loading, cleaning, and artistic visualizations here.",
    )


# TODO Axe 3: Image or Audio Editing
# Partners can connect PIL/OpenCV/PyDub effects and upload workflows here.
@app.route("/axe3")
def axe3_placeholder():
    return render_template(
        "placeholder.html",
        axe_title="Axe 3 - Image/Audio Editing",
        description="TODO: Add image filters, distortions, audio effects, and export features here.",
    )


# Axe 4: Interactivity Module
@app.route("/canvas")
@app.route("/generative")
@app.route("/interactivity")
def canvas():
    return render_template("canvas.html")


@app.route("/gallery")
def gallery():
    return render_template("gallery.html")


# Axe 6: Optional ML Bonus - Color Extraction
@app.route("/ml-palette", methods=["GET", "POST"])
@app.route("/axe6", methods=["GET", "POST"])
@app.route("/upload", methods=["GET", "POST"])
def ml_palette():
    palette = None
    uploaded_filename = None
    k = 5

    if request.method == "POST":
        k = int(request.form.get("k", 5))
        image = request.files.get("image")

        if not image or image.filename == "":
            flash("Please choose an image file.")
            return render_template("ml_palette.html", palette=palette, k=k)

        if not allowed_file(image.filename):
            flash("Allowed formats: PNG, JPG, JPEG, WEBP.")
            return render_template("ml_palette.html", palette=palette, k=k)

        filename = secure_filename(image.filename)
        image_path = app.config["UPLOAD_FOLDER"] / filename
        image.save(image_path)
        uploaded_filename = filename

        try:
            palette = extract_dominant_colors(image_path, k=k)
        except Exception as exc:
            flash(f"Color extraction failed: {exc}")

    return render_template(
        "ml_palette.html",
        palette=palette,
        uploaded_filename=uploaded_filename,
        k=k,
    )


if __name__ == "__main__":
    app.run(debug=True)
