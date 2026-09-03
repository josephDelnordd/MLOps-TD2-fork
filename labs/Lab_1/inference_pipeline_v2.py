from flask import Flask, request, jsonify
import pandas as pd
import joblib

def add_new_features(X):

    X = X.copy()

    X["radius_area_ratio"] = (
        X["mean radius"]
        /
        (X["mean area"] + 1)
    )

    X["worst_mean_radius_diff"] = (
        X["worst radius"]
        -
        X["mean radius"]
    )

    return X

# Initialisation de l'application Flask
app = Flask(__name__)

# Chargement du modèle entraîné
MODEL_PATH = "best_cancer_model_v2.joblib"
model = joblib.load(MODEL_PATH)

# Colonnes du dataset Breast Cancer
feature_names = [
    'mean radius',
    'mean texture',
    'mean perimeter',
    'mean area',
    'mean smoothness',
    'mean compactness',
    'mean concavity',
    'mean concave points',
    'mean symmetry',
    'mean fractal dimension',
    'radius error',
    'texture error',
    'perimeter error',
    'area error',
    'smoothness error',
    'compactness error',
    'concavity error',
    'concave points error',
    'symmetry error',
    'fractal dimension error',
    'worst radius',
    'worst texture',
    'worst perimeter',
    'worst area',
    'worst smoothness',
    'worst compactness',
    'worst concavity',
    'worst concave points',
    'worst symmetry',
    'worst fractal dimension'
]

@app.route("/")
def home():
    return "Breast Cancer Prediction API V2"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json

        features = data["features"]

        input_df = pd.DataFrame(
            [features],
            columns=feature_names
        )

        prediction = model.predict(input_df)

        return jsonify({
            "prediction": int(prediction[0])
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5003,
        debug=True
    )