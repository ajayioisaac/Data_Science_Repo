# app.py

import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Load the model
model = pickle.load(open('finalized_model.pkl', 'rb'))

# Load and prepare the dataset
dataset_path = 'Sensor.csv'  # Replace with actual path
dataset = pd.read_csv(dataset_path)
dataset.rename(columns={
    'Air temperature [K]': 'Air temperature',
    'Process temperature [K]': 'Process temperature',
    'Rotational speed [rpm]': 'Rotational speed',
    'Torque [Nm]': 'Torque',
    'Tool wear [min]': 'Tool wear'
}, inplace=True)
dataset['Power'] = dataset['Rotational speed'] * dataset['Torque']

# Z-score normalization
def z_score(feature, value):
    mean = np.mean(dataset[feature])
    std = np.std(dataset[feature])
    return (float(value) - mean) / std

# Streamlit UI
st.set_page_config(page_title="Machine Failure Prediction", layout="centered")
st.title("Zico's Machine Failure Prediction App")

st.markdown("Enter the machine parameters below to check if maintenance is needed. The torque is the most consequential parameter for the prediction.")

# Input fields
air_temp = st.slider("Air temperature (K)", 100, 350, 298)
proc_temp = st.slider("Process temperature (K)", 100, 350, 305)
speed = st.number_input("Rotational speed (rpm)", min_value=0, value=1500)
torque = st.number_input("Torque (Nm)", min_value=0.0, value=40.0)
wear = st.number_input("Tool wear (min)", min_value=0, value=100)
machine_type = st.radio("Type", ["L", "M", "H"])

# Prediction logic
if st.button("Predict Failure"):
    air_z = z_score('Air temperature', air_temp)
    proc_z = z_score('Process temperature', proc_temp)
    speed_z = z_score('Rotational speed', speed)
    torque_z = z_score('Torque', torque)
    wear_z = z_score('Tool wear', wear)
    power_z = z_score('Power', torque * speed)

    type_map = {'L': 0, 'M': 1, 'H': 2}
    input_df = pd.DataFrame([{
        'Type': type_map[machine_type],
        'Air temperature': air_z,
        'Process temperature': proc_z,
        'Rotational speed': speed_z,
        'Torque': torque_z,
        'Tool wear': wear_z,
        'Power': power_z
    }])

    prob = model.predict_proba(input_df)[0]
    pred = model.predict(input_df)[0]

    st.subheader("Prediction Result")
    st.write({ "No Failure": prob[0], "Machine Failure": prob[1] })

    if pred == 1:
        st.error("Machine likely to fail! Maintenance required.")
    else:
        st.success("Machine is operating normally.")

