"""
Space Gradio — Classificateur de feuilles de haricot (ViT fine-tuné).

Avant de déployer :
  1. Remplacez MODEL_ID par l'identifiant de VOTRE modèle publié sur le Hub
     (ex. "alimokh/vit-beans-demo").
  2. Poussez ce fichier + requirements.txt dans un Space (SDK: Gradio).
"""
import gradio as gr
from transformers import pipeline

# 👉 À REMPLACER par votre propre repo (username/nom-du-modele)
MODEL_ID = "YOUR_USERNAME/vit-beans-demo"

classifier = pipeline("image-classification", model=MODEL_ID)


def predict(image):
    if image is None:
        return {}
    preds = classifier(image)
    # Gradio gr.Label attend un dict {label: score}
    return {p["label"]: float(p["score"]) for p in preds}


demo = gr.Interface(
    fn=predict,
    inputs=gr.Image(type="pil", label="Image de feuille de haricot"),
    outputs=gr.Label(num_top_classes=3, label="Prédiction"),
    title="🌱 Bean Leaf Classifier (ViT)",
    description=(
        "Modèle Vision Transformer fine-tuné sur le dataset `beans`. "
        "Déposez une image de feuille : angular_leaf_spot, bean_rust ou healthy."
    ),
    examples=None,  # vous pouvez ajouter des chemins d'images d'exemple ici
)

if __name__ == "__main__":
    demo.launch()
