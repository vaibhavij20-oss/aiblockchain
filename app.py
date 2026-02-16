import streamlit as st
import pandas as pd
import joblib
from blockchain import Blockchain

# Load model and feature columns
model = joblib.load("model.pkl")
feature_columns = joblib.load("feature_columns.pkl")

# Initialize blockchain
blockchain = Blockchain()

st.title("AI-Based Risk Assessment with Blockchain Case Management")

st.header("Enter Case Details")

gender = st.selectbox("Gender", ["Female", "Male", "Transgender/NonConforming", "Unknown"])
ageBroad = st.selectbox("Age Group", ["0-8", "9-17", "18-23", "24-30", "31-38", "39-47", "48+", "Unknown"])
citizenship = st.text_input("Citizenship")

debtBondage = st.checkbox("Debt Bondage")
threats = st.checkbox("Threats")
psych_abuse = st.checkbox("Psychological Abuse")
physical_abuse = st.checkbox("Physical Abuse")
sexual_abuse = st.checkbox("Sexual Abuse")
documents = st.checkbox("Withholds Documents")
movement = st.checkbox("Restricts Movement")
working_hours = st.checkbox("Excessive Working Hours")
recruit_friend = st.checkbox("Recruiter: Friend")
recruit_family = st.checkbox("Recruiter: Family")
recruit_other = st.checkbox("Recruiter: Other")

if st.button("Assess Risk"):

    input_dict = {
        "gender": gender,
        "ageBroad": ageBroad,
        "citizenship": citizenship,
        "meansOfControlDebtBondage": int(debtBondage),
        "meansOfControlThreats": int(threats),
        "meansOfControlPsychologicalAbuse": int(psych_abuse),
        "meansOfControlPhysicalAbuse": int(physical_abuse),
        "meansOfControlSexualAbuse": int(sexual_abuse),
        "meansOfControlWithholdsDocuments": int(documents),
        "meansOfControlRestrictsMovement": int(movement),
        "meansOfControlExcessiveWorkingHours": int(working_hours),
        "recruiterRelationFriend": int(recruit_friend),
        "recruiterRelationFamily": int(recruit_family),
        "recruiterRelationOther": int(recruit_other)
    }

    input_df = pd.DataFrame([input_dict])
    input_df = pd.get_dummies(input_df)
    input_df = input_df.reindex(columns=feature_columns, fill_value=0)

    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0][1]

    st.subheader("Risk Assessment Result")
    st.write("Risk Score:", round(probability, 3))
    st.write("Prediction:", "High Risk" if prediction == 1 else "Low Risk")

    case_data = {
        "gender": gender,
        "ageBroad": ageBroad,
        "citizenship": citizenship,
        "risk_score": float(probability),
        "prediction": "High" if prediction == 1 else "Low"
    }

    blockchain.add_block(case_data)
    st.success("Case added to blockchain ledger.")

st.header("Blockchain Ledger")

if st.button("Validate Blockchain"):
    if blockchain.validate_chain():
        st.success("Blockchain is valid.")
    else:
        st.error("Blockchain integrity compromised!")

for block in blockchain.chain:
    st.json({
        "Index": block.index,
        "Timestamp": block.timestamp,
        "Data": block.data,
        "Hash": block.hash
    })
