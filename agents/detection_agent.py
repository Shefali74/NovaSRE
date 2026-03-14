def detect_incident(metrics_df):
    latest = metrics_df.iloc[-1]

    db_connection_usage = float(latest["db_connection_usage"])
    db_latency_ms = float(latest["db_latency_ms"])
    payment_error_rate = float(latest["payment_error_rate"])
    api_cpu_percent = float(latest["api_cpu_percent"])
    revenue_per_minute = float(latest["revenue_per_minute"])

    # -----------------------------------------------------
    # CRITICAL INCIDENT
    # Strong multi-signal failure pattern
    # -----------------------------------------------------
    if (
        db_connection_usage > 90 and
        db_latency_ms > 300 and
        payment_error_rate > 5
    ):
        return {
            "type": "Database Saturation Cascade",
            "severity": "Critical",
            "affected_services": ["Database", "API", "Payment"],
            "business_impact": "Revenue degradation likely",
            "trigger_metrics": {
                "db_connection_usage": db_connection_usage,
                "db_latency_ms": db_latency_ms,
                "payment_error_rate": payment_error_rate,
                "api_cpu_percent": api_cpu_percent,
                "revenue_per_minute": revenue_per_minute
            }
        }

    # -----------------------------------------------------
    # WARNING INCIDENT
    # Early stress signals before full outage
    # -----------------------------------------------------
    elif (
        db_connection_usage > 80 and
        db_latency_ms > 180
    ):
        return {
            "type": "Database Stress Warning",
            "severity": "Warning",
            "affected_services": ["Database", "API"],
            "business_impact": "Potential service degradation if trend continues",
            "trigger_metrics": {
                "db_connection_usage": db_connection_usage,
                "db_latency_ms": db_latency_ms,
                "payment_error_rate": payment_error_rate,
                "api_cpu_percent": api_cpu_percent,
                "revenue_per_minute": revenue_per_minute
            }
        }

    return None