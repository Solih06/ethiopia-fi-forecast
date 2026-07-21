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
    "Inclusion Forecasts & Policy Targets",
    "Channel & Demographic Breakdown"
])

# Stub Datasets
historical_findex = pd.DataFrame({
    'year': [2011, 2014, 2017, 2021, 2024],
    'ACC_OWNERSHIP': [14.0, 22.0, 35.0, 46.0, 49.0],
    'ACC_MM_ACCOUNT': [0.0, 0.05, 0.30, 4.70, 9.45],
    'USG_DIGITAL_PAYMENT': [2.0, 5.0, 12.0, 24.0, 35.0]
})

forecasts_df = pd.DataFrame({
    'year': [2025, 2026, 2027],
    'base': [51.5, 54.2, 57.0],
    'optimistic': [53.5, 58.0, 63.5],
    'pessimistic': [50.0, 51.2, 52.5],
    'ci_lower_95': [48.0, 50.5, 52.0],
    'ci_upper_95': [55.0, 58.0, 62.0]
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

elif page == "Inclusion Forecasts & Policy Targets":
    st.header("Task 4: Financial Inclusion Fan Chart vs. Policy Targets")
    
    st.info("""
    💡 **Stakeholder Guide & Scenario Definitions**:
    * **Baseline Scenario**: Continuous trend based purely on historical Global Findex trajectory without additional policy shocks.
    * **Base Scenario**: Incorporates planned policy interventions (Fayda Digital ID rollout, full M-Pesa expansion).
    * **Optimistic Scenario (+8%)**: Assumes rapid infrastructure deployment, 100% Fayda integration, and high rural adoption.
    * **Pessimistic Scenario (-8%)**: Reflects macro tailwinds, delayed network coverage expansions, or reduced consumer trust.
    * **Shaded Fan Band (95% CI)**: Illustrates model uncertainty around forecasts relative to **National Financial Inclusion Strategy (NFIS-II)** targets (60% by 2027, 70% by 2030).
    """)

    # Interactive Fan Chart
    fig_fan = go.Figure()

    # Historical
    fig_fan.add_trace(go.Scatter(
        x=historical_findex['year'], y=historical_findex['ACC_OWNERSHIP'],
        name='Historical (Findex)', mode='lines+markers', line=dict(color='blue', width=3)
    ))

    # Upper/Lower CI (Fan Band)
    fig_fan.add_trace(go.Scatter(
        x=forecasts_df['year'], y=forecasts_df['ci_upper_95'],
        mode='lines', line=dict(width=0), showlegend=False
    ))
    fig_fan.add_trace(go.Scatter(
        x=forecasts_df['year'], y=forecasts_df['ci_lower_95'],
        mode='lines', line=dict(width=0), fill='tonexty',
        fillcolor='rgba(255, 165, 0, 0.25)', name='95% Confidence Band'
    ))

    # Scenarios
    fig_fan.add_trace(go.Scatter(
        x=forecasts_df['year'], y=forecasts_df['base'],
        name='Base Forecast', mode='lines+markers', line=dict(color='orange', width=2, dash='dash')
    ))
    fig_fan.add_trace(go.Scatter(
        x=forecasts_df['year'], y=forecasts_df['optimistic'],
        name='Optimistic Scenario', mode='lines+markers', line=dict(color='green', width=2, dash='dot')
    ))
    fig_fan.add_trace(go.Scatter(
        x=forecasts_df['year'], y=forecasts_df['pessimistic'],
        name='Pessimistic Scenario', mode='lines+markers', line=dict(color='red', width=2, dash='dot')
    ))

    # NFIS Policy Target Reference Line
    fig_fan.add_hline(y=60.0, line_dash="solid", line_color="purple", annotation_text="2027 NFIS-II Target (60%)")

    fig_fan.update_layout(
        title="Account Ownership Forecast (2025–2027) with Uncertainty Fan Band vs. Policy Targets",
        xaxis_title="Year", yaxis_title="Account Ownership Rate (%)"
    )
    st.plotly_chart(fig_fan, use_container_width=True)

elif page == "Channel & Demographic Breakdown":
    st.header("Forecast Breakdown by Provider Channel & Demographics")
    
    col_a, col_b = st.columns(2)
    
    # Provider Channel Distribution Chart
    with col_a:
        st.subheader("Mobile Money vs Traditional Bank Channels")
        channel_df = pd.DataFrame({
            'Channel': ['Commercial Banks', 'Telebirr (Ethio Telecom)', 'M-Pesa (Safaricom)', 'MFIs & Cooperatives'],
            'Share_2024': [42, 38, 12, 8],
            'Projected_Share_2027': [35, 43, 16, 6]
        })
        fig_chan = px.bar(
            channel_df, x='Channel', y=['Share_2024', 'Projected_Share_2027'],
            barmode='group', title="Market Share Shift by Channel (2024 vs 2027 Projected %)",
            labels={'value': 'Market Share (%)', 'variable': 'Period'}
        )
        st.plotly_chart(fig_chan, use_container_width=True)

    # Gender Inclusion Gap Chart
    with col_b:
        st.subheader("Gender Disaggregated Access Gap")
        gender_df = pd.DataFrame({
            'Year': [2017, 2021, 2024, 2027],
            'Male': [41.0, 56.0, 58.0, 65.0],
            'Female': [29.0, 36.0, 40.0, 49.0]
        })
        fig_gen = px.line(
            gender_df, x='Year', y=['Male', 'Female'], markers=True,
            title="Gender Gap Projection in Account Access (2017–2027)",
            labels={'value': 'Inclusion Rate (%)', 'variable': 'Gender Segment'}
        )
        st.plotly_chart(fig_gen, use_container_width=True)