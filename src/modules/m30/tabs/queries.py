# src/modules/m30/tabs/queries.py
import streamlit as st
import pandas as pd
from src.modules.m30.db import (
    agg_pattern_frequency,
    agg_trend_summary,
    agg_series_count_by_frequency,
    agg_anomaly_count_by_series
)

def render_queries_tab():
    st.header("🔍 Complex MongoDB Queries")
    st.markdown("""
    This tab demonstrates complex MongoDB aggregation pipelines used to extract insights from the patient health data.
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("1. Pattern Frequency Analysis")
        st.markdown("*Groups patterns by type and calculates average significance.*")
        patterns = agg_pattern_frequency()
        if patterns:
            df_patterns = pd.DataFrame(patterns)
            df_patterns.columns = ["Pattern Type", "Count", "Avg Significance"]
            st.dataframe(df_patterns, use_container_width=True)
            st.code("""
pipeline = [
    {"$group": {"_id": "$Pattern_Type", "count": {"$sum": 1},
                 "avg_significance": {"$avg": "$Significance_Score"}}},
    {"$sort": {"count": -1}},
]
            """, language="python")
        else:
            st.info("No pattern data found.")

    with col2:
        st.subheader("2. Trend Direction Summary")
        st.markdown("*Summarizes trends by direction and average slope.*")
        trends = agg_trend_summary()
        if trends:
            df_trends = pd.DataFrame(trends)
            df_trends.columns = ["Direction", "Count", "Avg Slope"]
            st.dataframe(df_trends, use_container_width=True)
            st.code("""
pipeline = [
    {"$group": {"_id": "$Direction", "count": {"$sum": 1},
                 "avg_slope": {"$avg": "$Slope_Value"}}},
    {"$sort": {"count": -1}},
]
            """, language="python")
        else:
            st.info("No trend data found.")

    st.divider()

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("3. Series Count by Frequency")
        st.markdown("*Distribution of time-series data by sampling frequency.*")
        freqs = agg_series_count_by_frequency()
        if freqs:
            df_freqs = pd.DataFrame(freqs)
            df_freqs.columns = ["Frequency", "Count"]
            st.bar_chart(df_freqs.set_index("Frequency"))
        else:
            st.info("No frequency data found.")

    with col4:
        st.subheader("4. Anomaly Count by Series")
        st.markdown("*Identifies series with the highest number of anomalies.*")
        anomalies = agg_anomaly_count_by_series()
        if anomalies:
            df_anomalies = pd.DataFrame(anomalies)
            df_anomalies.columns = ["Series ID", "Anomaly Count"]
            st.dataframe(df_anomalies, use_container_width=True)
        else:
            st.info("No anomaly data found.")
