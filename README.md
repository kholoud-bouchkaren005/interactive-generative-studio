# Interactive Generative Studio - Axe 5 Web Integration

This branch implements the Flask web integration layer for the ENSA term project.

## Objective

Axe 5 provides the web application structure that connects all project modules into one usable Flask studio.

It includes:

- Home dashboard
- Navigation bar for all axes
- Module pages for Axe 1, Axe 2, Axe 3, Axe 4, and Axe 6
- Gallery page
- Clean Flask route map
- Responsive CSS layout
- Deployment-ready `python app.py` entry point

## Routes

```text
/              Home dashboard
/axe1          Generative Art placeholder
/generative    Alias for Axe 1
/axe2          Data Art placeholder
/data-art      Alias for Axe 2
/axe3          Image/Audio Tools placeholder
/upload        Alias for Axe 3
/axe4          Interactive Canvas placeholder
/canvas        Alias for Axe 4
/interactivity Alias for Axe 4
/gallery       Gallery page
/axe6          ML Palette placeholder
/ml-palette    Alias for Axe 6
```

## How Team Members Plug In Their Axes

Each teammate can replace the placeholder route/template for their axe:

- Axe 1: update `/axe1` and `app/templates/generative.html`
- Axe 2: update `/axe2` and `app/templates/data_art.html`
- Axe 3: update `/axe3` and `app/templates/upload.html`
- Axe 4: update `/axe4` or `/canvas`
- Axe 6: update `/axe6` or `/ml-palette`

Reusable Python logic should be placed in module folders, for example:

```text
app/modules/generative_art/
app/modules/data_visualization/
app/modules/image_audio_processing/
app/modules/interactivity/
app/modules/ml_tools/
```

## Run Locally

```bash
pip install -r requirements.txt
python app.py
```

Open:

```text
http://127.0.0.1:5000
```
