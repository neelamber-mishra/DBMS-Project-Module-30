# src/modules/m30/m30_page.py
"""
Streamlit page for Module 30: Time-Series Patient Health Data System.
Slim orchestrator — each tab lives in its own file under tabs/.
"""

import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from src.modules.m30.tabs.home import render_home_tab
from src.modules.m30.tabs.collections import render_collections_tab
from src.modules.m30.tabs.analytics import render_analytics_tab
from src.modules.m30.tabs.er_diagram import render_er_diagram_tab
from src.modules.m30.tabs.queries import render_queries_tab
from src.modules.m30.tabs.predictions import render_predictions_tab


def render_m30_page():

    st.markdown("# 📊 E6 — Time-Series Patient Health Data System")
    st.markdown("*Temporal data analysis · Pattern recognition · Trend detection · Prognosis prediction*")
    st.divider()

    tab_home, tab_collections, tab_analytics, tab_er, tab_queries, tab_predictions = st.tabs(
        ["🏠 Home", "📋 Collections", "📊 Analytics", "🔗 ER Diagram", "🔍 Queries", "🔮 Predictions"]
    )

    with tab_home:
        render_home_tab()
    with tab_collections:
        render_collections_tab()
    with tab_analytics:
        render_analytics_tab()
    with tab_er:
        render_er_diagram_tab()
    with tab_queries:
        render_queries_tab()
    with tab_predictions:
        render_predictions_tab()

    st.divider()
    if st.button("⬅ Back to ICU & Real-Time Monitoring"):
        st.session_state.view = "category"
        st.rerun()
