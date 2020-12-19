#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
from sklearn.preprocessing import PolynomialFeatures

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    
    init_features = [str(x) for x in request.form.values()]
    init_features = list(init_features)
    init_features[0] = float(init_features[0])
    init_features[1] = float(init_features[1])
    init_features[2] = float(init_features[2])
    init_features[5] = float(init_features[5])
    
    if init_features[3] == 'N' or init_features[3] == 'S':
        init_features[3] = 1
    elif init_features[3] == 'E' or init_features[3] == 'W':
        init_features[3] = 2
    elif init_features[3] == 'ENE' or init_features[3] == 'VAR' or init_features[3] == 'WSW' or init_features[3] == 'WNW' or init_features[3] == 'ESE':
        init_features[3] = 2.5
    elif init_features[3] == 'SSW' or init_features[3] == 'SSE' or init_features[3] == 'NNW' or init_features[3] == 'NNE':
        init_features[3] = 3
    elif init_features[3] == 'NE' or init_features[3] == 'SW' or init_features[3] == 'NW' or init_features[3] == 'SE':
        init_features[3] = 3.5
    else:
        init_features[3] = 0
        
    if init_features[4] == 'Fair' or init_features[4] == 'Fair / Windy':
        init_features[4] = 1
    elif init_features[4] == 'Haze' or init_features[4] == 'Mist':
        init_features[4] = 1.5
    elif init_features[4] == 'Partly Cloudy' or init_features[4] == 'Light Rain' or init_features[4] == 'Partly Cloudy / Windy':
        init_features[4] = 2
    elif init_features[4] == 'Thunder in the Vicinity' or init_features[4] == 'Light Rain with Thunder':
        init_features[4] = 2.5
    elif init_features[4] == 'Mostly Cloudy' or init_features[4] == 'Mostly Cloudy / Windy':
        init_features[4] = 3
    elif init_features[4] == 'Thunder':
        init_features[4] = 3.5
    elif init_features[4] == 'Cloudy' or init_features[4] == 'T-Storm' or init_features[4] == 'Cloudy / Windy':
        init_features[4] = 4
    else:
        init_features[4] = 4.5
        
    temp = init_features[2]
    init_features[2] = init_features[3]
    init_features[3] = temp
        
    final_features = [np.array(init_features)]
    polynomial_features = PolynomialFeatures(degree=2)
    prediction = model.predict(polynomial_features.fit_transform(final_features))
    
    output = round(prediction[0], 2)
    
    return render_template('index.html', prediction_text='Internal Greenhouse Temperature In 1 Hour Prediction: {}'.format(output))

if __name__ == "__main__":
    app.run(debug=True)

