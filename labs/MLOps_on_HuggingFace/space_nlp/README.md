---
title: Sentiment Analysis
emoji: 🎬
colorFrom: blue
colorTo: indigo
sdk: gradio
app_file: app.py
pinned: false
---

# Sentiment Analysis (DistilBERT)

Interface Gradio pour un modèle DistilBERT fine-tuné sur l'analyse de sentiment
([`rotten_tomatoes`](https://huggingface.co/datasets/rotten_tomatoes)).

Saisissez un texte ; le modèle prédit `POSITIVE` ou `NEGATIVE`.

## Configuration

Éditez `app.py` et remplacez `YOUR_USERNAME/distilbert-sentiment-demo`
par l'identifiant de votre modèle. Pour servir une version promue,
décommentez `REVISION = "production"` et passez `revision=REVISION` au `pipeline`.
