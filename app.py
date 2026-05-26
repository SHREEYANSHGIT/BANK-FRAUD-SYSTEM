import streamlit as st
import pandas as pd
import joblib
import os

# ------------------------------------------------
# Load trained model
# ------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "xgb_model.joblib")
model = joblib.load(MODEL_PATH)

st.set_page_config(
    page_title="FraudShield — Detection System",
    layout="centered",
    page_icon="🛡️"
)

# ------------------------------------------------
# CUSTOM CSS — Dark Fintech Aesthetic
# ------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

/* ---- ROOT VARIABLES ---- */
:root {
    --bg-base:      #080c14;
    --bg-card:      #0d1421;
    --bg-input:     #111827;
    --border:       #1e2d45;
    --border-glow:  #2563eb;
    --accent-blue:  #3b82f6;
    --accent-cyan:  #06b6d4;
    --accent-green: #10b981;
    --accent-amber: #f59e0b;
    --accent-red:   #ef4444;
    --text-primary: #f0f6ff;
    --text-muted:   #64748b;
    --text-dim:     #334155;
    --font-main:    'Space Grotesk', sans-serif;
    --font-mono:    'JetBrains Mono', monospace;
}

/* ---- GLOBAL RESET ---- */
html, body, [class*="css"] {
    font-family: var(--font-main) !important;
    background-color: var(--bg-base) !important;
    color: var(--text-primary) !important;
}

.stApp {
    background: var(--bg-base) !important;
    background-image:
        radial-gradient(ellipse at 20% 0%, rgba(37,99,235,0.12) 0%, transparent 60%),
        radial-gradient(ellipse at 80% 100%, rgba(6,182,212,0.08) 0%, transparent 55%);
    min-height: 100vh;
}

/* ---- HIDE STREAMLIT CHROME ---- */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 2.5rem 2rem 5rem !important;
    max-width: 720px !important;
}

/* ---- HERO HEADER ---- */
.hero-wrap {
    text-align: center;
    padding: 2.5rem 0 2rem;
    position: relative;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(59,130,246,0.12);
    border: 1px solid rgba(59,130,246,0.3);
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--accent-cyan);
    margin-bottom: 1rem;
}
.hero-title {
    font-size: clamp(2rem, 5vw, 2.8rem);
    font-weight: 700;
    letter-spacing: -0.03em;
    line-height: 1.1;
    margin: 0 0 0.5rem;
    background: linear-gradient(135deg, #f0f6ff 0%, var(--accent-cyan) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: 0.9rem;
    color: var(--text-muted);
    font-weight: 400;
    margin-bottom: 0.3rem;
}
.hero-author {
    font-size: 0.78rem;
    color: var(--text-dim);
    font-family: var(--font-mono);
}
.hero-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 2rem 0;
}

/* ---- STAT PILLS ROW ---- */
.stat-row {
    display: flex;
    gap: 12px;
    margin-bottom: 2rem;
    flex-wrap: wrap;
}
.stat-pill {
    flex: 1;
    min-width: 130px;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 14px 18px;
    display: flex;
    flex-direction: column;
    gap: 4px;
    transition: border-color 0.2s;
}
.stat-pill:hover { border-color: var(--accent-blue); }
.stat-pill .sp-label {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--text-muted);
}
.stat-pill .sp-val {
    font-size: 1.2rem;
    font-weight: 700;
    font-family: var(--font-mono);
    color: var(--text-primary);
}
.stat-pill .sp-desc {
    font-size: 0.7rem;
    color: var(--text-dim);
}

/* ---- FORM CARD ---- */
.form-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.form-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent-blue), var(--accent-cyan));
}
.section-label {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--accent-cyan);
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* ---- STREAMLIT WIDGETS OVERRIDES ---- */
div[data-baseweb="select"] > div,
.stSelectbox > div > div {
    background: var(--bg-input) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
}
div[data-baseweb="select"] > div:hover,
.stSelectbox > div > div:hover {
    border-color: var(--accent-blue) !important;
}

input[type="number"], .stNumberInput > div > div > input {
    background: var(--bg-input) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    font-family: var(--font-mono) !important;
    font-size: 0.92rem !important;
    padding: 0.5rem 0.8rem !important;
}
input[type="number"]:focus, .stNumberInput > div > div > input:focus {
    border-color: var(--accent-blue) !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.15) !important;
    outline: none !important;
}

label, .stSelectbox label, .stNumberInput label {
    color: var(--text-muted) !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
    margin-bottom: 4px !important;
}

/* ---- SUBMIT BUTTON ---- */
div[data-testid="stFormSubmitButton"] > button,
.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, #1d4ed8 0%, #0284c7 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.85rem 2rem !important;
    font-family: var(--font-main) !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    margin-top: 1rem !important;
    position: relative !important;
    overflow: hidden !important;
}
div[data-testid="stFormSubmitButton"] > button:hover,
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(37,99,235,0.4) !important;
}
div[data-testid="stFormSubmitButton"] > button:active,
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ---- RESULT CARDS ---- */
.result-card {
    border-radius: 16px;
    padding: 1.8rem;
    margin: 1.2rem 0;
    border: 1px solid;
    position: relative;
    overflow: hidden;
}
.result-card.approved {
    background: rgba(16,185,129,0.06);
    border-color: rgba(16,185,129,0.25);
}
.result-card.flagged {
    background: rgba(245,158,11,0.06);
    border-color: rgba(245,158,11,0.25);
}
.result-card.blocked {
    background: rgba(239,68,68,0.06);
    border-color: rgba(239,68,68,0.25);
}
.result-title {
    font-size: 1.4rem;
    font-weight: 700;
    margin-bottom: 0.3rem;
}
.result-title.green { color: var(--accent-green); }
.result-title.amber { color: var(--accent-amber); }
.result-title.red   { color: var(--accent-red); }
.result-desc {
    font-size: 0.85rem;
    color: var(--text-muted);
    margin-bottom: 1.2rem;
}

/* ---- SCORE GAUGES ---- */
.score-grid {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    margin-top: 1rem;
}
.score-box {
    flex: 1;
    min-width: 110px;
    background: rgba(0,0,0,0.3);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 12px 14px;
}
.score-box .sb-label {
    font-size: 9px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-muted);
    font-weight: 600;
}
.score-box .sb-val {
    font-size: 1.5rem;
    font-weight: 700;
    font-family: var(--font-mono);
    line-height: 1.2;
}
.score-box .sb-bar {
    height: 3px;
    border-radius: 2px;
    margin-top: 8px;
    background: var(--border);
    overflow: hidden;
}
.score-box .sb-fill {
    height: 100%;
    border-radius: 2px;
    transition: width 0.6s ease;
}

/* ---- RISK RULES LIST ---- */
.rules-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-top: 1rem;
}
.rules-card .rc-title {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--accent-amber);
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 6px;
}
.rule-item {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    padding: 8px 0;
    border-bottom: 1px solid var(--border);
    font-size: 0.86rem;
    color: var(--text-primary);
}
.rule-item:last-child { border-bottom: none; }
.rule-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--accent-amber);
    margin-top: 6px;
    flex-shrink: 0;
}

/* ---- INFO BOX ---- */
.info-chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(6,182,212,0.1);
    border: 1px solid rgba(6,182,212,0.2);
    border-radius: 8px;
    padding: 6px 12px;
    font-size: 0.8rem;
    color: var(--accent-cyan);
    margin: 0.5rem 0 1rem;
}

/* ---- FRAUD BLOCKED HARD RULE ---- */
.hard-block {
    background: rgba(239,68,68,0.07);
    border: 1px solid rgba(239,68,68,0.3);
    border-radius: 14px;
    padding: 1.5rem;
    margin: 1rem 0;
}
.hard-block-title {
    font-size: 1.2rem;
    font-weight: 700;
    color: var(--accent-red);
    margin-bottom: 0.4rem;
}
.hard-block-reason {
    font-size: 0.88rem;
    color: #fca5a5;
    font-family: var(--font-mono);
}

/* ---- FOOTER ---- */
.custom-footer {
    position: fixed;
    bottom: 0; left: 0; right: 0;
    background: rgba(8,12,20,0.95);
    border-top: 1px solid var(--border);
    padding: 10px 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.75rem;
    color: var(--text-dim);
    backdrop-filter: blur(8px);
    z-index: 9999;
}
.custom-footer span { font-family: var(--font-mono); }
.custom-footer b { color: var(--text-muted); }

/* ---- ALERT OVERRIDES ---- */
.stAlert {
    border-radius: 10px !important;
    border: 1px solid !important;
}
</style>
""", unsafe_allow_html=True)

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
        reasons.append("Very high-value transaction over ₹4 lakhs")
    if amount >= 1000000:
        score += 0.1
        reasons.append("Extreme transaction value over ₹10 lakhs")
    if amount > 0.9 * oldOrg:
        score += 0.3
        reasons.append("Drains more than 90% of sender balance")
    if newOrg == 0:
        score += 0.3
        reasons.append("Sender balance became zero post-transaction")
    if tx_type == "CASH_OUT":
        score += 0.2
        reasons.append("High-risk CASH_OUT transaction type")
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
# HERO SECTION
# ------------------------------------------------
st.markdown("""
<div class="hero-wrap">
    <div class="hero-badge">🛡️ &nbsp; AI-Powered Security</div>
    <h1 class="hero-title">FraudShield</h1>
    <p class="hero-sub">Hybrid Rule-Based + ML Transaction Risk Scoring</p>
    <p class="hero-author">by Shreeyansh Asati</p>
</div>
<div class="hero-divider"></div>
""", unsafe_allow_html=True)

# ---- STAT PILLS ----
st.markdown("""
<div class="stat-row">
    <div class="stat-pill">
        <span class="sp-label">Detection Mode</span>
        <span class="sp-val">Hybrid</span>
        <span class="sp-desc">Rules + XGBoost ML</span>
    </div>
    <div class="stat-pill">
        <span class="sp-label">Threshold — Safe</span>
        <span class="sp-val">&lt; 0.30</span>
        <span class="sp-desc">Auto-approved</span>
    </div>
    <div class="stat-pill">
        <span class="sp-label">Threshold — Block</span>
        <span class="sp-val">≥ 0.80</span>
        <span class="sp-desc">Hard block</span>
    </div>
    <div class="stat-pill">
        <span class="sp-label">Hard Rules</span>
        <span class="sp-val">6</span>
        <span class="sp-desc">Pre-ML checks</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------
# FORM
# ------------------------------------------------
st.markdown('<div class="form-card">', unsafe_allow_html=True)
st.markdown('<div class="section-label">⚡ Transaction Details</div>', unsafe_allow_html=True)

with st.form("transaction_form"):
    tx_type = st.selectbox(
        "Transaction Type",
        ["CASH_OUT", "TRANSFER", "PAYMENT", "DEBIT"],
        help="CASH_OUT transactions skip receiver balance validation"
    )

    if tx_type == "CASH_OUT":
        st.markdown('<div class="info-chip">ℹ️ CASH_OUT selected — receiver balance fields will be ignored</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        step = st.number_input("Step (Hour)", min_value=1, value=1)
    with col2:
        amount = st.number_input("Amount (₹)", min_value=0.01, format="%.2f")

    st.markdown('<div class="section-label" style="margin-top:1.2rem">💳 Sender Balances</div>', unsafe_allow_html=True)
    col3, col4 = st.columns(2)
    with col3:
        oldbalanceOrg = st.number_input("Old Balance — Sender (₹)", min_value=0.01, format="%.2f")
    with col4:
        newbalanceOrig = st.number_input("New Balance — Sender (₹)", min_value=0.0, format="%.2f")

    st.markdown('<div class="section-label" style="margin-top:1.2rem">🏦 Receiver Balances</div>', unsafe_allow_html=True)
    col5, col6 = st.columns(2)
    with col5:
        oldbalanceDest = st.number_input("Old Balance — Receiver (₹)", min_value=0.0, format="%.2f",
                                          disabled=(tx_type == "CASH_OUT"))
    with col6:
        newbalanceDest = st.number_input("New Balance — Receiver (₹)", min_value=0.0, format="%.2f",
                                          disabled=(tx_type == "CASH_OUT"))

    submitted = st.form_submit_button("🔍 Analyse Transaction Risk")

st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------
# PREDICTION LOGIC
# ------------------------------------------------
if submitted:
    if tx_type == "CASH_OUT":
        oldbalanceDest = 0
        newbalanceDest = 0

    # --- Validation errors ---
    validation_errors = validate_inputs(tx_type, oldbalanceDest, newbalanceDest)
    if validation_errors:
        st.markdown(f"""
        <div class="hard-block">
            <div class="hard-block-title">🚫 BLOCKED — Input Validation Failed</div>
            {"".join(f'<div class="hard-block-reason">↳ {e}</div>' for e in validation_errors)}
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    # --- Hard fraud rules ---
    is_fraud, reason = hard_fraud_rules(
        amount, oldbalanceOrg, newbalanceOrig,
        oldbalanceDest, newbalanceDest, tx_type
    )
    if is_fraud:
        st.markdown(f"""
        <div class="hard-block">
            <div class="hard-block-title">🚫 FRAUD DETECTED — Hard Rule Triggered</div>
            <div class="hard-block-reason">↳ {reason}</div>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    # --- Feature engineering ---
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
    rule_risk, rule_reasons = risk_score_rules(amount, oldbalanceOrg, newbalanceOrig, tx_type)
    total_risk = min(ml_score + rule_risk, 1.0)

    # --- Determine verdict ---
    if total_risk < 0.30:
        verdict_class = "approved"
        verdict_title_class = "green"
        verdict_icon = "✅"
        verdict_text = "APPROVED"
        verdict_desc = "Transaction cleared all checks. Risk is within acceptable bounds."
    elif total_risk < 0.70:
        verdict_class = "flagged"
        verdict_title_class = "amber"
        verdict_icon = "⚠️"
        verdict_text = "FLAGGED — Manual Review"
        verdict_desc = "Moderate risk detected. Route to compliance team for verification."
    elif total_risk < 0.80:
        verdict_class = "flagged"
        verdict_title_class = "amber"
        verdict_icon = "⚠️"
        verdict_text = "HIGH RISK — Review Mandatory"
        verdict_desc = "Elevated fraud signals. Immediate manual review required before processing."
    else:
        verdict_class = "blocked"
        verdict_title_class = "red"
        verdict_icon = "🚫"
        verdict_text = "BLOCKED — FRAUD"
        verdict_desc = "Risk score exceeds fraud threshold. Transaction has been blocked."

    def score_color(s):
        if s < 0.3: return "#10b981"
        if s < 0.7: return "#f59e0b"
        return "#ef4444"

    ml_color   = score_color(ml_score)
    rule_color = score_color(rule_risk)
    tot_color  = score_color(total_risk)

    st.markdown(f"""
    <div class="result-card {verdict_class}">
        <div class="result-title {verdict_title_class}">{verdict_icon} &nbsp; {verdict_text}</div>
        <div class="result-desc">{verdict_desc}</div>
        <div class="score-grid">
            <div class="score-box">
                <div class="sb-label">ML Score</div>
                <div class="sb-val" style="color:{ml_color}">{ml_score:.3f}</div>
                <div class="sb-bar"><div class="sb-fill" style="width:{ml_score*100:.1f}%;background:{ml_color}"></div></div>
            </div>
            <div class="score-box">
                <div class="sb-label">Rule Score</div>
                <div class="sb-val" style="color:{rule_color}">{rule_risk:.3f}</div>
                <div class="sb-bar"><div class="sb-fill" style="width:{rule_risk*100:.1f}%;background:{rule_color}"></div></div>
            </div>
            <div class="score-box">
                <div class="sb-label">Total Risk</div>
                <div class="sb-val" style="color:{tot_color}">{total_risk:.3f}</div>
                <div class="sb-bar"><div class="sb-fill" style="width:{total_risk*100:.1f}%;background:{tot_color}"></div></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- Triggered rules ---
    if rule_reasons:
        rules_html = "".join(
            f'<div class="rule-item"><div class="rule-dot"></div><span>{r}</span></div>'
            for r in rule_reasons
        )
        st.markdown(f"""
        <div class="rules-card">
            <div class="rc-title">⚡ Triggered Risk Rules</div>
            {rules_html}
        </div>
        """, unsafe_allow_html=True)

# ------------------------------------------------
# FOOTER
# ------------------------------------------------
st.markdown("""
<div class="custom-footer">
    <span>© 2025 &nbsp;<b>FraudShield</b> &nbsp;·&nbsp; Hybrid Fraud Detection System</span>
    <span>Built by <b>Shreeyansh Asati</b></span>
</div>
""", unsafe_allow_html=True)
