# src/modules/m30/tabs/analytics.py
"""Tab 5 — Analytics: Moving averages, trends, patterns, rate of change, seasonality."""

import streamlit as st
import pandas as pd
from src.modules.m30.db import (
    METRICS,
    get_distinct_series_ids,
    get_time_series_by_series_id,
    get_trends_by_series,
    get_patterns_by_series,
    get_seasonality_by_series,
    agg_moving_average,
    agg_rate_of_change,
)


def render_analytics_tab():
    st.markdown("### 📊 Time-Series Analytics Dashboard")

    series_ids = get_distinct_series_ids()
    if not series_ids:
        st.warning("No time-series data available.")
        return

    selected_sid = st.selectbox("Select Series_ID for analysis", series_ids, key="m30_analytics_series")
    metric = st.selectbox("Select Metric", METRICS, key="m30_analytics_metric")

    # Basic info
    data = get_time_series_by_series_id(selected_sid, limit=5)
    if data:
        d = data[0]
        st.markdown(f"**Patient:** {d.get('Patient_ID', 'N/A')} | **Frequency:** {d.get('Frequency', 'N/A')} | **Metric:** {metric}")
    st.divider()

    # Three-column analysis
    col_ma, col_trend, col_pattern = st.columns(3)

    with col_ma:
        st.markdown("#### 📉 Moving Average")
        ma_data = agg_moving_average(selected_sid, metric, 5)
        if ma_data:
            df = pd.DataFrame(ma_data)
            st.line_chart(df.set_index("Timestamp")[["Value", "Moving_Avg"]])
        else:
            st.caption("No data")

    with col_trend:
        st.markdown("#### 📈 Trends")
        trends = get_trends_by_series(selected_sid)
        if trends:
            for t in trends:
                icon = {"Increasing": "🔼", "Decreasing": "🔽", "Stable": "➡️"}.get(t.get("Direction", ""), "•")
                st.markdown(f"{icon} **{t.get('Metric', '?')}** — {t.get('Direction', '?')} (slope: `{t.get('Slope_Value', 0):.4f}`)")
        else:
            st.caption("No trends detected")

    with col_pattern:
        st.markdown("#### 🔍 Patterns")
        patterns = get_patterns_by_series(selected_sid)
        if patterns:
            for p in patterns[:10]:
                st.markdown(f"• **{p.get('Pattern_Type', '?')}** ({p.get('Metric', '?')}) — score: `{p.get('Significance_Score', 0):.2f}`")
            if len(patterns) > 10:
                st.caption(f"...and {len(patterns) - 10} more")
        else:
            st.caption("No patterns detected")

    st.divider()

    # Rate of change
    st.markdown("#### ⚡ Rate of Change")
    roc_data = agg_rate_of_change(selected_sid, metric)
    if roc_data:
        df_roc = pd.DataFrame(roc_data)
        st.line_chart(df_roc.set_index("Timestamp")["Pct_Change"])
    else:
        st.caption("Not enough data points")

    st.divider()

    # Seasonality
    st.markdown("#### 🔄 Seasonality")
    seasonality = get_seasonality_by_series(selected_sid)
    if seasonality:
        for s in seasonality:
            st.info(f"🔄 **{s.get('Metric', '?')}** — Cycle: **{s.get('Cycle_Period', '?')}** | Amplitude: `{s.get('Max_Amplitude', 0):.2f}`")
    else:
        st.caption("No seasonality data for this series")
