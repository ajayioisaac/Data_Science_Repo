import streamlit as st
import pandas as pd
import joblib
from sklearn.preprocessing import OneHotEncoder
import numpy as np
import os

# Load your trained model
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'financial_inclusion_model.pkl')
model = joblib.load(MODEL_PATH)

st.title("Financial Inclusion Prediction Tool")
st.write("This application predicts whether an individual has a bank account based on demographic and socioeconomic factors.")

# Create input fields for all features
with st.form("user_inputs"):
    st.header("Personal Information")
    
    # Basic information
    age = st.number_input("Age", min_value=15, max_value=100, value=30)
    gender = st.selectbox("Gender", ["Male", "Female"])
    household_size = st.number_input("Household Size", min_value=1, max_value=20, value=4)
    
    st.header("Location and Technology")
    location_type = st.selectbox("Location Type", ["Urban", "Rural"])
    cellphone_access = st.selectbox("Cellphone Access", ["Yes", "No"])
    
    st.header("Family Information")
    relationship_with_head = st.selectbox(
        "Relationship with Household Head",
        ["Head of Household", "Spouse", "Child", "Parent", "Other relative", "Other non-relatives"]
    )
    marital_status = st.selectbox(
        "Marital Status",
        ["Single/Never Married", "Married/Living together", "Divorced/Seperated", "Widowed", "Dont know"]
    )
    
    st.header("Education and Employment")
    education_level = st.selectbox(
        "Education Level",
        ["No formal education", "Primary education", "Secondary education", 
         "Vocational/Specialised training", "Tertiary education", "Other/Dont know/RTA"]
    )
    job_type = st.selectbox(
        "Job Type",
        ["Formally employed Government", "Formally employed Private", "Informally employed", 
         "Farming and Fishing", "Remittance Dependent", "Self employed", 
         "Government Dependent", "Other Income", "Dont Know/Refuse to answer"]
    )
    
    # Country selection (even though your data is only Kenya, the model expects these features)
    country = st.selectbox("Country", ["Kenya", "Rwanda", "Tanzania", "Uganda"])
    
    # Submit button
    submitted = st.form_submit_button("Predict Financial Inclusion")

if submitted:
    # Create a dataframe with the user inputs
    input_data = pd.DataFrame({
        'country': [country],
        'location_type': [location_type],
        'cellphone_access': [cellphone_access],
        'household_size': [household_size],
        'age_of_respondent': [age],
        'gender_of_respondent': [gender],
        'relationship_with_head': [relationship_with_head],
        'marital_status': [marital_status],
        'education_level': [education_level],
        'job_type': [job_type]
    })
    
    # One-hot encode categorical variables to match model's training data
    # This should match exactly how you preprocessed during training
    categorical_cols = ['country', 'location_type', 'cellphone_access', 'gender_of_respondent',
                      'relationship_with_head', 'marital_status', 'education_level', 'job_type']
    
    # Create dummy variables (one-hot encoding)
    input_processed = pd.get_dummies(input_data, columns=categorical_cols)
    
    # Ensure all expected columns are present (add missing with 0)
    # Get the feature names the model expects
    expected_features = model.feature_names_in_
    
    # Add missing columns with 0
    for feature in expected_features:
        if feature not in input_processed.columns:
            input_processed[feature] = 0
    
    # Reorder columns to match training data
    input_processed = input_processed[expected_features]
    
    # Make prediction
    prediction = model.predict(input_processed)
    probability = model.predict_proba(input_processed)[0][1]
    
    st.subheader("Prediction Result")
    if prediction[0] == "Yes":
        st.success(f"The model predicts this individual HAS a bank account (probability: {probability:.2%})")
    else:
        st.error(f"The model predicts this individual DOES NOT have a bank account (probability: {1-probability:.2%})")
    
    # Show the input data for verification
    st.subheader("Input Summary")
    st.write(input_data.T)