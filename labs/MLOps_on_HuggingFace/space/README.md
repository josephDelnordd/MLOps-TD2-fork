---
title: Bean Leaf Classifier
emoji: 🌱
colorFrom: green
colorTo: yellow
sdk: gradio
app_file: app.py
pinned: false
---

# Bean Leaf Classifier (ViT)

Interface Gradio pour un Vision Transformer fine-tuné sur le dataset [`beans`](https://huggingface.co/datasets/beans).

Déposez une image de feuille de haricot ; le modèle prédit l'une des trois classes :
`angular_leaf_spot`, `bean_rust`, `healthy`.

## Configuration

Avant de lancer, éditez `app.py` et remplacez `YOUR_USERNAME/vit-beans-demo`
par l'identifiant de votre modèle publié sur le Hub.

> `sdk_version` est volontairement omis : le Space utilisera la dernière version de Gradio.
> Pour figer une version, ajoutez `sdk_version: "x.y.z"` dans l'en-tête YAML ci-dessus.
