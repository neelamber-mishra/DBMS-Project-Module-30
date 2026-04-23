# src/modules/m30/tabs/er_diagram.py
import streamlit as st
import os

def render_er_diagram_tab():
    st.header("🔗 Entity Relationship Diagram")
    st.markdown("""
    The following ER diagram illustrates the schema for the **Time-Series Patient Health Data System**.
    It shows the relationships between patient records, time-series data, patterns, trends, and seasonality.
    """)
    
    # Path to the ER diagram image
    img_path = os.path.join(os.path.dirname(__file__), "..", "er_diagram.png")
    
    if os.path.exists(img_path):
        st.image(img_path, caption="M30 ER Diagram", use_container_width=True)
    else:
        st.error("ER Diagram image not found.")
        st.info(f"Expected path: {img_path}")
