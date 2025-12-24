
# HYBRID FRAUD DETECTION SYSTEM (ML + RULE ENGINE)


----------------------------------------------------
PROJECT OVERVIEW
----------------------------------------------------
This project implements a real-world Fraud Detection System for financial transactions
using a hybrid approach that combines:

• Machine Learning (Random Forest)
• Rule-Based Fraud Detection
• Risk Scoring & Decision Engine
• Interactive Web UI using Streamlit

Instead of relying only on ML predictions, this system enforces
financial and accounting logic using deterministic rules, followed by
probabilistic risk scoring using ML.

Final decisions are classified as:
1. NOT FRAUD (Approve)
2. FLAGGED (Manual Review)
3. FRAUD (Block Transaction)

----------------------------------------------------
WHY NOT ONLY MACHINE LEARNING?
----------------------------------------------------
Machine learning models learn from historical data patterns.
They do NOT understand financial laws such as:

• Money must be deducted from sender
• Receiver cannot be credited without sender debit
• Balances cannot become negative
• Sudden account drain is suspicious

During development, it was observed that ML alone can misclassify
logically impossible transactions as non-fraud due to dataset bias.

Therefore, a hybrid architecture was implemented:

RULE ENGINE (Hard Constraints) → ML RISK SCORING → DECISION ENGINE

This reflects how real banks and fintech systems operate.

----------------------------------------------------
DATASET USED
----------------------------------------------------
Dataset Name: PaySim – A Financial Mobile Money Simulator

Description:
PaySim is a synthetic dataset that simulates real mobile money
transactions and fraud scenarios.

Key Characteristics:
• Highly imbalanced dataset (~0.1% fraud)
• Realistic transaction types and balances
• Commonly used for fraud research

Dataset Link:
https://www.kaggle.com/datasets/ealaxi/paysim1

----------------------------------------------------
FEATURES USED
----------------------------------------------------
• step
• amount
• oldbalanceOrg
• newbalanceOrig
• oldbalanceDest
• newbalanceDest
• balance_diff_orig (engineered)
• balance_diff_dest (engineered)
• transaction type (one-hot encoded)

----------------------------------------------------
MODEL SELECTION
----------------------------------------------------
Algorithm Used: Random Forest Classifier

Reason for choosing Random Forest over XGBoost:
• Better interpretability
• Robust to noisy & imbalanced data
• Easier deployment
• Faster inference for real-time systems
• Handles non-linear patterns well

Random Forest performed consistently with lower operational complexity.

----------------------------------------------------
MODEL PERFORMANCE (APPROXIMATE)
----------------------------------------------------
Precision : ~80%
Recall    : ~90%
ROC-AUC   : High (fraud-focused optimization)

Recall was prioritized over precision to minimize missed fraud cases,
which is critical in financial systems.

----------------------------------------------------
SYSTEM ARCHITECTURE
----------------------------------------------------
1. User enters transaction details
2. Hard Rule Validation (Accounting & Logic Checks)
3. Risk Scoring Rules (Behavioral Patterns)
4. ML Probability Prediction
5. Risk Aggregation
6. Final Decision:
   - Approve
   - Flag for Review
   - Block Transaction

----------------------------------------------------
RULE-BASED FRAUD LOGIC (EXAMPLES)
----------------------------------------------------
HARD RULES (Immediate Block):
• Amount > Sender balance
• Sender balance not deducted properly
• Receiver credited without sender debit
• Receiver credited more than transferred amount
• Negative balances
• Ledger inconsistency

RISK RULES (Score Increase):
• High-value transactions
• Draining more than 90% balance
• CASH_OUT transactions
• Sender balance suddenly becomes zero (Account Drain)
• Very large transaction amounts

----------------------------------------------------
TECH STACK / LIBRARIES
----------------------------------------------------
• Python
• Pandas
• NumPy
• Scikit-learn (Training)
• Joblib (Model serialization)
• Streamlit (Web UI)

----------------------------------------------------
DEPLOYMENT
----------------------------------------------------
Deployment Platform: Streamlit Community Cloud

Live Application:
[ADD YOUR STREAMLIT DEPLOYED LINK HERE]

GitHub Repository:
[ADD YOUR GITHUB REPO LINK HERE]

----------------------------------------------------
USER INTERFACE
----------------------------------------------------
• Interactive Streamlit Web App
• Dynamic input validation
• Conditional field visibility (CASH_OUT logic)
• Risk explanation display
• Footer watermark

----------------------------------------------------
CHALLENGES FACED DURING DEVELOPMENT
----------------------------------------------------
1. ML predicting incorrect results for logically impossible cases
2. Handling extreme class imbalance
3. Designing financial rules without overfitting
4. Deployment issues due to Python & Linux dependency mismatches
5. Streamlit Cloud compatibility challenges
6. Model size & serialization constraints
7. Input validation & UX consistency

All challenges were resolved using engineering-first thinking
instead of model-only tuning.

----------------------------------------------------
WHY THIS PROJECT IS REAL-WORLD READY
----------------------------------------------------
• Hybrid ML + Rule-based architecture
• Explainable decisions
• Risk-based outputs (not just binary)
• Production-style validation
• Deployment-ready
• UI + Backend integration

----------------------------------------------------
AREAS FOR FUTURE IMPROVEMENT
----------------------------------------------------
• Velocity-based fraud detection
• User transaction history profiling
• Dynamic threshold tuning
• SHAP / Explainability dashboards
• Database integration
• REST API using FastAPI
• Model monitoring & drift detection
• Batch transaction processing

----------------------------------------------------
DEVELOPED BY
----------------------------------------------------
Name: Shreeyansh Asati
Role: Machine Learning / Data Science Enthusiast
Project Type: Real-world Applied ML System

----------------------------------------------------
FINAL NOTE
----------------------------------------------------
This project focuses on solving a real business problem
rather than achieving high accuracy alone.

It demonstrates system design, domain understanding,
and responsible ML deployment.

====================================================
