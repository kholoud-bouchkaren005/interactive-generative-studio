# Interactive Generative Studio

Interactive Generative Studio is a Flask web application for the ENSA Digital Creativity term project. It brings together generative art, real-time inspired animation, image editing, interactive drawing, web integration, and a small machine-learning color extraction bonus.

## Final Deliverables Checklist

- Complete code base: included in this repository.
- Fully working Flask app: run with `python app.py`.
- README with installation steps and explanations: this file.
- 2-3 page report: see `REPORT.md`.

GitHub repository:

```text
https://github.com/kholoud-bouchkaren005/interactive-generative-studio
```

## Quick Start Guide for the Professor

This guide explains how to get the project from GitHub and run it locally.

### 1. Download the project from GitHub

Open this repository in the browser:

```text
https://github.com/kholoud-bouchkaren005/interactive-generative-studio
```

Then choose one of these two methods:

**Method A - Download ZIP**

1. Click the green `Code` button.
2. Click `Download ZIP`.
3. Extract the ZIP file.
4. Open the extracted folder named `interactive-generative-studio`.

**Method B - Clone with Git**

If Git is installed, open a terminal and run:

```bash
git clone https://github.com/kholoud-bouchkaren005/interactive-generative-studio.git
cd interactive-generative-studio
```

### 2. Open the project folder in a terminal

If the project was downloaded as ZIP, open a terminal inside the extracted folder.

On Windows, this can be done by opening the folder, clicking the address bar, typing `cmd`, and pressing Enter.

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

On Windows:

```bash
.venv\Scripts\activate
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

### 5. Install the required libraries

```bash
pip install -r requirements.txt
```

### 6. Run the Flask application

```bash
python app.py
```

### 7. Open the application in the browser

After running `python app.py`, open:

```text
http://127.0.0.1:5000
```

If the browser does not open automatically, copy this link and paste it manually into the browser.

## Team Members and Contributions

- Nihal: Axe 1 - Generative Art, Axe 2 - Pulsar Generative Animation.
- Kholoud: Axe 3 - Image Editing, Axe 5 - Web Integration.
- Ghizlane: Axe 4 - Interactivity Module, Axe 6 - ML Color Extraction Bonus.

## Installation

Recommended Python version:

```text
Python 3.11
```

Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

If there are dependency problems, check that the virtual environment is activated and that all team members are using the same dependency list from `requirements.txt`.

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

### Axe 2 - Pulsar Generative Animation

Routes:

- `/axe2`
- `/data-art`
- `/generate-data-art`
- `/download-pulsar`

Features:

- Generates animated GIF artwork with Matplotlib, NumPy, Pandas, and Pillow.
- Creates a warm cosmic visual system inspired by galaxies, nebulae, ember fields, and orbital motion.
- Uses layered rendering: nebula gradient field, breathing wave bands, spiral dust particles, galactic arms, glowing core, and shimmer texture.
- Provides controls for theme, duration, FPS, wave layers, particle count, color speed, morph intensity, symmetry, and beat mode.
- Includes multiple cinematic palettes, including warm amber, blue sapphire, refined gold, verdant green, ruby, amethyst, and soft pearl variants.
- Shows render statistics including frame count, duration, FPS, particles, waves, symmetry, and file size.
- Supports downloadable animated GIF export through `/download-pulsar`.

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
- Pillow for generative image rendering, GIF assembly, and image effects.
- Pandas and NumPy for data processing.
- Matplotlib for generative animation frame rendering.
- scikit-learn KMeans for ML color extraction.
- HTML, CSS, and JavaScript for frontend interaction.

## Technical Pipeline

1. The user opens the Flask web application from the browser.
2. The user selects a module from the dashboard.
3. The frontend sends form data, uploaded files, or canvas actions.
4. Flask receives the request through the corresponding route.
5. The selected Python module processes the input.
6. The result is returned as an image, GIF, JSON response, or rendered HTML page.
7. The browser displays the final creative result and allows download when available.

## GitHub Workflow

The team used GitHub to organize and merge the work. Each major axis was developed on a dedicated branch, then merged progressively into the main application.

Main branches used during the project:

- `axe1-GenArtStudio`
- `axe2-data-art`
- `axe3-GenArtStudio`
- `axe4-ghizlane`
- `axe5-web-integration`
- `feature/kholoud`
- `feature/forma-redesign`
- `main`

This workflow helped separate responsibilities, test modules independently, and combine the final version through pull requests and merges.

## Challenges and Solutions

- GitHub collaboration was difficult at the beginning because of branches, pull requests, and merge conflicts. The solution was to organize the work by axes and merge changes progressively.
- Team members had different Python versions, including Python 3.11 and Python 3.14. This caused dependency issues, so the project uses a shared `requirements.txt` file and a virtual environment.
- Different development tools were used, mainly Visual Studio Code and PyCharm. To avoid committing local IDE settings, `.gitignore` excludes files such as `.idea`, cache folders, and virtual environment folders.
- Generated images and animations needed to be displayed in the browser. The solution was to generate images in memory and return them as Base64 images or downloadable GIF files.
- The animation module can become heavy when the duration, FPS, waves, and particles are high. The interface provides controls to balance quality and generation time.
- Combining all axes into one app required a clean route structure. The final solution uses a central `app.py` file and separate module folders for the processing logic.

## Notes

The final application is designed so each module has its own route, template, and Python logic. This keeps the code easier to maintain and makes the project suitable for final merging and presentation.
