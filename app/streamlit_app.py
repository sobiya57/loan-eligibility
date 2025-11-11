import streamlit as st
import requests

st.set_page_config(
    page_title="Loan Eligibility Predictor",
    page_icon="🏛️",
    layout="centered"
)

# ---------- Glass Card CSS ----------
st.markdown("""
<style>
/* page background */
.stApp {
  background: radial-gradient(1200px 600px at 10% 0%, #e9efff 0%, #f7f8ff 35%, #fafbff 60%, #ffffff 100%);
  background-attachment: fixed;
}

/* subtle animated shimmer at top border */
@keyframes glow {
  0% { box-shadow: 0 -2px 30px rgba(76, 110, 245, .25) inset; }
  50% { box-shadow: 0 -2px 45px rgba(76, 110, 245, .45) inset; }
  100% { box-shadow: 0 -2px 30px rgba(76, 110, 245, .25) inset; }
}
.block-container { padding-top: 2.2rem; animation: glow 6s ease-in-out infinite; }

/* glass card */
.glass {
  background: rgba(255,255,255,.55);
  border-radius: 18px;
  border: 1px solid rgba(255,255,255,.35);
  box-shadow:
    0 10px 30px rgba(16, 24, 40, .08),
    0 1px 0 rgba(255,255,255,.6) inset;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  padding: 22px 22px 8px 22px;
}

/* title */
h1.glass-title{
  text-align:center;
  margin: 0 0 6px 0;
  color:#0f172a;
  letter-spacing: .3px;
}
.subtle {
  text-align:center;
  color:#55607a;
  margin:-2px 0 18px 0;
  font-size:.95rem;
}

/* inputs */
.stSelectbox > div, .stNumberInput > div, .stTextInput > div {
  background: rgba(255,255,255,.65);
  border: 1px solid rgba(15,23,42,.07);
  border-radius: 12px;
}
.stSelectbox:hover > div, .stNumberInput:hover > div, .stTextInput:hover > div{
  border-color: rgba(76,110,245,.35);
}

/* predict button */
div[data-testid="baseButton-secondary"] > button,
div[data-testid="baseButton-primary"] > button,
.stButton > button {
  background: linear-gradient(135deg, #4c6ef5 0%, #7c8dfb 100%);
  border: 0;
  color: white;
  border-radius: 12px;
  padding: 0.6rem 1.1rem;
  font-weight: 600;
  box-shadow: 0 10px 18px rgba(76,110,245,.25);
}
.stButton > button:hover {
  filter: brightness(1.05);
  box-shadow: 0 12px 20px rgba(76,110,245,.32);
}

/* result cards */
.result-ok {
  background: rgba(16,185,129,.10);
  border: 1px solid rgba(16,185,129,.35);
  color: #065f46;
  border-radius: 14px;
  padding: 14px 14px;
}
.result-no {
  background: rgba(239,68,68,.10);
  border: 1px solid rgba(239,68,68,.35);
  color: #7f1d1d;
  border-radius: 14px;
  padding: 14px 14px;
}

/* footer mini */
.footer-note { color:#6b7280; text-align:center; font-size:.85rem; margin-top: 8px;}
</style>
""", unsafe_allow_html=True)

# -------------- Header --------------
st.markdown("<h1 class='glass-title'>🏛️ Loan Eligibility Predictor</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtle'>Premium glass UI • powered by FastAPI + Streamlit</div>", unsafe_allow_html=True)

with st.container():
    st.markdown("<div class='glass'>", unsafe_allow_html=True)

    # -------------- Inputs (same schema you already used) --------------
    col1, col2 = st.columns(2, vertical_alignment="center")
    with col1:
        Gender = st.selectbox("Gender", ["Male", "Female"])
        Dependents = st.selectbox("Dependents", ["0", "1", "2", "3+"])
        Self_Employed = st.selectbox("Self Employed", ["Yes", "No"])
        ApplicantIncome = st.number_input("Applicant Income", min_value=0, step=1, value=0)
        LoanAmount = st.number_input("Loan Amount", min_value=0, step=1, value=0)

    with col2:
        Married = st.selectbox("Married", ["Yes", "No"])
        Education = st.selectbox("Education", ["Graduate", "Not Graduate"])
        Property_Area = st.selectbox("Property Area", ["Urban", "Rural", "Semiurban"])
        CoapplicantIncome = st.number_input("Co-applicant Income", min_value=0, step=1, value=0)
        Loan_Amount_Term = st.number_input("Loan Term (days)", min_value=0, step=1, value=0)

    Credit_History = st.selectbox("Credit History", [1, 0])

    st.write("")  # tiny spacer
    predict = st.button("Predict")

    # -------------- API call --------------
    API_URL = "https://loan-api-z9u8.onrender.com/predict"

    if predict:
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
            "Credit_History": Credit_History,
        }

        try:
            r = requests.post(API_URL, json=payload, timeout=20)
            r.raise_for_status()
            result = r.json()

            if result.get("approved"):
                st.markdown(
                    f"<div class='result-ok'>✅ <b>Loan Approved</b> — "
                    f"Probability: <b>{result.get('probability', 0):.2f}</b></div>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"<div class='result-no'>❌ <b>Loan Not Approved</b> — "
                    f"Probability: <b>{result.get('probability', 0):.2f}</b></div>",
                    unsafe_allow_html=True
                )
        except Exception as e:
            st.markdown(
                f"<div class='result-no'>⚠️ <b>Unable to connect to API</b>. "
                f"Please verify the API is live. <br/><small>{e}</small></div>",
                unsafe_allow_html=True
            )

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='footer-note'>Made with ❤️  •  Glass UI theme</div>", unsafe_allow_html=True)




