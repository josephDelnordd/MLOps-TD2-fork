from flask import Flask, request, jsonify
import joblib
import pandas as pd

# Initialize the Flask app
app = Flask(__name__)

def add_combined_feature(X):
    X = X.copy()  # Ensure we're modifying a copy of the DataFrame
    
    # Example feature: combining two features
    X['Combined_radius_texture'] = X['mean radius'] * X['mean texture']
    
    return X

BEST_MODEL = 'best_cancer_model_pipeline.joblib'
# Load the trained model pipeline
model_pipeline = joblib.load(BEST_MODEL)



# Define a route for the home page
@app.route('/')
def home():
    return "Welcome to the Breast Cancer Prediction API!"

# Define a route for making predictions
@app.route('/predict', methods=['POST'])
def predict():
    # Get the JSON data from the request
    data = request.json
    
    # Convert JSON data to a DataFrame
    input_data = pd.DataFrame([data])
    
    # Make predictions using the loaded model
    prediction = model_pipeline.predict(input_data)
    
    # Return the prediction as a JSON response
    return jsonify({'prediction': int(prediction[0])})

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=5002)