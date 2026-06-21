#  Indian Tech Salary Predictor & Analyzer

An end-to-end ML project that performs exploratory data analysis (EDA), implements preprocessing pipelines, compares multiple models, and deploys a Streamlit dashboard to predict technology compensation in India.

**[Try the Live App](https://tech-salary-advisor.streamlit.app/)**

---

## 📌 Project Overview
This project analyzes how salaries scale across different dimensions in the Indian tech industry. Specifically, it explores:
* The premium salary trends for AI/ML and Deep Learning roles compared to traditional software roles.
* Non-linear compensation scaling over years of experience.
* Cost-of-living adjustments across major Indian tech hubs (Bangalore, Mumbai, Delhi NCR, Hyderabad, Pune, Chennai, Noida).
* The impact of education levels and individual technical skill flags.

The dataset contains messy data (missing values, inconsistent string formatting, synonyms, and spaces) to demonstrate a complete cleaning, engineering, and modeling data science workflow inside Jupyter Notebooks.

---

## 📂 Repository Structure

```text
Tech-Salary-Advisor/
│
├── data/
│   └── salary_dataset_dirty.csv  ← salary dataset
│
├── notebooks/
│   ├── EDA.ipynb                 ← data cleaning & visualizations
│   └── Salary_Prediction.ipynb   ← preprocessing, model training & tuning
│
├── streamlit/
│   ├── app.py                    ← script to run streamlit app
│   └── models/
│       ├── salary_model.pkl      ← scikit-learn pipeline (preprocessor + model)
│       └── metadata.pkl          
│
├── packages.txt                  ← system dependencies (streamlit)
├── requirements.txt              ← package dependencies
└── README.md                     ← this documentation
```

---

## 🚀 Setup & Execution

### 1. Install Dependencies
Set up your virtual environment and install all packages:
```bash
pip install -r requirements.txt
```

### 2. Exploratory Data Analysis
Open and run **`notebooks/EDA.ipynb`** to explore dataset statistics and view visual trends:
* Distribution of salaries (in LPA).
* Boxplots of compensation ranges by role, city, and degree.
* Bar charts showing top demanded technical skills.

### 3. Model Training & Pipeline Serialization
Open and run **`notebooks/Salary_Prediction.ipynb`**:
* Imputes missing columns (median/mode) and standardizes messy text strings.
* Parses multi-label skills into binary indicators.
* Sets up a scikit-learn `Pipeline` utilizing `ColumnTransformer` (StandardScaler for experience, OHE for categoricals,etc).
* Trains and compares **ElasticNet, Random Forest, XGBoost, and CatBoost**.
* **Tunes hyperparameter spaces** for the top 2 models using `RandomizedSearchCV`.
* Exports the final tuned pipeline and metadata to `streamlit/models/`.

### 4. Launch the Dashboard
Run the dashboard application locally:
```bash
streamlit run streamlit/app.py
```
Open `http://localhost:8501` to predict expected salaries, view experience growth curves, and check estimated salary increments for learning new skills.

---

## 📊 Model Evaluation Results

The models were trained on 88,000 training records and evaluated on a 22,000-sample test set (80/20 split):

| Model | Mean Absolute Error (MAE) | R² Score |
|---|---|---|
| **ElasticNet** | ₹ 2,43,005 (~2.43 LPA) | 0.7283 |
| **Random Forest** | ₹ 1,96,974 (~1.96 LPA) | 0.8209 |
| **XGBoost** | ₹ 1,64,437 (~1.64 LPA) | 0.8697 |
| **CatBoost** | ₹ 1,80,936 (~1.80 LPA) | 0.8459 |
| **Tuned XGBoost (CV)** | ₹ 1,63,186 (~1.63 LPA) | 0.8715 |
| **Tuned CatBoost (CV)** | **₹ 1,60,258 (~1.60 LPA)** | **0.8753** |

*Note: The **Tuned CatBoost Regressor Pipeline** is deployed in the Streamlit app due to its superior R² score and lowest MAE, cross-validated with 3 folds.*
