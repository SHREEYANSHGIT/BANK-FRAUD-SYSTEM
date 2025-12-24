import streamlit as st
import pandas as pd
import joblib
import os

# ------------------------------------------------
# Load trained model
# ------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "rf_model.joblib")
model = joblib.load(MODEL_PATH)

st.set_page_config(page_title="Fraud Detection System", layout="centered")

st.title("💳 Fraud Detection System")
st.caption("Rule-based validation + ML risk scoring")
st.caption("Developed by Shreeyansh Asati")

# ------------------------------------------------
# HARD FRAUD RULES
# ------------------------------------------------
def hard_fraud_rules(amount, oldOrg, newOrg, oldDest, newDest, tx_type):

    if amount <= 0:
        return True, "Invalid transaction amount"

    if amount > oldOrg:
        return True, "Amount exceeds sender balance"

    if abs((oldOrg - newOrg) - amount) > 1e-2:
        return True, "Sender balance change mismatch"

    if tx_type != "CASH_OUT":
        if oldDest <= 0:
            return True, "Receiver old balance missing or zero"
        if (newDest - oldDest) != amount:
            return True, "Receiver balance not credited correctly"

    if newOrg < 0 or newDest < 0:
        return True, "Negative balance detected"

    return False, None


# ------------------------------------------------
# RISK SCORE RULES (UPDATED)
# ------------------------------------------------
def risk_score_rules(amount, oldOrg, newOrg, tx_type):
    score = 0.0
    reasons = []

    
    if amount >= 400000:
        score += 0.3
        reasons.append("Very high-value transaction over 10 lakhs ")
        
    if amount >= 1000000:
        score += 0.1
        reasons.append("Very high-value transaction over 4 lakhs")

    if amount > 0.9 * oldOrg:
        score += 0.3
        reasons.append("Drains more than 90% balance")

    # 🔥 NEW RULE: Sender balance becomes zero
    if newOrg == 0:
        score += 0.3
        reasons.append("Sender balance suddenly became zero")

    if tx_type == "CASH_OUT":
        score += 0.2
        reasons.append("High-risk CASH_OUT transaction")

    return score, reasons


# ------------------------------------------------
# INPUT VALIDATION
# ------------------------------------------------
def validate_inputs(tx_type, oldDest, newDest):

    if tx_type == "CASH_OUT":
        return []

    errors = []
    if oldDest <= 0:
        errors.append("Receiver old balance is 0")

    if newDest <= 0:
        errors.append("Receiver new balance is 0")

    return errors


# ------------------------------------------------
# USER FORM
# ------------------------------------------------
with st.form("transaction_form"):
    st.subheader("🔍 Enter Transaction Details")

    tx_type = st.selectbox(
        "Transaction Type",
        ["CASH_OUT", "TRANSFER", "PAYMENT", "DEBIT"]
    )

    if tx_type == "CASH_OUT":
        st.info("ℹ️ CASH_OUT selected → Receiver balances NOT required")

    step = st.number_input("Step", min_value=1, value=1)
    amount = st.number_input("Amount", min_value=0.01)

    oldbalanceOrg = st.number_input("Old Balance (Sender)", min_value=0.01)
    newbalanceOrig = st.number_input("New Balance (Sender)", min_value=0.0)

    oldbalanceDest = st.number_input("Old Balance (Receiver)", min_value=0.0)
    newbalanceDest = st.number_input("New Balance (Receiver)", min_value=0.0)

    submitted = st.form_submit_button("🚀 Check Fraud Risk")


# ------------------------------------------------
# PREDICTION LOGIC
# ------------------------------------------------
if submitted:

    if tx_type == "CASH_OUT":
        oldbalanceDest = 0
        newbalanceDest = 0

    validation_errors = validate_inputs(
        tx_type,
        oldbalanceDest,
        newbalanceDest
    )

    if validation_errors:
        st.error("🚫 FRAUD — BLOCK PAYMENT")
        for err in validation_errors:
            st.write("•", err)
        st.stop()

    is_fraud, reason = hard_fraud_rules(
        amount,
        oldbalanceOrg,
        newbalanceOrig,
        oldbalanceDest,
        newbalanceDest,
        tx_type
    )

    if is_fraud:
        st.error("🚫 FRAUD — BLOCK PAYMENT")
        st.write("**Reason:**", reason)
        st.stop()

    # Feature engineering
    balance_diff_orig = oldbalanceOrg - newbalanceOrig
    balance_diff_dest = oldbalanceDest - newbalanceDest

    data = {
        "step": step,
        "amount": amount,
        "oldbalanceOrg": oldbalanceOrg,
        "newbalanceOrig": newbalanceOrig,
        "oldbalanceDest": oldbalanceDest,
        "newbalanceDest": newbalanceDest,
        "balance_diff_orig": balance_diff_orig,
        "balance_diff_dest": balance_diff_dest,
        "type": tx_type
    }

    df = pd.DataFrame([data])
    df = pd.get_dummies(df, columns=["type"], drop_first=True)
    df = df.reindex(columns=model.feature_names_in_, fill_value=0)

    ml_score = model.predict_proba(df)[0][1]
    rule_risk, rule_reasons = risk_score_rules(
        amount,
        oldbalanceOrg,
        newbalanceOrig,
        tx_type
    )

    total_risk = min(ml_score + rule_risk, 1.0)

    # ------------------------------------------------
    # OUTPUT
    # ------------------------------------------------
    st.subheader("📊 Fraud Decision")

    st.metric("ML Risk Score", f"{ml_score:.3f}")
    st.metric("Rule Risk Score", f"{rule_risk:.3f}")
    st.metric("Total Risk Score", f"{total_risk:.3f}")

    if total_risk < 0.30:
        st.success("✅ NOT FRAUD — Transaction Approved")
    elif total_risk < 0.70:
        st.warning("⚠️ FLAGGED — Manual Review Required")
    elif total_risk < 0.80:
        st.warning("⚠️⚠️ HIGH CHANCE OF FRAUD - Manual Review mandatory")
    else:
        st.error("🚫 FRAUD — BLOCK PAYMENT")

    if rule_reasons:
        st.subheader("🔎 Triggered Risk Rules")
        for r in rule_reasons:
            st.write("•", r)


# ------------------------------------------------
# FOOTER
# ------------------------------------------------
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        bottom: 0;
        width: 100%;
        text-align: center;
        font-size: 18px;
        color: gray;
    }
    </style>
    <div class="footer">
        © 2025 | Built by <b>Shreeyansh Asati</b> | Hybrid Fraud Detection System
    </div>
    """,
    unsafe_allow_html=True
)
