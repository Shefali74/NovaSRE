import pandas as pd
import numpy as np
from datetime import datetime

# Global simulation state
current_state = "healthy"
state_counter = 0


def generate_live_metric():
    global current_state, state_counter

    # -----------------------------------------------------
    # STATE TRANSITIONS
    # healthy -> degrading -> critical -> recovering -> healthy
    # -----------------------------------------------------
    if current_state == "healthy" and state_counter > 20:
        current_state = "degrading"
        state_counter = 0

    elif current_state == "degrading" and state_counter > 20:
        current_state = "critical"
        state_counter = 0

    elif current_state == "critical" and state_counter > 20:
        current_state = "recovering"
        state_counter = 0

    elif current_state == "recovering" and state_counter > 15:
        current_state = "healthy"
        state_counter = 0

    state_counter += 1

    # -----------------------------------------------------
    # METRIC GENERATION BY STATE
    # -----------------------------------------------------
    if current_state == "healthy":
        cpu = np.random.normal(45, 5)
        db_conn = np.random.normal(50, 5)
        latency = np.random.normal(100, 10)
        error = np.random.normal(1, 0.5)
        revenue = np.random.normal(1000, 50)

    elif current_state == "degrading":
        cpu = np.random.normal(65, 5)
        db_conn = np.random.normal(80, 5)
        latency = np.random.normal(200, 20)
        error = np.random.normal(3, 1)
        revenue = np.random.normal(850, 50)

    elif current_state == "critical":
        cpu = np.random.normal(85, 5)
        db_conn = np.random.normal(95, 3)
        latency = np.random.normal(400, 50)
        error = np.random.normal(8, 2)
        revenue = np.random.normal(600, 100)

    else:  # recovering
        cpu = np.random.normal(55, 5)
        db_conn = np.random.normal(65, 5)
        latency = np.random.normal(150, 15)
        error = np.random.normal(2, 1)
        revenue = np.random.normal(900, 50)

    return {
        "timestamp": datetime.now(),
        "api_cpu_percent": round(max(0, min(cpu, 100)), 2),
        "db_connection_usage": round(max(0, min(db_conn, 100)), 2),
        "db_latency_ms": round(max(0, latency), 2),
        "payment_error_rate": round(max(0, error), 2),
        "revenue_per_minute": round(max(0, revenue), 2),
        "state": current_state
    }


def initialize_metrics():
    rows = [generate_live_metric() for _ in range(5)]
    return pd.DataFrame(rows)


def append_new_metric(df):
    metric = generate_live_metric()
    updated_df = pd.concat([df, pd.DataFrame([metric])], ignore_index=True)

    # Keep only the latest 200 rows for performance
    updated_df = updated_df.tail(200).reset_index(drop=True)

    return updated_df