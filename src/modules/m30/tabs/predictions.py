# src/modules/m30/tabs/predictions.py
import streamlit as st
import pandas as pd
from src.modules.m30.db import get_distinct_series_ids, agg_prediction_trend, METRICS

def render_predictions_tab():
    st.header("🔮 Time-Series Predictions")
    st.markdown("""
    This tab uses linear regression to forecast future patient health metrics based on historical trends.
    """)

    series_ids = get_distinct_series_ids()
    if not series_ids:
        st.warning("No time-series data available for predictions.")
        return

    col1, col2 = st.columns(2)
    with col1:
        selected_series = st.selectbox("Select Series ID", series_ids, key="pred_series")
    with col2:
        selected_metric = st.selectbox("Select Metric", METRICS, key="pred_metric")

    forecast_steps = st.slider("Forecast Steps", 5, 50, 10)

    actual, predicted = agg_prediction_trend(selected_series, selected_metric, forecast_steps)

    if not actual:
        st.info("Insufficient data for prediction in this series.")
        return

    # Prepare data for plotting
    df_actual = pd.DataFrame(actual)
    df_actual['Type'] = 'Actual'
    
    df_predicted = pd.DataFrame(predicted)
    df_predicted['Type'] = 'Predicted'
    
    df_combined = pd.concat([df_actual, df_predicted])
    
    st.subheader(f"Forecast for {selected_metric}")
    
    # Plotting
    chart_data = df_combined.pivot(index='Timestamp', columns='Type', values='Value')
    st.line_chart(chart_data)

    st.markdown("""
    ### Prediction Logic
    The system uses a **Simple Linear Regression** model ($y = mx + b$) calculated over the historical data points:
    1.  **Slope ($m$):** Calculated using the least squares method.
    2.  **Intercept ($b$):** Derived from the mean of the values.
    3.  **Forecast:** Extrapolates the trend line into the future based on the average time interval between existing data points.
    """)
