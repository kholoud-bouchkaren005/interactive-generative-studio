# Interactive Generative Studio

Interactive Generative Studio is an ENSA term project built with Flask. The goal is to create a creative web platform where users can explore generative art, interact with visual tools, manipulate media, visualize data artistically, and experiment with a small machine learning bonus.

## Project Structure

```text
interactive-generative-studio/
|-- app.py                  # Main Flask app and route architecture
|-- ml_module.py            # Axe 6 K-means color extraction module
|-- requirements.txt
|-- templates/
|   |-- base.html           # Shared Bootstrap layout and navigation
|   |-- canvas.html         # Axe 4 interactive canvas
|   |-- gallery.html        # Axe 4 artwork gallery
|   |-- ml_palette.html     # Axe 6 ML color extraction page
|   `-- placeholder.html    # TODO placeholder for partner axes
|-- uploads/                # Uploaded images for Axe 6, generated locally
`-- app/                    # Existing package structure kept for compatibility
```

## Implemented Axes

### Axe 4 - Interactivity Module

Implemented routes:

- `/canvas`
- `/generative`
- `/interactivity`
- `/gallery`

Features:

- Interactive HTML5 canvas.
- Click or drag to draw shapes in real time.
- Shape controls: circle, square, triangle, line.
- Palette selector: Aurora, Citrus, Ink, Neon.
- Sliders for shape size and burst density.
- Animation toggle.
- Buttons for Random, Clear, and Download PNG.
- Responsive gallery with artwork thumbnail examples.

Main files:

- `templates/canvas.html`
- `templates/gallery.html`

### Axe 6 - Optional ML Bonus: Color Extraction

Implemented routes:

- `/ml-palette`
- `/axe6`
- `/upload`

Features:

- Upload an image.
- Choose the number of dominant colors.
- Extract colors using K-means clustering.
- Display HEX, RGB, and percentage distribution for each color.

Main files:

- `ml_module.py`
- `templates/ml_palette.html`

## TODO For Team Members

### Axe 1 - Generative Art

Route placeholder:

- `/axe1`

Where to add code:

- Add routes or logic in `app.py` near the `Axe 1` TODO block.
- Add a new template, for example `templates/axe1_generative_art.html`.
- Add Python drawing logic in a separate module if needed, for example `modules/generative_art.py`.

Expected work:

- Generative artwork using loops, randomness, and conditionals.
- At least one OOP-based artwork with classes.
- Optional Pygame, Turtle, Matplotlib, or dynamic Flask image generation.

### Axe 2 - Data Art

Route placeholder:

- `/axe2`

Where to add code:

- Add routes or logic in `app.py` near the `Axe 2` TODO block.
- Add a new template, for example `templates/axe2_data_art.html`.
- Add data processing logic in a separate module if needed, for example `modules/data_art.py`.

Expected work:

- Load and clean a small dataset with Pandas.
- Create an artistic visualization using Matplotlib or Seaborn.
- Display the generated visual output on the web page.

### Axe 3 - Image or Audio Editing

Route placeholder:

- `/axe3`

Where to add code:

- Add routes or logic in `app.py` near the `Axe 3` TODO block.
- Add a new template, for example `templates/axe3_media_tools.html`.
- Add processing logic in a separate module if needed, for example `modules/media_tools.py`.

Expected work:

- Image option: grayscale, sepia, neon, inversion, blur, pixelation, contour detection, etc.
- Audio option: speed change, echo, reverb, layering, soundscape generation, etc.
- Display or download the final result.

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

Run the Flask app:

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Route Map

```text
/              Redirects to Axe 4 canvas
/axe1          TODO placeholder for Generative Art
/axe2          TODO placeholder for Data Art
/axe3          TODO placeholder for Image/Audio Editing
/canvas        Axe 4 interactive canvas
/gallery       Axe 4 artwork gallery
/ml-palette    Axe 6 ML color extraction
```

## Notes For Collaboration

- Keep each axe in its own route and template.
- Avoid changing another teammate's files unless necessary.
- Add shared styles to `templates/base.html` only when they are useful for multiple pages.
- Put reusable Python logic in separate modules instead of writing everything inside route functions.
- Commit each completed axe or feature with a clear message.
