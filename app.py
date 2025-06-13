import streamlit as st
import  joblib
import pandas as pd
import numpy as np

# load the model
model = joblib.load('final_model.pkl')

data = pd.read_csv('data/bank-full.csv')

# Set page title and header
st.set_page_config(page_title="Bank Term Deposit Subscription Predictor", layout="centered")

st.markdown("""
    <h1 style='text-align: center; color: white;'>🏦 Bank Marketing Predictor App</h1>
    <h3 style='text-align: center; color: grey;'>Will this client subscribe to a term deposit?</h3>
""", unsafe_allow_html=True)

# Input form
with st.form("prediction_form"):
    st.subheader("📋 Client Information")
    
    p1,p2,p3 = st.columns([2,2,2])
    with p1:
        client_age = st.number_input("Client Age", min_value=18, max_value=100)
    with p2:
        marital_status = st.selectbox("Marital Status", ['single', 'married', 'divorced'])
    with p3:
        job_type = st.selectbox("Job Type", ['admin.', 'technician', 'services', 'management', 'retired', 'blue-collar', 'unemployed', 'entrepreneur', 'self-employed', 'housemaid', 'student'])
    
    education_level = st.selectbox("Education Level", ['primary', 'secondary', 'tertiary'])
    

    st.markdown("---")
    p4,p5 = st.columns([2,2])

    with p4:
        has_credit_default = st.selectbox("Credit in Default?", ['yes', 'no'])
    with p5:
        account_balance = st.number_input("Account Balance", min_value=-8019, max_value=100000, value=0, step=100)
    
    p6,p7,p8 = st.columns([2,2,2])
    with p6:
        has_housing_loan = st.selectbox("Housing Loan?", ['yes', 'no'])
    with p7:
        has_personal_loan = st.selectbox("Personal Loan?", ['yes', 'no'])
    with p8:
        contact_type = st.selectbox("Contact Communication Type", ['cellular', 'telephone', 'none'])
    last_contact_day = st.slider("Last Contact Day of Month", 1, 31, 15)
    
    p9,p10 = st.columns([2,2])
    with p9:
        last_contact_month = st.selectbox("Last Contact Month", ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'])
    
    with p10:
        last_contact_duration = st.number_input("Last Contact Duration (seconds)", min_value=0, max_value=5000, value=120)
    campaign_contacts = st.slider("Number of Contacts During Campaign", 1, 50, 2)
    days_since_last_contact = st.slider("Days Since Last Contact", -1, 871, 100)
    previous_contacts = st.slider("Number of Contacts Before This Campaign", 0, 275, 10)
    previous_outcome = st.selectbox("Previous Campaign Outcome", ['success', 'failure', 'other', 'none'])

    submitted = st.form_submit_button("🔍 Predict",use_container_width=True)

# When form is submitted
if submitted:
    input_data = pd.DataFrame([{
        'client_age': client_age,
        'job_type': job_type,
        'marital_status': marital_status,
        'education_level': education_level,
        'has_credit_default': has_credit_default,
        'account_balance': account_balance,
        'has_housing_loan': has_housing_loan,
        'has_personal_loan': has_personal_loan,
        'contact_type': contact_type,
        'last_contact_day': last_contact_day,
        'last_contact_month': last_contact_month,
        'last_contact_duration': last_contact_duration,
        'campaign_contacts': campaign_contacts,
        'days_since_last_contact': days_since_last_contact,
        'previous_contacts': previous_contacts,
        'previous_outcome': previous_outcome
    }])

    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]

    if prediction == 1:
        st.success(f"✅ The client is **likely to subscribe**. Probability: {round(probability*100, 2)}%")
        st.balloons()
    else:
        st.warning(f"❌ The client is **not likely to subscribe**. Probability: {round(probability*100, 2)}%")
        st.snow()