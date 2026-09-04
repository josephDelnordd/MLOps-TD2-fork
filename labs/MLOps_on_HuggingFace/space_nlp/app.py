"""
Space Gradio — Analyse de sentiment (DistilBERT fine-tuné).

Avant de déployer :
  1. Remplacez MODEL_ID par l'identifiant de VOTRE modèle publié
     (ex. "alimokh/distilbert-sentiment-demo").
     Astuce : pour servir une version promue, utilisez revision="production".
  2. Poussez ce fichier + requirements.txt dans un Space (SDK: Gradio).
"""
import gradio as gr
from transformers import pipeline

# 👉 À REMPLACER par votre propre repo (username/nom-du-modele)
MODEL_ID = "DELNORD/distilbert-sentiment-demo"
REVISION = "production"  # décommentez pour servir la version promue

classifier = pipeline("sentiment-analysis", model=MODEL_ID, truncation=True, revision=REVISION)


def predict(text):
    if not text or not text.strip():
        return {}
    preds = classifier(text, top_k=None)  # renvoie tous les labels avec scores
    return {p["label"]: float(p["score"]) for p in preds}


demo = gr.Interface(
    fn=predict,
    inputs=gr.Textbox(lines=4, label="Votre texte (critique, avis...)",
                      placeholder="This movie was absolutely fantastic!"),
    outputs=gr.Label(num_top_classes=2, label="Sentiment"),
    title="🎬 Sentiment Analysis (DistilBERT)",
    description=(
        "Modèle DistilBERT fine-tuné pour l'analyse de sentiment. "
        "Saisissez un texte : le modèle prédit POSITIVE ou NEGATIVE."
    ),
    examples=[
        ["This movie was absolutely fantastic, a real masterpiece!"],
        ["A total waste of time, I fell asleep halfway through."],
    ],
)

if __name__ == "__main__":
    demo.launch()
