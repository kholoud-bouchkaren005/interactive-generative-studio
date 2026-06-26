# Interactive Generative Studio

Interactive Generative Studio is a Flask web application for the ENSA Digital Creativity term project. It combines procedural image generation, cosmic GIF animation, image styling, interactive canvas drawing, web integration, and machine-learning palette extraction in one responsive studio interface.

## Final Deliverables Checklist

- Complete code base: included in this repository.
- Fully working Flask app: run with `python app.py`.
- README with installation steps and module explanations: this file.
- 2-3 page report: see `REPORT.md`.

## Team Members and Contributions

- Nihal: Axe 1 - Generative Art, Axe 2 - Pulsar Generative Animation.
- Kholoud: Axe 3 - Styler Image Editing, Axe 5 - Web Integration.
- Ghizlane: Axe 4 - Interactivity Module, Axe 6 - Palette Studio ML Bonus.

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

Optional environment variable:

```bash
set SECRET_KEY=your-secret-key
```

If `SECRET_KEY` is not set, the app uses a development fallback key.

## Implemented Modules

### Axe 1 - Forma: Generative Art

Routes:

- `/axe1`
- `/generative`
- `/generate`

Features:

- Generates procedural PNG artwork with Pillow.
- Uses randomness, loops, conditionals, and reusable OOP shape classes.
- Includes circles, squares, triangles, lines, radial bursts, flow strokes, mandala rings, and organic blobs.
- Provides controls for shape count, maximum size, and palette.
- Available palettes: `aurora`, `sunset`, `forest`, and `mono`.

Main files:

- `app/modules/generative_art/artworks.py`
- `app/templates/generative.html`

### Axe 2 - Pulsar: Generative Animation

Routes:

- `/axe2`
- `/data-art`
- `/generate-data-art`
- `/download-pulsar`

Features:

- Generates animated GIF artwork with Matplotlib, NumPy, Pandas, and Pillow.
- Creates cosmic animations inspired by galaxies, nebulae, ember fields, orbital motion, and spiral dust trails.
- Uses layered rendering: animated gradient field, breathing wave bands, orbiting particles, galactic arms, glowing core, and shimmer overlay.
- Provides controls for theme, duration, FPS, wave layers, particle count, color speed, morph intensity, symmetry, and beat mode.
- Includes multiple cinematic palettes: `aurora`, `sunset`, `forest`, `cosmos`, `neon`, `sapphire`, `gold`, `verdant`, `ruby`, `amethyst`, and `pearl`.
- Shows render statistics including frames, duration, FPS, particles, waves, symmetry, and file size.
- Supports downloadable animated GIF export through `/download-pulsar`.

Main files:

- `app/modules/data_visualization/data_art.py`
- `app/templates/data_art.html`

### Axe 3 - Styler: Image Editing

Routes:

- `/axe3`
- `/upload`
- `/apply-image-effect`

Features:

- Uploads an image and applies creative visual effects.
- Keeps the last uploaded image available during the session so users can try multiple effects without re-uploading.
- Effects include grayscale, sepia, neon, invert, blur, pixelate, contour, mirror, and rotate.
- Uses a strength control for effects that support intensity.
- Saves the working source image in `app/static/generated/lens_source.png`.
- Displays edited output and supports PNG download from the interface.

Main files:

- `app/modules/image_audio_processing/image_tools.py`
- `app/templates/upload.html`
- `app/static/generated/`

### Axe 4 - Canvas: Interactivity Module

Routes:

- `/axe4`
- `/canvas`
- `/interactivity`
- `/gallery`

Features:

- Interactive HTML5 canvas drawing experience.
- Users can click or drag to add animated shapes in real time.
- Controls for shape type, palette, size, burst density, and animation behavior.
- Includes randomize, clear, and PNG download actions.
- Gallery page displays the available studio modules.

Main files:

- `app/templates/canvas.html`
- `app/templates/gallery.html`
- `app/static/main.js`

### Axe 5 - Web Integration

Routes:

- `/`
- `/legacy-home`
- all module routes listed above

Features:

- Unified Flask entry point in `app.py`.
- Shared dashboard navigation through the `MODULES` route map.
- Shared base template and responsive CSS.
- Redirects `/legacy-home` to the current home route.
- Connects Forma, Pulsar, Styler, Canvas, and Palette Studio into one application.

Main files:

- `app.py`
- `app/templates/base.html`
- `app/templates/home.html`
- `app/static/style.css`

### Axe 6 - Palette Studio: ML Color Extraction

Routes:

- `/axe6`
- `/ml-palette`
- `/extract-palette`

Features:

- Uploads an image and extracts dominant colors.
- Uses K-means clustering from scikit-learn.
- Returns palette data as JSON through `/extract-palette`.
- Displays HEX, RGB, and percentage distribution for each detected color.

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
|-- index.html
|-- app/
|   |-- modules/
|   |   |-- generative_art/
|   |   |   `-- artworks.py
|   |   |-- data_visualization/
|   |   |   `-- data_art.py
|   |   |-- image_audio_processing/
|   |   |   `-- image_tools.py
|   |   `-- ml_tools/
|   |       `-- color_extraction.py
|   |-- static/
|   |   |-- generated/
|   |   |-- main.js
|   |   `-- style.css
|   `-- templates/
|       |-- base.html
|       |-- home.html
|       |-- generative.html
|       |-- data_art.html
|       |-- upload.html
|       |-- canvas.html
|       |-- gallery.html
|       |-- ml_palette.html
|       `-- module_placeholder.html
```

## Tools Used

- Flask and Jinja2 for routing, rendering, and templates.
- Pillow for PNG generation, image effects, and GIF frame assembly.
- Matplotlib for Pulsar animation frame rendering.
- NumPy and Pandas for animation data and numerical processing.
- scikit-learn KMeans for ML color extraction.
- HTML, CSS, and JavaScript for the frontend, canvas interactions, and dynamic controls.

## Notes

The application is organized so each creative module has its own route, template, and Python logic while sharing the same Flask app shell. Generated or temporary user-facing assets are kept under `app/static/generated/`, and the project can be presented from the dashboard at `/`.
