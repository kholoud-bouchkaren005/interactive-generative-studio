# Interactive Generative Studio

Interactive Generative Studio is a Flask web application for the ENSA Digital Creativity term project. It brings together generative art, data-driven visualization, image editing, interactive drawing, web integration, and a small machine-learning color extraction bonus.

## Final Deliverables Checklist

- Complete code base: included in this repository.
- Fully working Flask app: run with `python app.py`.
- README with installation steps and explanations: this file.
- 2-3 page report: see `REPORT.md`.

## Team Members and Contributions

- Nihal: Axe 1 - Generative Art, Axe 2 - Data-Driven Creative Visualization.
- Kholoud: Axe 3 - Image Editing, Axe 5 - Web Integration.
- Ghizlane: Axe 4 - Interactivity Module, Axe 6 - ML Color Extraction Bonus.

## Installation

Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

Open the app in your browser:

```text
http://127.0.0.1:5000
```

## Implemented Modules

### Axe 1 - Generative Art

Routes:

- `/axe1`
- `/generative`
- `/generate`

Features:

- Generates geometric artwork as PNG.
- Uses loops, randomness, and conditionals.
- Uses OOP shape classes: circle, square, triangle, and line.
- Provides controls for number of shapes, maximum size, and palette.

Main files:

- `app/modules/generative_art/artworks.py`
- `app/templates/generative.html`

### Axe 2 - Data-Driven Creative Visualization

Routes:

- `/axe2`
- `/data-art`
- `/generate-data-art`

Features:

- Builds a simulated weather dataset with Pandas.
- Creates an abstract landscape visualization with Matplotlib.
- Provides controls for dataset size, density, and visual theme.
- Displays summary statistics and PNG download.

Main files:

- `app/modules/data_visualization/data_art.py`
- `app/templates/data_art.html`

### Axe 3 - Image Editing

Routes:

- `/axe3`
- `/upload`
- `/apply-image-effect`

Features:

- Upload an image and apply creative effects.
- Effects include grayscale, sepia, neon, invert, blur, pixelate, contour, mirror, and rotate.
- Displays edited output and allows PNG download.

Main files:

- `app/modules/image_audio_processing/image_tools.py`
- `app/templates/upload.html`

### Axe 4 - Interactivity Module

Routes:

- `/axe4`
- `/canvas`
- `/interactivity`
- `/gallery`

Features:

- Interactive HTML5 canvas.
- Users can click or drag to add shapes in real time.
- Controls for shape type, palette, size, burst density, and animation.
- Random, clear, and download PNG buttons.
- Gallery page for module previews and generated outputs.

Main files:

- `app/templates/canvas.html`
- `app/templates/gallery.html`
- `app/static/main.js`

### Axe 5 - Web Integration

Routes:

- `/`
- all module routes listed above

Features:

- Unified Flask application entry point.
- Dashboard with navigation to all axes.
- Shared responsive styling.
- Gallery page.
- Route map that connects the modules into a single web app.

Main files:

- `app.py`
- `app/templates/home.html`
- `app/static/style.css`

### Axe 6 - Optional ML Bonus: Color Extraction

Routes:

- `/axe6`
- `/ml-palette`
- `/extract-palette`

Features:

- Upload an image.
- Extract dominant colors with K-means clustering.
- Displays HEX, RGB, and percentage distribution for each color.

Main files:

- `app/modules/ml_tools/color_extraction.py`
- `app/templates/ml_palette.html`
- `app/static/main.js`

## Project Structure

```text
interactive-generative-studio/
|-- app.py
|-- README.md
|-- REPORT.md
|-- requirements.txt
|-- app/
|   |-- modules/
|   |   |-- generative_art/
|   |   |-- data_visualization/
|   |   |-- image_audio_processing/
|   |   `-- ml_tools/
|   |-- static/
|   |   |-- style.css
|   |   `-- main.js
|   `-- templates/
|       |-- home.html
|       |-- generative.html
|       |-- data_art.html
|       |-- upload.html
|       |-- canvas.html
|       |-- gallery.html
|       `-- ml_palette.html
```

## Tools Used

- Flask and Jinja2 for web routing and templates.
- Pillow for generative image rendering and image effects.
- Pandas and NumPy for data processing.
- Matplotlib for artistic data visualization.
- scikit-learn KMeans for ML color extraction.
- HTML, CSS, and JavaScript for frontend interaction.

## Notes

The final application is designed so each module has its own route, template, and Python logic. This keeps the code easier to maintain and makes the project suitable for final merging and presentation.
