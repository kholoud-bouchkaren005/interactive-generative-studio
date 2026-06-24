import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from PIL import Image

# 1. Chargement du modèle (C'est le composant Bonus ML du projet)
print("--- Chargement du modèle Neural Style Transfer... ---")
# Utilisation d'un modèle pré-entraîné de Magenta via TensorFlow Hub pour plus d'efficacité
hub_model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')

def load_img(path_to_img):
    """Fonction pour charger et prétraiter l'image pour le modèle."""
    img = tf.io.read_file(path_to_img)
    # Décodage de l'image en format RGB
    img = tf.image.decode_image(img, channels=3)
    # Conversion des pixels en valeurs flottantes entre 0 et 1
    img = tf.image.convert_image_dtype(img, tf.float32)
    # Ajout d'une dimension supplémentaire (batch dimension) requise par TensorFlow
    img = img[tf.newaxis, :]
    return img

def tensor_to_image(tensor):
    """Fonction pour convertir le tenseur de sortie en image affichable."""
    tensor = tensor * 255
    tensor = np.array(tensor, dtype=np.uint8)
    if np.ndim(tensor) > 3:
        assert tensor.shape[0] == 1
        tensor = tensor[0]
    return Image.fromarray(tensor)

# 2. Chemins vers tes images (Assure-toi que les noms correspondent à ton dossier app/static/)[cite: 1]
content_path = 'app/static/content.jpeg' # L'image de base (ex: ENSA Tanger)[cite: 1]
style_path = 'app/static/Style.jpg'     # L'image de style (ex: Peinture de Kandinsky)[cite: 1]

print("--- Transformation de l'image en cours... ---")
content_image = load_img(content_path)
style_image = load_img(style_path)

# 3. Application du transfert de style[cite: 1]
# Le modèle prend l'image de contenu et l'image de style pour créer une œuvre fusionnée[cite: 1]
stylized_image = hub_model(tf.constant(content_image), tf.constant(style_image))[0]

# 4. Sauvegarde du résultat final
result_image = tensor_to_image(stylized_image)
result_image.save('app/static/artistic_output.jpg')
print("--- Terminé ! Vérifie le fichier 'artistic_output.jpg' dans ton dossier static. ---")