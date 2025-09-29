# SLE Cardiovascular Risk Calculator

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://sle-cv-risk-calculator.streamlit.app)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A machine learning-based tool for predicting cardiovascular event risk in patients with Systemic Lupus Erythematosus (SLE).

## 🎯 Overview

This calculator predicts the 5-year cardiovascular event risk in SLE patients using baseline clinical and biological features. It is based on the LESLY cohort (n=874 patients) from Hospices Civils de Lyon, France.

**Live Application**: [https://sle-cv-risk-calculator.streamlit.app](https://sle-cv-risk-calculator.streamlit.app)

## 📊 Model Performance

- **C-index**: 0.76
- **Brier score**: 0.064
- **Validation**: 10-fold cross-validation
- **Algorithm**: Elastic Net Penalized Cox Regression (CoxNet)

## 🔬 Key Findings

The study identified several significant predictors of cardiovascular events in SLE:

### Traditional Risk Factors
- Male sex (HR=2.28, p=0.009)
- Hypertension (HR=2.00, p=0.047)
- Smoking (HR=1.76, p=0.049)

### SLE-Specific Factors
- **Antiphospholipid antibodies** (HR=3.51, p<0.001) - *Most potent predictor*
- **Inaugural cutaneous signs** (HR=2.69, p=0.011)
- Inaugural joint involvement (HR=0.55, p=0.043) - *Protective factor*

### Main Result
SLE patients exhibited **8.25× higher cardiovascular risk** (HR=8.25 [5.90-11.53], p<0.001) compared to the general population (UK Biobank cohort, n=48,104), even after adjusting for traditional cardiovascular risk factors.

## 🚀 Features

- **Interactive risk calculator** with real-time predictions
- **Survival curve visualization** using Plotly
- **Risk stratification** (Low/Medium/High)
- **Comparative analysis** vs. general population and average SLE patients
- **Results export** functionality
- **Responsive design** (mobile-friendly)

## 💻 Local Installation

### Prerequisites

- Python 3.9 or higher
- pip

### Setup

1. Clone the repository:
```bash
git clone https://github.com/YOUR-USERNAME/sle-cv-risk-calculator.git
cd sle-cv-risk-calculator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

4. Open your browser at `http://localhost:8501`

## 📝 Usage

### Input Parameters

The calculator requires the following patient information:

**Demographics:**
- Age at SLE diagnosis
- Sex

**Traditional CV Risk Factors:**
- Hypertension
- Diabetes mellitus
- Dyslipidemia
- BMI ≥25
- Smoking (current or past)

**SLE-Specific Features:**
- Antiphospholipid antibodies (any positive: anticardiolipin, anti-β2GP1, or lupus anticoagulant)
- Inaugural cutaneous signs
- Inaugural joint involvement

### Output

The calculator provides:
- 5-year cardiovascular event probability
- Risk category (Low/Medium/High)
- Interactive survival curve
- Risk comparison chart
- Clinical recommendations based on risk level

## 🏥 Clinical Application

This tool is designed to assist clinicians in:
- **Early risk stratification** of SLE patients
- **Identifying high-risk patients** requiring intensive cardiovascular prevention
- **Supporting clinical decision-making** for antiplatelet/anticoagulation therapy
- **Optimizing follow-up strategies** based on individual risk profiles

⚠️ **Disclaimer**: This calculator is for research and clinical decision support purposes only. It should not replace comprehensive clinical judgment and should be used as part of a broader cardiovascular risk assessment.

## 🧪 Model Details

### Training Data
- **Cohort**: LESLY (Lupus Erythémateux Systémique LYon)
- **Sample size**: 874 SLE patients
- **Inclusion period**: January 2002 - August 2020
- **Follow-up**: Mean 8.77 ± 5.2 years
- **Events**: 55 cardiovascular events (6.3%)

### Model Development
1. **Data preprocessing**: KNN imputation for missing values, age normalization
2. **Algorithm selection**: Comparison of 5 algorithms (RF, CoxPH, CoxNet, fsSVM, GBSA)
3. **Hyperparameter tuning**: Grid search with cross-validation
4. **Validation**: 80/20 train-test split

### Event Definition
Cardiovascular events include:
- Myocardial infarction
- Ischemic stroke
- Mesenteric ischemia
- Lower limb ischemia

## 🔧 Technical Stack

- **Frontend**: Streamlit
- **Visualization**: Plotly
- **ML Framework**: scikit-survival
- **Model**: Elastic Net Penalized Cox Regression
- **Deployment**: Streamlit Cloud


## 👥 Authors

- **Thomas Barba, MD, PhD** - Department of Internal Medicine, Edouard Herriot Hospital, Hospices Civils de Lyon
**Corresponding author**: thomas.barba@chu-lyon.fr

## 🏛️ Affiliations

1. Internal Medicine, Edouard Herriot Hospital, Hospices Civils de Lyon, Lyon, France
2. Lyon 1 University, Lyon, France
3. Lyon Immunology Federation (LIFE), Lyon, France

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


---

**Note**: This research tool is provided for educational and research purposes. Always consult with healthcare professionals for medical decisions.