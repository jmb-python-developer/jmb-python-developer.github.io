<a href="https://jmb-python-developer.github.io/"><img src="assets/ml-quest-map.svg" width="100%" alt="ML Quest world map: my machine-learning projects shown as game levels. Click to open the interactive version."></a>

<sub>Click a level below to see what it covered, or open the <a href="https://jmb-python-developer.github.io/">interactive map</a>.</sub>

<details>
<summary><b>✅ Level 1.0 · Exam Score Predictor</b> — Cleared</summary>

**Mission:** Predict a student's exam score from five everyday habits: study hours, attendance, sleep, mental health and part-time work.

**Result:** Predictions land within about 7 points on a 0–100 score, and the model explains 81% of the variation between students.

**Learned:**
- The full pipeline once, end to end: explore the data, build features, compare models, ship an app
- Judging models against a simple baseline, so scores mean something
- Keeping the test set untouched until the very end

**Skills:** `Python` · `pandas` · `scikit-learn` · `Regression` · `Cross-validation` · `Streamlit app`

[Open the project ↗](https://github.com/jmb-python-developer/ML-01-exam-scores-prediction)

</details>
<details>
<summary><b>✅ Level 1.2 · Customer Churn Prediction</b> — Cleared</summary>

**Mission:** Predict which of a bank's 10,000 customers are about to leave, using account and demographic data.

**Result:** When the best model flags a customer as leaving, it is right about 3 times out of 4. It finds about half of the customers who actually leave.

**Learned:**
- Backing up what the charts suggest with statistical tests
- Why accuracy misleads when most customers stay
- Comparing five different models fairly and picking one on evidence

**Skills:** `Classification` · `Hypothesis testing` · `Feature scaling` · `Pipelines` · `Precision & recall` · `5-model comparison`

[Open the project ↗](https://github.com/jmb-python-developer/ML-02-customer-churn-prediction)

</details>
<details>
<summary><b>⭐ Level 1.3 · Credit Risk Scoring</b> — In progress</summary>

**Mission:** Predict which loan applicants will default, and tune the models so they catch more of the risky ones.

**Result:** In progress.

**Will learn:**
- Tuning models instead of accepting their defaults
- Handling data where the important cases are the rare ones
- Choosing the decision cut-off on purpose, based on the cost of each kind of mistake

**Skills:** `Hyperparameter tuning` · `Random forest` · `XGBoost` · `Class imbalance` · `Threshold tuning`

[Open the project ↗](https://github.com/jmb-python-developer/ML-03-credit-risk-scoring)

</details>
<details>
<summary><b>🔒 Level 1.4 · Model Serving</b> — Locked</summary>

**Mission:** Turn the 1.3 model into a web service that other software can call, packaged so it runs anywhere.

**Will learn:**
- Moving from a notebook to a real, repeatable training script
- Serving predictions through an API that rejects bad input
- Packaging the service in a container

**Skills:** `FastAPI` · `REST API` · `Docker` · `Deployment`

</details>

**How I use AI.** I write the modelling code and make the analysis decisions myself: what to explore, which models to compare, how to evaluate them and what the results mean. I use LLMs the way I would on any engineering team: to scaffold projects, handle repetitive boilerplate, talk through concepts, and draft documentation and tooling (including this page), which I review and edit before it ships.
