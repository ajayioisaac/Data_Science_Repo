# Streamlit_app_1.py

import streamlit as st
import joblib
import numpy as np
import pandas as pd

# Load saved model and metadata
model = joblib.load("expresso_churn_model.pkl")
features = joblib.load("expresso_model_features.pkl")
encoders = joblib.load("expresso_label_encoders.pkl")

# Define categorical features (from your dataset)
categorical_features = list(encoders.keys())

# Streamlit setup
st.set_page_config(page_title="Expresso Churn Predictor", layout="centered")
st.title("📱 Expresso Customer Churn Prediction")
st.markdown("Fill out the form below with customer details:")

# Input collection
user_inputs = []

for feature in features:
    if feature in categorical_features:
        # Provide dropdowns using encoder classes
        options = encoders[feature].classes_.tolist()
        selected = st.selectbox(f"{feature}", options)
        encoded_value = encoders[feature].transform([selected])[0]
        user_inputs.append(encoded_value)
    else:
        val = st.number_input(f"{feature}", step=1.0)
        user_inputs.append(val)

# Predict
if st.button("Predict"):
    input_array = np.array(user_inputs).reshape(1, -1)
    prediction = model.predict(input_array)[0]

    if prediction == 1:
        st.error("⚠️ This customer is likely to CHURN.")
    else:
        st.success("✅ This customer is likely to STAY.")
