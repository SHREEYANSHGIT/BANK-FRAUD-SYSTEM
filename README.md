💳 HYBRID FRAUD DETECTION SYSTEM  
================================

# 👨‍💻 Developed By: Shreeyansh Asati  

🔗 GitHub: https://www.linkedin.com/in/shreeyansh-asati-18shreey/

🌐 Live App (Streamlit): https://bank-fraud-system-shreeyansh.streamlit.app/

💾 Dataset link : https://www.kaggle.com/datasets/mtalaltariq/paysim-data

--------------------------------------------------
📌 PROJECT OVERVIEW
--------------------------------------------------
This project is a **real-world fraud detection decision system** built for
digital payment transactions.

Unlike simple ML projects, this system combines:
✅ Machine Learning (Random Forest)

✅ Rule-Based Fraud Detection

✅ Risk Scoring & Decision Engine

✅ User-Friendly Streamlit Web App

The goal is NOT just to predict fraud, but to make **actionable decisions**:
• Allow transaction  
• Flag for manual review  
• Block fraudulent transaction  

--------------------------------------------------
📊 DATASET INFORMATION
--------------------------------------------------
📁 Dataset Used: PaySim – A Financial Mobile Money Simulator Dataset


📌 Description:
PaySim is a synthetic dataset that simulates mobile money transactions
based on real financial behavior.

📌 Why PaySim?
• Highly imbalanced fraud data (realistic)
• Widely used in fraud research
• Mimics real payment systems

🔗 Dataset Link:
https://www.kaggle.com/datasets/ealaxi/paysim1

--------------------------------------------------
🤖 MACHINE LEARNING MODEL
--------------------------------------------------
Model Used: **Random Forest Classifier**

📌 Why Random Forest over XGBoost?
---------------------------------
✔ Handles class imbalance well

✔ Robust to noisy financial data

✔ Easier to interpret for risk systems

✔ Faster & more stable for deployment

✔ Less overfitting compared to boosting

🚫 Why NOT only XGBoost?
XGBoost is powerful but:
• Harder to interpret
• Sensitive to noise
• Overkill when business rules dominate

In fraud systems, **stability & explainability > marginal accuracy gains**.

--------------------------------------------------
📈 MODEL PERFORMANCE
--------------------------------------------------
Metric              | Value
------------------- | -------
Precision (Fraud)   | ~80%
Recall (Fraud)      | ~90%
ROC-AUC             | High
False Negatives     | Minimized (priority)

📌 Why Recall is prioritized?
Missing a fraud is more costly than flagging a legit transaction.

--------------------------------------------------
🧠 WHY ML + RULE-BASED (NOT ONLY ML)
--------------------------------------------------
Machine Learning:
✔ Finds hidden patterns
✔ Learns probabilistic behavior

BUT ML CANNOT:

❌ Enforce financial laws

❌ Guarantee ledger consistency

❌ Catch logically impossible cases


📌 Example:

If sender balance is NOT reduced but receiver balance increases,
ML alone may still say “Not Fraud”.

✔ RULES catch this instantly.

👉 Therefore, this system uses:
ML = Risk probability  
Rules = Absolute financial logic  

This is how **real banks & fintech companies** operate.

--------------------------------------------------
⚙️ SYSTEM ARCHITECTURE
--------------------------------------------------
Transaction Input

      ↓
Hard Fraud Rules (Ledger Validation)

      ↓
Risk Scoring Rules (Behavioral)

      ↓
ML Probability (Random Forest)

      ↓
Final Decision Engine

      ↓
✅ NOT FRAUD | ⚠️ FLAGGED | 🚫 FRAUD


--------------------------------------------------
🧱 RULE-BASED LOGIC (Examples)
--------------------------------------------------
🚫 HARD RULES (Immediate Block)

• Amount > Sender balance

• Sender balance not deducted correctly

• Receiver credited incorrectly

• Negative balances

⚠️ RISK RULES (Score Based)

• High-value transaction

• Account drained >90%

• Sender balance suddenly becomes zero

• CASH_OUT transactions

--------------------------------------------------
🖥️ WEB APPLICATION (STREAMLIT)
--------------------------------------------------
Framework: Streamlit

Features:

✔ Interactive UI

✔ Mandatory input validation

✔ CASH_OUT logic handling

✔ Real-time risk explanation

✔ Deployed on Streamlit Cloud

--------------------------------------------------
📁 Project Structure
--------------------------------------------------
📂 Hybrid-Fraud-Detection
- │
- ├── 📓 main_model.ipynb              # Model training & evaluation
- ├── 📦 rf_model.joblib               # Trained Random Forest model
- ├── 🖥️ app.py                        # Streamlit application
- ├── 📄 requirements.txt              # Required libraries
- └── 📘 README.txt                    # Project documentation

--------------------------------------------------
📚 LIBRARIES USED
--------------------------------------------------
• Python

• Pandas

• NumPy

• Scikit-learn

• Joblib

• Streamlit

• OS (path handling)

--------------------------------------------------
🚧 CHALLENGES FACED
--------------------------------------------------
🔴 Highly imbalanced dataset
🔴 ML misclassifying logically impossible cases
🔴 Deployment issues on Streamlit Cloud
🔴 Python version & dependency conflicts
🔴 Integrating rules without breaking ML flow
🔴 Making UI dynamic & realistic

✔ All issues were solved using engineering-first thinking.

--------------------------------------------------
🚀 DEPLOYMENT
--------------------------------------------------
Platform: Streamlit Community Cloud  
CI/CD: GitHub auto-deploy on push  

Live App:
🌐 https://bank-fraud-system-shreeyansh.streamlit.app/  

--------------------------------------------------
🔮 FUTURE IMPROVEMENTS
--------------------------------------------------
• Transaction velocity rules

• User historical profiling

• Rule weights configuration file

• Audit logs (CSV / DB)

• Explainability (SHAP)

• REST API (FastAPI)

• Docker deployment

--------------------------------------------------
🎯 KEY TAKEAWAY
--------------------------------------------------
This project demonstrates:

✔ Real-world fraud system design

✔ Hybrid ML + Rule architecture

✔ Risk-based decision making

✔ End-to-end ownership

This is NOT just an ML model —
this is a **production-style fraud detection system**.

--------------------------------------------------
⭐ FINAL NOTE
--------------------------------------------------
If you are reviewing this project as a recruiter or mentor:
This work reflects **practical ML engineering**, not just academic modeling.

--------------------------------------------------
