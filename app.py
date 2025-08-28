from flask import Flask, render_template, request
import os
import numpy as np
import pandas as pd
from src.datascienceproject.pipeline.pipeline_prediction import PredictionPipeline

app = Flask(__name__)

@app.route('/', methods=['GET',]) ## route to display the home page
def homepage():
    return render_template('index.html')

@app.route('/train', methods=['GET']) ## route to train the pipeline
def training():
    os.system('python main.py')
    return 'Training completed!'

@app.route('/predict', methods=['POST', 'GET']) ## route from the web ui
def index():
    if request.method == 'POST':
        try:
            fixed_acidity = float(request.form['fixed_acidity'])
            volatile_acidity = float(request.form['volatile_acidity'])
            citric_acid = float(request.form['citric_acid'])
            residual_sugar = float(request.form['residual_sugar'])
            chlorides = float(request.form['chlorides'])
            free_sulfur_dioxide = float(request.form['free_sulfur_dioxide'])
            total_sulfur_dioxide = float(request.form['total_sulfur_dioxide'])
            density = float(request.form['density'])
            ph = float(request.form['pH'])
            sulphates = float(request.form['sulphates'])
            alcohol = float(request.form['alcohol'])

            # Create a DataFrame for the input features
            data=[fixed_acidity, volatile_acidity, citric_acid, residual_sugar, chlorides, free_sulfur_dioxide, total_sulfur_dioxide, density, ph, sulphates, alcohol]

            data = np.array(data).reshape(1, 11)
            obj = PredictionPipeline()
            predict = obj.prediction(data)

            return render_template('results.html', prediction=str(predict))

        except Exception as e:
            return "Something is wrong!!!!"
        
    else:
        return render_template('index.html')
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)