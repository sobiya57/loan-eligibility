import streamlit as st
import requests

st.set_page_config(page_title="Loan Eligibility Predictor")

st.title("🏦 Loan Eligibility Predictor")

Gender = st.selectbox("Gender", ["Male", "Female"])
Married = st.selectbox("Married", ["Yes", "No"])
Dependents = st.selectbox("Dependents", ["0", "1", "2", "3+"])
Education = st.selectbox("Education", ["Graduate", "Not Graduate"])
Self_Employed = st.selectbox("Self Employed", ["Yes", "No"])
Property_Area = st.selectbox("Property Area", ["Urban", "Rural", "Semiurban"])
ApplicantIncome = st.number_input("Applicant Income", min_value=0, step=1)
CoapplicantIncome = st.number_input("Co-applicant Income", min_value=0, step=1)
LoanAmount = st.number_input("Loan Amount", min_value=0, step=1)
Loan_Amount_Term = st.number_input("Loan Term (days)", min_value=0, step=1)
Credit_History = st.selectbox("Credit History", [1, 0])

# API URL
API_URL = "http://127.0.0.1:8000/predict"

if st.button("Predict"):
    payload = {
        "Gender": Gender,
        "Married": Married,
        "Dependents": Dependents,
        "Education": Education,
        "Self_Employed": Self_Employed,
        "Property_Area": Property_Area,
        "ApplicantIncome": ApplicantIncome,
        "CoapplicantIncome": CoapplicantIncome,
        "LoanAmount": LoanAmount,
        "Loan_Amount_Term": Loan_Amount_Term,
        "Credit_History": Credit_History
    }

    try:
        response = requests.post(API_URL, json=payload)
        result = response.json()

        if result["approved"]:
            st.success(f"✅ Loan Approved (Probability: {result['probability']:.2f})")
        else:
            st.error(f"❌ Loan Not Approved (Probability: {result['probability']:.2f})")

    except Exception as e:
        st.error("⚠️ Unable to connect to API. Make sure FastAPI is running.")
        st.write(e)


