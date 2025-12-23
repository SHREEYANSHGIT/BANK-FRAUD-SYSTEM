import streamlit as st
import pandas as pd
import joblib

# ------------------------------------------------
# Load trained model
# ------------------------------------------------
model = joblib.load("rf_model.joblib")

st.set_page_config(page_title="Fraud Detection System", layout="centered")

st.title("💳 Fraud Detection System")
st.caption("Rule-based validation + ML risk scoring")

# ------------------------------------------------
# HARD FRAUD RULES
# ------------------------------------------------
def hard_fraud_rules(amount, oldOrg, newOrg, oldDest, newDest):
    if amount <= 0:
        return True, "Invalid transaction amount"

    if amount > oldOrg:
        return True, "Amount exceeds available sender balance"

    if abs((oldOrg - newOrg) - amount) > 1e-2:
        return True, "Sender balance change does not match amount"

    if (newDest - oldDest) > 0 and oldOrg == newOrg:
        return True, "Receiver credited without sender debit"

    if (newDest - oldDest) > amount:
        return True, "Receiver credited more than transferred amount"

    if newOrg < 0 or newDest < 0:
        return True, "Negative balance detected"

    return False, None


# ------------------------------------------------
# RISK SCORING RULES
# ------------------------------------------------
def risk_score_rules(amount, oldOrg, tx_type):
    score = 0.0
    reasons = []

    if amount > 400000:
        score += 0.3
        reasons.append("High-value transaction (>50k)")

    if amount > 40000:
        score += 0.3
        reasons.append("High-value transaction (>50k)")

    if amount > 0.9 * oldOrg:
        score += 0.3
        reasons.append("Amount drains >90% of sender balance")

    if (oldOrg - amount) == 0:
        score += 0.2
        reasons.append("Sender balance becomes zero")

    if tx_type == "CASH_OUT" or amount > 40000:
        score += 0.2
        reasons.append("High-risk transaction type (CASH_OUT)")

    return score, reasons


# ------------------------------------------------
# USER INPUT FORM
# ------------------------------------------------
with st.form("transaction_form"):
    st.subheader("🔍 Enter Transaction Details")

    step = st.number_input("Step", min_value=0, value=1)
    amount = st.number_input("Amount", min_value=0.0, step=100.0)

    oldbalanceOrg = st.number_input("Old Balance (Sender)", min_value=0.0)
    newbalanceOrig = st.number_input("New Balance (Sender)", min_value=0.0)

    oldbalanceDest = st.number_input("Old Balance (Receiver)", min_value=0.0)
    newbalanceDest = st.number_input("New Balance (Receiver)", min_value=0.0)

    # 👉 Drag / Dropdown Transaction Type
    tx_type = st.selectbox(
        "Transaction Type",
        ["CASH_OUT", "TRANSFER", "PAYMENT", "DEBIT"]
    )

    submitted = st.form_submit_button("🚀 Check Fraud Risk")


# ------------------------------------------------
# PREDICTION LOGIC
# ------------------------------------------------
if submitted:

    is_fraud, reason = hard_fraud_rules(
        amount,
        oldbalanceOrg,
        newbalanceOrig,
        oldbalanceDest,
        newbalanceDest
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
    rule_risk, rule_reasons = risk_score_rules(amount, oldbalanceOrg, tx_type)

    total_risk = min(ml_score + rule_risk, 1.0)

    # ------------------------------------------------
    # DECISION OUTPUT
    # ------------------------------------------------
    st.subheader("📊 Fraud Decision")

    st.metric("ML Risk Score", f"{ml_score:.3f}")
    st.metric("Rule Risk Score", f"{rule_risk:.3f}")
    st.metric("Total Risk Score", f"{total_risk:.3f}")

    if total_risk < 0.30:
        st.success("✅ NOT FRAUD — Transaction Approved")

    elif total_risk < 0.70:
        st.warning("⚠️ FLAGGED — Manual Review Required")

    else:
        st.error("🚫 FRAUD — BLOCK PAYMENT")

    if rule_reasons:
        st.subheader("🔎 Triggered Risk Rules")
        for r in rule_reasons:
            st.write("•", r)
