import pickle
import numpy as np

from flask import Flask, request, jsonify

def predict_single(customer, dv, model):
    X = dv.transform([customer])
    y_pred = model.predict_proba(X)[:, 1]
    return y_pred[0]

# open DV
with open('churn-dv.bin', 'rb') as f_in:
    dv = pickle.load(f_in)

# open Model
with open('churn-model1.bin', 'rb') as f_in:
    model = pickle.load(f_in)

app = Flask('churn-flask')


@app.route('/predict', methods=['POST'])
def predict():
    customer = request.get_json()

    prediction = predict_single(customer, dv, model)
    churn = prediction >= 0.5
    
    result = {
        'churn_probability': float(prediction),
        'churn': bool(churn),
    }

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=9696)