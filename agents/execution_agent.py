def execute_mitigation(metrics_df, incident=None):
    healed_metrics = metrics_df.copy()
    rows_to_fix = min(10, len(healed_metrics))

    if rows_to_fix == 0:
        return healed_metrics, "No mitigation applied because no metrics were available"

    db_usage_col = healed_metrics.columns.get_loc("db_connection_usage")
    db_latency_col = healed_metrics.columns.get_loc("db_latency_ms")
    payment_error_col = healed_metrics.columns.get_loc("payment_error_rate")
    revenue_col = healed_metrics.columns.get_loc("revenue_per_minute")
    api_cpu_col = healed_metrics.columns.get_loc("api_cpu_percent")

    mitigation_action = "Applied generic infrastructure optimization"

    if incident and incident.get("type") == "Database Saturation Cascade":
        mitigation_action = "Scaled database resources and optimized connection pooling"

        for i in range(-rows_to_fix, 0):
            healed_metrics.iloc[i, db_usage_col] *= 0.70
            healed_metrics.iloc[i, db_latency_col] *= 0.60
            healed_metrics.iloc[i, payment_error_col] *= 0.50
            healed_metrics.iloc[i, revenue_col] *= 1.20
            healed_metrics.iloc[i, api_cpu_col] *= 0.85

    else:
        mitigation_action = "Applied baseline service optimization"

        for i in range(-rows_to_fix, 0):
            healed_metrics.iloc[i, db_usage_col] *= 0.85
            healed_metrics.iloc[i, db_latency_col] *= 0.80
            healed_metrics.iloc[i, payment_error_col] *= 0.80
            healed_metrics.iloc[i, revenue_col] *= 1.10
            healed_metrics.iloc[i, api_cpu_col] *= 0.92

    return healed_metrics, mitigation_action