# Copyright (c) 2024 Thomas Barba, Hospices Civils de Lyon
# Licensed under the MIT License - see LICENSE file for details

import streamlit as st
import numpy as np
import pandas as pd
import joblib
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="SLE CV Risk Calculator",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .risk-box {
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
    }
    .risk-low {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border-left: 5px solid #28a745;
    }
    .risk-medium {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        border-left: 5px solid #ffc107;
    }
    .risk-high {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        border-left: 5px solid #dc3545;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="main-header">🩺 SLE Cardiovascular Risk Calculator</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">LESLY Cohort • Hospices Civils de Lyon</p>', unsafe_allow_html=True)

# Load model
@st.cache_resource
def load_model():
    try:
        model = joblib.load('model.pkl')
        return model
    except:
        st.error("⚠️ Model file not found. Please ensure 'model.pkl' is in the same directory.")
        return None

model = load_model()

# Sidebar - Information
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    This calculator predicts the 5-year cardiovascular event risk in patients with Systemic Lupus Erythematosus (SLE).
    
    **Based on:**
    - LESLY Cohort (n=874)
    - C-index: 0.76
    - Brier score: 0.064
    
    **Reference:**
    Barba T, et al. (2024)
    """)
    
    st.divider()
    
    st.header("📊 Model Features")
    st.markdown("""
    **Traditional Risk Factors:**
    - Age, Sex
    - Hypertension
    - Diabetes mellitus
    - Dyslipidemia
    - BMI ≥25
    - Smoking
    
    **SLE-Specific:**
    - Antiphospholipid antibodies
    - Inaugural cutaneous signs
    - Inaugural joint involvement
    """)

# Main content
if model is not None:
    # Create three columns for input
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("👤 Demographics")
        age = st.slider("Age at diagnosis (years)", 18, 90, 35, 1)
        sex = st.radio("Sex", ["Female", "Male"], horizontal=True)
    
    with col2:
        st.subheader("🫀 Traditional CV Risk Factors")
        hta = st.checkbox("Hypertension")
        diabetes = st.checkbox("Diabetes mellitus")
        dyslipidemia = st.checkbox("Dyslipidemia")
        obesity = st.checkbox("BMI ≥25")
        smoking = st.checkbox("Smoking (current or past)")
    
    with col3:
        st.subheader("🦋 SLE-Specific Features")
        apl = st.checkbox("Antiphospholipid antibodies")
        cutaneous = st.checkbox("Inaugural cutaneous signs")
        joint = st.checkbox("Inaugural joint involvement")
    
    st.divider()
    
    # Calculate button
    col_calc1, col_calc2, col_calc3 = st.columns([1, 1, 1])
    with col_calc2:
        calculate = st.button("🔍 Calculate Risk", type="primary", use_container_width=True)
    
    if calculate:
        # Prepare data
        sex_binary = 1 if sex == "Male" else 0
        age_normalized = age / 87.8  # Normalize like in training
        
        # Create feature array
        features = np.array([[
            sex_binary,           # Male sex
            age_normalized,       # Age (normalized)
            int(hta),            # Hypertension
            int(diabetes),       # Diabetes mellitus
            int(dyslipidemia),   # Dyslipidemia
            int(obesity),        # BMI ≥25
            int(smoking),        # Smoking
            int(apl),            # Antiphospholipid antibodies
            int(cutaneous),      # Cutaneous signs
            int(joint)           # Joint involvement
        ]])
        
        # Feature names for display
        feature_names = [
            "Male sex", "Age", "Hypertension", "Diabetes mellitus",
            "Dyslipidemia", "BMI ≥25", "Smoking", 
            "Antiphospholipid antibodies", "Cutaneous signs", "Joint involvement"
        ]
        
        # Create DataFrame
        X = pd.DataFrame(features, columns=feature_names)
        
        # Predict survival function
        try:
            surv_funcs = model.predict_survival_function(X)
            times = surv_funcs[0].x
            survival_probs = surv_funcs[0].y
            
            # Calculate 5-year risk
            five_years = 5 * 365.25
            idx_5y = np.abs(times - five_years).argmin()
            survival_5y = survival_probs[idx_5y]
            risk_5y = (1 - survival_5y) * 100
            
            # Display results
            st.divider()
            st.header("📊 Results")
            
            # Risk category
            if risk_5y < 5:
                risk_category = "LOW"
                risk_color = "risk-low"
                risk_emoji = "✅"
            elif risk_5y < 10:
                risk_category = "MEDIUM"
                risk_color = "risk-medium"
                risk_emoji = "⚠️"
            else:
                risk_category = "HIGH"
                risk_color = "risk-high"
                risk_emoji = "🔴"
            
            # Risk box
            st.markdown(f"""
            <div class="risk-box {risk_color}">
                <h1 style="margin:0; font-size: 3rem;">{risk_emoji} {risk_5y:.1f}%</h1>
                <h3 style="margin:0.5rem 0 0 0;">5-Year Cardiovascular Event Risk</h3>
                <p style="margin:0.5rem 0 0 0; font-size: 1.2rem; font-weight: 600;">{risk_category} RISK</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Two columns for additional info
            col_res1, col_res2 = st.columns(2)
            
            with col_res1:
                st.subheader("📈 Risk Comparison")
                
                # Comparison chart
                comparison_data = {
                    'Category': ['Your Patient', 'Average SLE', 'General Population'],
                    'Risk (%)': [risk_5y, 5.7, 2.7],
                    'Color': ['#dc3545', '#ffc107', '#28a745']
                }
                
                fig_comp = go.Figure(data=[
                    go.Bar(
                        x=comparison_data['Category'],
                        y=comparison_data['Risk (%)'],
                        marker_color=comparison_data['Color'],
                        text=[f"{x:.1f}%" for x in comparison_data['Risk (%)']],
                        textposition='auto',
                    )
                ])
                
                fig_comp.update_layout(
                    title="Risk Comparison",
                    yaxis_title="5-Year CV Event Risk (%)",
                    height=400,
                    showlegend=False
                )
                
                st.plotly_chart(fig_comp, use_container_width=True)
            
            with col_res2:
                st.subheader("📉 Survival Curve")
                
                # Survival curve
                times_years = times / 365.25
                event_probs = (1 - survival_probs) * 100
                
                fig_surv = go.Figure()
                
                fig_surv.add_trace(go.Scatter(
                    x=times_years,
                    y=event_probs,
                    mode='lines',
                    name='Event Probability',
                    line=dict(color='#1f77b4', width=3),
                    fill='tozeroy',
                    fillcolor='rgba(31, 119, 180, 0.2)'
                ))
                
                # Add 5-year marker
                fig_surv.add_vline(x=5, line_dash="dash", line_color="red", 
                                   annotation_text=f"5y: {risk_5y:.1f}%")
                
                fig_surv.update_layout(
                    title="Predicted Event Probability Over Time",
                    xaxis_title="Years from Diagnosis",
                    yaxis_title="Cumulative Event Probability (%)",
                    height=400,
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig_surv, use_container_width=True)
            

            # Export section
            st.divider()
            col_export1, col_export2, col_export3 = st.columns([1, 1, 1])
            
            with col_export2:
                # Create summary text for export
                summary = f"""
SLE Cardiovascular Risk Assessment
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

Patient Characteristics:
- Age: {age} years
- Sex: {sex}
- Hypertension: {'Yes' if hta else 'No'}
- Diabetes: {'Yes' if diabetes else 'No'}
- Dyslipidemia: {'Yes' if dyslipidemia else 'No'}
- BMI ≥25: {'Yes' if obesity else 'No'}
- Smoking: {'Yes' if smoking else 'No'}
- APL: {'Yes' if apl else 'No'}
- Cutaneous signs: {'Yes' if cutaneous else 'No'}
- Joint involvement: {'Yes' if joint else 'No'}

Result:
5-Year CV Event Risk: {risk_5y:.1f}%
Risk Category: {risk_category}

LESLY Cohort Model (C-index: 0.76)
                """
                
                st.download_button(
                    label="📄 Export Results",
                    data=summary,
                    file_name=f"SLE_CV_Risk_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
        
        except Exception as e:
            st.error(f"Error during prediction: {str(e)}")
            st.info("Please ensure all inputs are valid and the model file is correctly loaded.")

else:
    st.warning("⚠️ Model not loaded. Please add 'model.pkl' to the app directory.")

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    <p><strong>Disclaimer:</strong> This calculator is for research purposes only and should not replace clinical judgment.</p>
    <p>© 2024 LESLY Cohort - Hospices Civils de Lyon</p>
</div>
""", unsafe_allow_html=True)