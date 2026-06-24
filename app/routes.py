from flask import render_template, request, jsonify
from app import app
import os

# Importation de la fonction depuis ton nouveau module
try:
    from app.modules.ml_tools.style_transfer import apply_style
except ImportError:
    print("Warning: style_transfer module not found")
    apply_style = None

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/generative")
def generative():
    return render_template("generative.html")

@app.route("/interactivity")
def interactivity():
    return render_template("generative.html")

@app.route("/data-art")
def data_art():
    return render_template("data_art.html")

@app.route("/gallery")
def gallery():
    return render_template("gallery.html")

@app.route("/upload")
def upload():
    return render_template("upload.html")

@app.route("/style-transfer", methods=["POST"])
def style_transfer():
    """Applique un transfert de style à une image"""
    if apply_style is None:
        return jsonify({"error": "Style transfer module not available"}), 500
    
    try:
        # Récupérer les fichiers uploadés
        if 'content' not in request.files or 'style' not in request.files:
            return jsonify({"error": "Missing files"}), 400
        
        content_file = request.files['content']
        style_file = request.files['style']
        
        if content_file.filename == '' or style_file.filename == '':
            return jsonify({"error": "No files selected"}), 400
        
        # Chemins pour sauvegarder les fichiers
        static_dir = os.path.join(app.root_path, 'static')
        content_path = os.path.join(static_dir, 'content_temp.jpg')
        style_path = os.path.join(static_dir, 'style_temp.jpg')
        output_path = os.path.join(static_dir, 'artistic_output.jpg')
        
        # Sauvegarder les fichiers uploadés
        content_file.save(content_path)
        style_file.save(style_path)
        
        # Appliquer le transfert de style
        apply_style(content_path, style_path, output_path)
        
        return jsonify({
            "success": True,
            "message": "La transformation est terminée !",
            "output": "artistic_output.jpg"
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
