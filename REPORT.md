# Interactive Generative Studio - Project Report

## 1. Concept and Artistic Direction

Interactive Generative Studio is a creative web application built with Flask. The project explores how Python can be used as a digital creativity tool through generative art, artistic data visualization, image manipulation, real-time interaction, and a small machine-learning bonus.

The artistic direction is based on the idea of a modular creative studio. Instead of presenting one isolated artwork, the application offers several creative stations. Each station lets the user interact with a different type of digital creation: generating abstract shapes, transforming data into visual landscapes, editing images, drawing on an interactive canvas, and extracting color palettes from images.

The visual identity of the studio is clean and tool-focused. The interface uses simple panels, clear controls, responsive layouts, and strong color accents. This makes the application usable during a live presentation while still keeping the creative outputs at the center of the experience.

## Team Members and Contributions

- Nihal: Axe 1 - Generative Art, Axe 2 - Data-Driven Creative Visualization.
- Kholoud: Axe 3 - Image Editing, Axe 5 - Web Integration.
- Ghizlane: Axe 4 - Interactivity Module, Axe 6 - ML Color Extraction Bonus.

## 2. Implemented Modules

### Axe 1 - Generative Art

The generative art module creates abstract geometric compositions. Users can choose the number of shapes, maximum shape size, and color palette. The backend generates a PNG image using Pillow.

The implementation uses object-oriented programming. A base `Shape` class is extended by shape types such as `Circle`, `Square`, `Triangle`, and `Line`. Randomness is used to choose positions, sizes, colors, opacity, and shape types. Loops are used to layer many shapes into one final artwork.

Main route:

- `/axe1`
- `/generate`

Main file:

- `app/modules/generative_art/artworks.py`

### Axe 2 - Data-Driven Creative Visualization

The data art module transforms a simulated weather dataset into an artistic landscape. The dataset is created with Pandas and NumPy. It contains values such as temperature, humidity, and wind. These values are combined into a creative index and visualized with Matplotlib.

The output is not a traditional chart. It uses layered waves, colored fills, and scatter points to create an abstract visual rhythm. Users can change the number of dataset days, visual density, and theme.

Main route:

- `/axe2`
- `/generate-data-art`

Main file:

- `app/modules/data_visualization/data_art.py`

### Axe 3 - Image Editing

The image editing module allows users to upload an image and apply creative filters. It uses Pillow for image manipulation. Available effects include grayscale, sepia, neon, inversion, blur, pixelation, contour detection, mirror, and rotation.

The edited image is displayed directly on the page and can be downloaded as a PNG. This module demonstrates media manipulation and file upload integration in Flask.

Main route:

- `/axe3`
- `/apply-image-effect`

Main file:

- `app/modules/image_audio_processing/image_tools.py`

### Axe 4 - Interactivity Module

The interactivity module uses an HTML5 canvas and JavaScript. Users can click or drag on the canvas to add shapes in real time. The interface includes controls for shape type, palette, shape size, burst density, and animation mode.

The module also includes random generation, clear canvas, and PNG download controls. This part focuses on direct user interaction and immediate visual feedback.

Main route:

- `/axe4`
- `/canvas`

Main files:

- `app/templates/canvas.html`
- `app/static/main.js`

### Axe 5 - Web Integration

The Flask integration module connects the whole project into a single web application. It provides the home dashboard, navigation bar, route map, gallery page, and consistent visual layout.

The goal of this axis is to make the project feel like one complete studio instead of disconnected pages. Every module has a clear entry point and is accessible from the main dashboard.

Main file:

- `app.py`

### Axe 6 - Optional ML Bonus: Color Extraction

The bonus machine-learning module extracts dominant colors from an uploaded image using K-means clustering. Users choose the number of colors, upload an image, and receive a palette with HEX values, RGB values, and percentage distribution.

This module connects image processing with a simple ML technique and makes the result useful for creative work, such as selecting palettes for generative art.

Main route:

- `/axe6`
- `/extract-palette`

Main file:

- `app/modules/ml_tools/color_extraction.py`

## 3. Tools Used and Technical Pipeline

The project uses Flask as the main backend framework. Flask handles routing, templates, form submissions, file uploads, and JSON responses. Jinja2 templates are used to render dynamic pages.

Pillow is used for image generation and editing. In Axe 1, it renders geometric artworks as PNG images. In Axe 3, it applies visual filters and transformations to uploaded images.

Pandas and NumPy are used in Axe 2 to create and process a small simulated weather dataset. Matplotlib converts the processed data into an artistic visualization.

JavaScript and the HTML5 Canvas API power Axe 4. The canvas provides real-time drawing and animation directly in the browser. It also supports downloading the final canvas as an image.

scikit-learn is used in Axe 6. The KMeans algorithm clusters image pixels into dominant color groups. The result is returned as a creative color palette.

The general technical pipeline is:

1. User opens a module page from the dashboard.
2. The user adjusts controls or uploads a file.
3. Flask receives the request.
4. A module-specific Python function processes the input.
5. The output is returned as an image, JSON response, or rendered template.
6. The frontend displays the final creative result.

## 4. Challenges and Solutions

One of the first challenges was GitHub collaboration. At the beginning, the team had difficulties with branches, pull requests, merge conflicts, and keeping the same project version on all computers. The solution was to organize the work by axes, create separate branches for each part, and merge the work progressively into the main project after resolving conflicts.

Another important constraint was the difference between local development environments. Some team members installed Python 3.11, while others used Python 3.14. This created dependency and compatibility problems, especially with libraries such as Flask, Pillow, NumPy, Pandas, Matplotlib, and scikit-learn. The solution was to use a shared `requirements.txt` file and a virtual environment so the project could be installed with the same packages on every machine.

The team also used different code editors. Some members worked with Visual Studio Code, while others used PyCharm. This sometimes created different project settings and hidden IDE files. To solve this, the project used `.gitignore` to avoid committing personal IDE folders such as `.idea`, cache files, and virtual environment files.

Keeping the project modular was also a challenge. Since each axis has different requirements, the code was separated into routes, templates, and module folders. This makes it easier to maintain and merge the work of different teammates.

Another technical challenge was displaying generated images without creating many temporary files. The solution was to generate images in memory and encode them as Base64 PNG strings. This allows images to appear directly in the web page and be downloaded by the user.

For the interactive canvas, the challenge was keeping drawing responsive while supporting several controls. The solution was to store shapes in JavaScript objects and redraw them inside an animation loop.

For the ML color extraction, the challenge was making the method simple but meaningful. K-means clustering was chosen because it is understandable, fast enough for small images, and produces useful creative palettes.

The animation module also required performance control. Generating animated GIFs can become slow when the number of frames, particles, and layers is high. To manage this, the interface includes parameters such as duration, FPS, wave layers, and particle count, so the user can balance visual quality and generation time.

Finally, combining all modules into one Flask application required a clean route structure. A central `app.py` file was used to connect all pages, while each module keeps its own processing code in a dedicated folder. This reduced duplicated routes and made the final application easier to present.

## Conclusion

Interactive Generative Studio demonstrates how Python can support creative coding in several forms: generative visuals, artistic data transformation, media editing, real-time interaction, and machine-learning-assisted color design. The result is a modular Flask application that is ready for presentation and future extension.

## Final Deliverables

The final submission includes all required project deliverables:

1. Complete code base

   The full source code is available in the GitHub repository: `https://github.com/kholoud-bouchkaren005/interactive-generative-studio`. It includes the Flask entry point, module files, templates, static assets, README, report, and dependency list.

2. Fully working Flask app

   The application runs with `python app.py` and provides a complete web interface for all implemented axes. Each module is accessible through its own route and connected through the main dashboard.

3. README with installation steps and explanations

   The repository includes a `README.md` file containing setup instructions, dependency installation, run commands, route descriptions, module explanations, project structure, and tools used.

4. Two-to-three page report

   This report covers the required elements:

   - Concept and artistic direction.
   - All implemented modules.
   - Tools used and technical pipeline.
   - Challenges and solutions.
