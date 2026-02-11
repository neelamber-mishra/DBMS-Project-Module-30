# src/modules/m30/seed.py
"""
Seed the MongoDB database with realistic sample data for all 4 collections.
Run standalone:  python -m src.modules.m30.seed
"""

import os
import random
from datetime import datetime, timedelta
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".env"))

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://sandeep172918:password@sandeep.dhrneuu.mongodb.net/?appName=sandeep")
DB_NAME = os.getenv("MONGO_DB_NAME", "m30_timeseries")

PATIENT_IDS = [f"P-{str(i).zfill(4)}" for i in range(1, 11)]
FREQUENCIES = ["Minutes", "Hourly", "Daily", "Weekly", "Monthly"]
PATTERN_TYPES = ["Spikes", "Dips", "Plateau", "Oscillation", "Gradual Rise", "Gradual Fall"]
DIRECTIONS = ["Increasing", "Decreasing"]
CYCLE_PERIODS = ["Circadian", "Weekly", "Monthly", "Seasonal", "Annual"]
METRIC_NAMES = ["Heart Rate", "Blood Pressure Systolic", "Blood Pressure Diastolic",
                "Temperature", "SpO2", "Respiratory Rate", "Blood Glucose", "Weight"]

METRIC_BASELINES = {
    "Heart Rate": (60, 100),
    "Blood Pressure Systolic": (100, 140),
    "Blood Pressure Diastolic": (60, 90),
    "Temperature": (97.0, 99.5),
    "SpO2": (94, 100),
    "Respiratory Rate": (12, 20),
    "Blood Glucose": (70, 140),
    "Weight": (55, 95),
}


def generate_data_points(metric: str, frequency: str, count: int = 50):
    """Generate realistic time-series data points for a given metric."""
    low, high = METRIC_BASELINES.get(metric, (50, 150))
    base = random.uniform(low, high)
    freq_delta = {
        "Minutes": timedelta(minutes=5),
        "Hourly": timedelta(hours=1),
        "Daily": timedelta(days=1),
        "Weekly": timedelta(weeks=1),
        "Monthly": timedelta(days=30),
    }
    delta = freq_delta.get(frequency, timedelta(hours=1))
    start = datetime(2025, 1, 1, 8, 0, 0)

    points = []
    value = base
    for i in range(count):
        noise = random.gauss(0, (high - low) * 0.05)
        trend = random.uniform(-0.1, 0.15)
        spike = random.gauss(0, (high - low) * 0.3) if random.random() < 0.05 else 0
        value = max(low * 0.8, min(high * 1.2, value + noise + trend + spike))
        ts = start + delta * i
        points.append({
            "timestamp": ts.isoformat(),
            "value": round(value, 2),
            "metric": metric,
        })
    return points, start, start + delta * (count - 1)


def seed():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]

    for col_name in ["time_series", "patterns", "trends", "seasonality"]:
        db[col_name].drop()
    print("🗑️  Cleared existing collections.")

    series_docs = []
    pattern_docs = []
    trend_docs = []
    season_docs = []

    series_counter = 1
    pattern_counter = 1
    trend_counter = 1
    season_counter = 1

    for patient_id in PATIENT_IDS:
        num_series = random.randint(2, 4)
        metrics = random.sample(METRIC_NAMES, num_series)

        for metric in metrics:
            freq = random.choice(FREQUENCIES)
            points, start_time, end_time = generate_data_points(metric, freq, count=random.randint(30, 80))

            series_id = f"TS-{str(series_counter).zfill(4)}"
            series_counter += 1

            series_docs.append({
                "series_id": series_id,
                "patient_id": patient_id,
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "frequency": freq,
                "metric": metric,
                "data_points": points,
            })

            for _ in range(random.randint(1, 3)):
                pattern_docs.append({
                    "pattern_id": f"PAT-{str(pattern_counter).zfill(4)}",
                    "series_id": series_id,
                    "pattern_type": random.choice(PATTERN_TYPES),
                    "significance_score": round(random.uniform(0.1, 1.0), 2),
                })
                pattern_counter += 1

            for _ in range(random.randint(1, 2)):
                trend_docs.append({
                    "trend_id": f"TRD-{str(trend_counter).zfill(4)}",
                    "series_id": series_id,
                    "direction": random.choice(DIRECTIONS),
                    "slope_value": round(random.uniform(-2.0, 2.0), 3),
                })
                trend_counter += 1

            if random.random() > 0.3:
                season_docs.append({
                    "season_id": f"SEA-{str(season_counter).zfill(4)}",
                    "series_id": series_id,
                    "cycle_period": random.choice(CYCLE_PERIODS),
                })
                season_counter += 1

    if series_docs:
        db["time_series"].insert_many(series_docs)
    if pattern_docs:
        db["patterns"].insert_many(pattern_docs)
    if trend_docs:
        db["trends"].insert_many(trend_docs)
    if season_docs:
        db["seasonality"].insert_many(season_docs)

    print(f"✅ Seeded {len(series_docs)} time-series, {len(pattern_docs)} patterns, "
          f"{len(trend_docs)} trends, {len(season_docs)} seasonality records.")
    client.close()


if __name__ == "__main__":
    seed()
