from prefect import flow, task
import pandas as pd
import pickle
import tensorflow as tf
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODELS_DIR = os.path.join(BASE_DIR, "..", "models")

# Carrega o modelo
@task
def load_model():
    model_path = os.path.join(MODELS_DIR, "loan_default_risk_detection_ann_v3.h5")
    return tf.keras.models.load_model(model_path)

@task
def load_scaler():
    scaler_path = os.path.join(MODELS_DIR, "model_min_max_scaler.pkl")
    with open(scaler_path, "rb") as f:
        return pickle.load(f)

# Simula os dados (você pode alterar para ler de um CSV, banco, etc)
@task
def get_data():
    return [100000, 33, 4, 3, 0, 0, 1, 1]  # exemplo de dados para 1 cliente

@task
def predict(model, scaler, data):
    scaled = scaler.transform([data])
    result = model.predict(scaled)[0][0]
    prediction = int(result > 0.5)
    return prediction, result

@flow(name="Loan Default Risk Prediction Flow")
def loan_flow():
    model = load_model()
    scaler = load_scaler()
    data = get_data()
    prediction, probability = predict(model, scaler, data)
    print(f"Previsão: {'Inadimplente' if prediction else 'Não Inadimplente'} ({probability*100:.2f}%)")

if __name__ == "__main__":
    loan_flow()