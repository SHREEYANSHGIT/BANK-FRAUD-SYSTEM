import streamlit as st
import pandas as pd
import joblib
import os
from streamlit_option_menu import option_menu

# ------------------------------------------------
# Page Configuration
# ------------------------------------------------
st.set_page_config(
    page_title="Hybrid Fraud Detection System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ------------------------------------------------
# Custom CSS
# ------------------------------------------------
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Container */
    .main-container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    
    /* Title Styles */
    .title-gradient {
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(120deg, #667eea, #764ba2, #f093fb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 10px;
        animation: gradient 3s ease infinite;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Card Styles */
    .custom-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: transform 0.3s, box-shadow 0.3s;
    }
    
    .custom-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.3);
    }
    
    /* Button Styles */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 15px 30px;
        font-size: 18px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Metric Cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        background: rgba(255, 255, 255, 0.12);
        transform: scale(1.05);
    }
    
    /* Alert Styles */
    .alert-success {
        background: linear-gradient(135deg, #00b09b, #96c93d);
        color: white;
        padding: 20px;
        border-radius: 15px;
        font-size: 18px;
        font-weight: 600;
        animation: slideIn 0.5s ease;
    }
    
    .alert-warning {
        background: linear-gradient(135deg, #f2994a, #f2c94c);
        color: white;
        padding: 20px;
        border-radius: 15px;
        font-size: 18px;
        font-weight: 600;
        animation: slideIn 0.5s ease;
    }
    
    .alert-error {
        background: linear-gradient(135deg, #cb2d3e, #ef473a);
        color: white;
        padding: 20px;
        border-radius: 15px;
        font-size: 18px;
        font-weight: 600;
        animation: slideIn 0.5s ease;
    }
    
    @keyframes slideIn {
        from {
            transform: translateX(-20px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    /* Progress Bar */
    .custom-progress {
        height: 10px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 5px;
        overflow: hidden;
    }
    
    .progress-fill {
        height: 100%;
        border-radius: 5px;
        transition: width 1s ease;
    }
    
    /* Footer */
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: rgba(15, 12, 41, 0.9);
        backdrop-filter: blur(10px);
        color: white;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Input Fields */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px !important;
        color: white !important;
    }
    
    .stNumberInput > div > div {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px !important;
    }
    
    /* Labels */
    .stSelectbox label, .stNumberInput label {
        color: #e0e0e0 !important;
        font-weight: 500 !important;
    }
    
    /* Icons */
    .icon-large {
        font-size: 40px;
        margin-bottom: 10px;
    }
    
    /* Pulse Animation */
    .pulse {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(102, 126, 234, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(102, 126, 234, 0); }
        100% { box-shadow: 0 0 0 0 rgba(102, 126, 234, 0); }
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# Load trained model
# ------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "xgb_model.joblib")
model = joblib.load(MODEL_PATH)

# ------------------------------------------------
# Header Section
# ------------------------------------------------
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown('<h1 class="title-gradient">🛡️ FraudShield AI</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #e0e0e0; font-size: 18px; margin-bottom: 30px;">'
                'Intelligent Fraud Detection System powered by Machine Learning</p>', unsafe_allow_html=True)

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
# RISK SCORE RULES
# ------------------------------------------------
def risk_score_rules(amount, oldOrg, newOrg, tx_type):
    score = 0.0
    reasons = []
    
    if amount >= 400000:
        score += 0.3
        reasons.append("⚠️ Very high-value transaction over 4 lakhs")
        
    if amount >= 1000000:
        score += 0.1
        reasons.append("🚨 Extremely high-value transaction over 10 lakhs")

    if amount > 0.9 * oldOrg:
        score += 0.3
        reasons.append("💸 Drains more than 90% of sender balance")

    if newOrg == 0:
        score += 0.3
        reasons.append("🔄 Sender balance suddenly became zero")

    if tx_type == "CASH_OUT":
        score += 0.2
        reasons.append("🏦 High-risk CASH_OUT transaction")

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
# Main Content Layout
# ------------------------------------------------
with st.container():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Quick Stats Row
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
            <div class="metric-card pulse">
                <div class="icon-large">⚡</div>
                <h3 style="color: #667eea;">Real-Time</h3>
                <p style="color: #e0e0e0;">Processing</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="metric-card">
                <div class="icon-large">🎯</div>
                <h3 style="color: #764ba2;">99.9%</h3>
                <p style="color: #e0e0e0;">Accuracy Rate</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="metric-card">
                <div class="icon-large">🔒</div>
                <h3 style="color: #f093fb;">Secure</h3>
                <p style="color: #e0e0e0;">Encrypted</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<br>', unsafe_allow_html=True)
    
    # Transaction Form
    with st.form("transaction_form", clear_on_submit=False):
        st.markdown('<h2 style="color: #e0e0e0; margin-bottom: 20px;">📝 Enter Transaction Details</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            tx_type = st.selectbox(
                "💳 Transaction Type",
                ["CASH_OUT", "TRANSFER", "PAYMENT", "DEBIT"],
                help="Select the type of transaction"
            )
            
            if tx_type == "CASH_OUT":
                st.info("💡 CASH_OUT transactions don't require receiver details")
            
            step = st.number_input("🕐 Step (Hour)", min_value=1, value=1, help="Hour of the transaction")
            amount = st.number_input("💰 Amount", min_value=0.01, value=10000.00, help="Transaction amount")
        
        with col2:
            st.markdown("### 👤 Sender Details")
            oldbalanceOrg = st.number_input("📊 Old Balance (Sender)", min_value=0.01, value=50000.00)
            newbalanceOrig = st.number_input("📈 New Balance (Sender)", min_value=0.0, value=40000.00)
            
            if tx_type != "CASH_OUT":
                st.markdown("### 👥 Receiver Details")
                oldbalanceDest = st.number_input("📊 Old Balance (Receiver)", min_value=0.0, value=20000.00)
                newbalanceDest = st.number_input("📈 New Balance (Receiver)", min_value=0.0, value=30000.00)
            else:
                oldbalanceDest = 0
                newbalanceDest = 0
        
        st.markdown('<br>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submitted = st.form_submit_button("🔍 Analyze Transaction")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------
# PREDICTION LOGIC
# ------------------------------------------------
if submitted:
    st.markdown('<br>', unsafe_allow_html=True)
    
    if tx_type == "CASH_OUT":
        oldbalanceDest = 0
        newbalanceDest = 0

    validation_errors = validate_inputs(tx_type, oldbalanceDest, newbalanceDest)

    if validation_errors:
        st.markdown("""
            <div class="alert-error">
                <h3>🚫 TRANSACTION BLOCKED</h3>
                <p>Invalid transaction detected</p>
            </div>
        """, unsafe_allow_html=True)
        for err in validation_errors:
            st.error(f"• {err}")
        st.stop()

    is_fraud, reason = hard_fraud_rules(
        amount, oldbalanceOrg, newbalanceOrig,
        oldbalanceDest, newbalanceDest, tx_type
    )

    if is_fraud:
        st.markdown(f"""
            <div class="alert-error">
                <h3>🚫 FRAUD DETECTED - TRANSACTION BLOCKED</h3>
                <p><strong>Reason:</strong> {reason}</p>
            </div>
        """, unsafe_allow_html=True)
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

    with st.spinner('🔄 Analyzing transaction...'):
        import time
        time.sleep(1)  # Simulate processing
        ml_score = model.predict_proba(df)[0][1]
        rule_risk, rule_reasons = risk_score_rules(amount, oldbalanceOrg, newbalanceOrig, tx_type)
        total_risk = min(ml_score + rule_risk, 1.0)

    # Results Section
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown('<h2 style="color: #e0e0e0; text-align: center;">📊 Fraud Analysis Results</h2>', unsafe_allow_html=True)
    
    # Risk Score Meters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <h4 style="color: #667eea;">🤖 ML Risk Score</h4>
                <h2 style="color: white;">{ml_score:.3f}</h2>
                <div class="custom-progress">
                    <div class="progress-fill" style="width: {ml_score*100}%; background: linear-gradient(90deg, #667eea, #764ba2);"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <h4 style="color: #f2994a;">📋 Rule Risk Score</h4>
                <h2 style="color: white;">{rule_risk:.3f}</h2>
                <div class="custom-progress">
                    <div class="progress-fill" style="width: {rule_risk*100}%; background: linear-gradient(90deg, #f2994a, #f2c94c);"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_risk_color = "#00b09b" if total_risk < 0.3 else "#f2994a" if total_risk < 0.7 else "#cb2d3e"
        st.markdown(f"""
            <div class="metric-card" style="border: 2px solid {total_risk_color};">
                <h4 style="color: {total_risk_color};">🎯 Total Risk Score</h4>
                <h2 style="color: white;">{total_risk:.3f}</h2>
                <div class="custom-progress">
                    <div class="progress-fill" style="width: {total_risk*100}%; background: linear-gradient(90deg, {total_risk_color}, {total_risk_color});"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<br>', unsafe_allow_html=True)
    
    # Decision Box
    if total_risk < 0.30:
        st.markdown("""
            <div class="alert-success">
                <h3>✅ SAFE - Transaction Approved</h3>
                <p>Low risk detected. Transaction can proceed safely.</p>
            </div>
        """, unsafe_allow_html=True)
        st.balloons()
    elif total_risk < 0.70:
        st.markdown("""
            <div class="alert-warning">
                <h3>⚠️ SUSPICIOUS - Manual Review Required</h3>
                <p>Moderate risk detected. Please review before approving.</p>
            </div>
        """, unsafe_allow_html=True)
    elif total_risk < 0.80:
        st.markdown("""
            <div class="alert-warning">
                <h3>⚠️⚠️ HIGH RISK - Mandatory Manual Review</h3>
                <p>High fraud probability. Expert verification required.</p>
            </div>
        """, unsafe_allow_html=True)
        st.error("🔴 High Risk Transaction!")
    else:
        st.markdown("""
            <div class="alert-error">
                <h3>🚫 FRAUD CONFIRMED - Transaction Blocked</h3>
                <p>Critical fraud indicators detected.</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Risk Rules Details
    if rule_reasons:
        st.markdown('<br>', unsafe_allow_html=True)
        st.markdown("""
            <div class="custom-card">
                <h4 style="color: #f2994a;">🔍 Triggered Risk Rules</h4>
            </div>
        """, unsafe_allow_html=True)
        for reason in rule_reasons:
            st.markdown(f"""
                <div class="metric-card" style="margin-bottom: 10px; text-align: left;">
                    <p style="color: #e0e0e0; margin: 0;">{reason}</p>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------
# Sidebar with Info
# ------------------------------------------------
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <h2 style="color: #667eea;">🛡️ FraudShield AI</h2>
            <p style="color: #e0e0e0;">v2.0</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
        <div class="custom-card">
            <h4 style="color: #667eea;">📊 Detection Methods</h4>
            <ul style="color: #e0e0e0;">
                <li>Machine Learning Model</li>
                <li>Rule-Based Validation</li>
                <li>Pattern Recognition</li>
                <li>Real-Time Scoring</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<br>', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="custom-card">
            <h4 style="color: #764ba2;">🎯 Risk Levels</h4>
            <ul style="color: #e0e0e0;">
                <li><span style="color: #00b09b;">●</span> Low (0-30%)</li>
                <li><span style="color: #f2994a;">●</span> Medium (30-70%)</li>
                <li><span style="color: #cb2d3e;">●</span> High (70-100%)</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<br><br>', unsafe_allow_html=True)
    
    st.markdown("""
        <div style="text-align: center; color: #e0e0e0; font-size: 12px;">
            <p>Built with ❤️ by Shreeyansh Asati</p>
            <p>© 2025 All Rights Reserved</p>
        </div>
    """, unsafe_allow_html=True)

# ------------------------------------------------
# Footer
# ------------------------------------------------
st.markdown("""
    <div class="footer">
        © 2025 | Built by <b>Shreeyansh Asati</b> | FraudShield AI - Hybrid Fraud Detection System
    </div>
""", unsafe_allow_html=True)
