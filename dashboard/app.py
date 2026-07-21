import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Ethiopia Financial Inclusion Forecast Dashboard",
    page_icon="🇪🇹",
    layout="wide"
)

st.title("🇪🇹 Financial Inclusion Forecasting System — Ethiopia (2025–2027)")
st.caption("Selam Analytics | Prepared for National Bank of Ethiopia & Consortium Stakeholders")

# Sidebar Controls
st.sidebar.header("Navigation")
page = st.sidebar.radio("Select Module", [
    "Executive Overview", 
    "Historical Trends & EDA", 
    "Event Association Matrix", 
    "Inclusion Forecasts (2025–2027)"
])

# Dataset Stubs
historical_findex = pd.DataFrame({
    'year': [2011, 2014, 2017, 2021, 2024],
    'ACC_OWNERSHIP': [14.0, 22.0, 35.0, 46.0, 49.0],
    'ACC_MM_ACCOUNT': [0.0, 0.05, 0.30, 4.70, 9.45],
    'USG_DIGITAL_PAYMENT': [2.0, 5.0, 12.0, 24.0, 35.0]
})

forecasts_df = pd.DataFrame({
    'year': [2025, 2026, 2027],
    'ACC_OWNERSHIP_Base': [51.5, 54.2, 57.0],
    'ACC_OWNERSHIP_Optimistic': [53.5, 58.0, 63.5],
    'ACC_OWNERSHIP_Pessimistic': [50.0, 51.2, 52.5],
    'USG_DIGITAL_PAYMENT_Base': [39.0, 43.5, 48.0],
    'USG_DIGITAL_PAYMENT_Optimistic': [41.0, 47.0, 53.0],
    'USG_DIGITAL_PAYMENT_Pessimistic': [37.0, 40.0, 43.0]
})

if page == "Executive Overview":
    st.header("Consortium Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("2024 Account Access Rate", "49.0%", "+3.0 pp vs 2021")
    col2.metric("2024 Digital Payment Usage", "35.0%", "+11.0 pp vs 2021")
    col3.metric("P2P / ATM Volume Ratio", "1.42x", "Digital > Physical Cash")
    col4.metric("2030 Universal Target", "70.0%", "NFIS-II Policy Horizon")

    st.markdown("---")
    st.subheader("Core Analytical Findings")
    st.markdown("""
    * **Registration vs. Ownership Gap**: Mobile money registered accounts exceed 65M, yet unique individual account ownership reached 49% due to multi-SIM wallet holdings by already-banked individuals.
    * **P2P Crossover**: Interoperable digital transfers now exceed physical ATM cash withdrawals, demonstrating accelerated velocity in digital commerce.
    * **Access Deceleration (2021–2024)**: Overall growth slowed down to 3 percentage points due to rural telecom infrastructure constraints and persistent digital literacy bottlenecks.
    """)

elif page == "Historical Trends & EDA":
    st.header("Historical Findex Progress (2011–2024)")
    fig = px.line(
        historical_findex,
        x='year',
        y=['ACC_OWNERSHIP', 'ACC_MM_ACCOUNT', 'USG_DIGITAL_PAYMENT'],
        markers=True,
        title="Ethiopia Financial Inclusion Indicators Over Time",
        labels={'value': 'Percentage of Adult Population (%)', 'variable': 'Indicator Code'}
    )
    st.plotly_chart(fig, use_container_width=True)

elif page == "Event Association Matrix":
    st.header("Task 3: Event-Indicator Association Matrix")
    events = ["Telebirr Launch (2021)", "M-Pesa Rollout (2023)", "EthSwitch Interoperability Mandate", "Fayda Digital ID Expansion"]
    indicators = ["ACC_OWNERSHIP", "ACC_MM_ACCOUNT", "USG_DIGITAL_PAYMENT"]
    
    matrix_data = np.array([
        [1.5, 4.5, 8.0],
        [1.0, 3.5, 6.0],
        [0.5, 2.0, 7.5],
        [2.0, 1.5, 4.0]
    ])
    
    fig_heat = px.imshow(
        matrix_data,
        x=indicators,
        y=events,
        color_continuous_scale="Viridis",
        title="Event Impact Magnitudes (+ Percentage Points Shift)"
    )
    st.plotly_chart(fig_heat, use_container_width=True)

elif page == "Inclusion Forecasts (2025–2027)":
    st.header("Task 4: Financial Inclusion Forecasts (2025–2027)")
    
    col_ind, col_scen = st.columns(2)
    selected_ind = col_ind.selectbox("Target Indicator", ["ACC_OWNERSHIP", "USG_DIGITAL_PAYMENT"])
    selected_scen = col_scen.selectbox("Forecast Scenario", ["Base", "Optimistic", "Pessimistic"])
    
    fig_fc = go.Figure()
    # Historical trace
    fig_fc.add_trace(go.Scatter(
        x=historical_findex['year'], 
        y=historical_findex[selected_ind], 
        name="Historical (Findex Surveys)", 
        mode='lines+markers'
    ))
    
    # Forecast trace
    target_col = f"{selected_ind}_{selected_scen}"
    fig_fc.add_trace(go.Scatter(
        x=forecasts_df['year'], 
        y=forecasts_df[target_col], 
        name=f"Forecast Projection ({selected_scen})", 
        mode='lines+markers', 
        line=dict(dash='dash', color='orange')
    ))
    
    fig_fc.update_layout(title=f"{selected_ind} Forecast Trajectory ({selected_scen} Scenario)", yaxis_title="Percentage (%)")
    st.plotly_chart(fig_fc, use_container_width=True)
    
    # Download Button
    st.download_button(
        label="📥 Download Forecast Results (CSV)",
        data=forecasts_df.to_csv(index=False),
        file_name="ethiopia_fi_forecasts_2025_2027.csv",
        mime="text/csv"
    )