# src/modules/m30/db.py
"""
MongoDB database layer for Module 30: Time-Series Patient Health Data System.
Adapted to the existing medicare_db schema.
Collections: time_series, patterns, trends, seasonality
"""

import os
import streamlit as st
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from datetime import datetime, timedelta
from dotenv import load_dotenv
import statistics

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".env"))

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("MONGO_DB_NAME", "medicare_db")

METRICS = ["HeartRate", "SystolicBP", "DiastolicBP", "Temperature"]


@st.cache_resource
def get_client():
    client = MongoClient(MONGO_URI)
    try:
        client.admin.command("ping")
    except ConnectionFailure:
        st.error("❌ Could not connect to MongoDB. Check your connection string.")
        return None
    return client


def get_db():
    client = get_client()
    if client is None:
        return None
    return client[DB_NAME]

def col_time_series():
    return get_db()["time_series"]

def col_patterns():
    return get_db()["patterns"]

def col_trends():
    return get_db()["trends"]

def col_seasonality():
    return get_db()["seasonality"]


def get_distinct_series_ids():
    return sorted(col_time_series().distinct("Series_ID"))


def get_distinct_patient_ids():
    return sorted(col_time_series().distinct("Patient_ID"))