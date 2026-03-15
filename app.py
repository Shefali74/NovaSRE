import streamlit as st
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# Agents
from agents.detection_agent import detect_incident
from agents.reasoning_agent import get_nova_reasoning
from agents.execution_agent import execute_mitigation
from agents.dependency_agent import show_dependency_graph

# Simulation
from utils.simulation import initialize_metrics, append_new_metric


# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="NovaSRE Autonomous Cloud Self-Healing System",
    layout="wide"
)

st.title("NovaSRE — Autonomous Cloud Self-Healing System")
st.caption("AI-powered incident detection, root-cause reasoning, and self-healing for cloud systems")


# =========================================================
# AUTO REFRESH
# =========================================================
st_autorefresh(interval=2000, key="nova_refresh")


# =========================================================
# SESSION STATE INITIALIZATION
# =========================================================
DEFAULT_SESSION_STATE = {
    "metrics_df": None,
    "logs": [],
    "incident_active": False,
    "warning_active": False,
    "reasoning_done": False,
    "mitigation_done": False,
    "cached_reasoning": None,
    "mitigation_action": None,
    "last_incident_type": None,
    "normal_streak": 0,
}

for key, value in DEFAULT_SESSION_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = initialize_metrics() if key == "metrics_df" else value


# =========================================================
# HELPER FUNCTIONS
# =========================================================
def add_log(message: str):
    timestamp = datetime.now().strftime("%H:%M:%S")
    entry = f"[{timestamp}] {message}"

    if not st.session_state.logs or st.session_state.logs[0] != entry:
        st.session_state.logs.insert(0, entry)

    st.session_state.logs = st.session_state.logs[:20]


def reset_incident_state():
    st.session_state.incident_active = False
    st.session_state.warning_active = False
    st.session_state.reasoning_done = False
    st.session_state.mitigation_done = False
    st.session_state.cached_reasoning = None
    st.session_state.mitigation_action = None
    st.session_state.last_incident_type = None


def reset_critical_only_state():
    st.session_state.incident_active = False
    st.session_state.reasoning_done = False
    st.session_state.mitigation_done = False
    st.session_state.cached_reasoning = None
    st.session_state.mitigation_action = None


def get_health_status(value, warn, crit):
    if value >= crit:
        return "🔴 Critical"
    elif value >= warn:
        return "🟡 Degraded"
    return "🟢 Healthy"


# =========================================================
# LIVE METRIC UPDATE
# =========================================================
st.session_state.metrics_df = append_new_metric(st.session_state.metrics_df)

metrics = st.session_state.metrics_df
latest = metrics.iloc[-1]


# =========================================================
# HEALTH OVERVIEW
# =========================================================
st.header("System Health Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.subheader("API Service")
    st.write(get_health_status(latest["api_cpu_percent"], 70, 85))

with col2:
    st.subheader("Database")
    st.write(get_health_status(latest["db_connection_usage"], 75, 90))

with col3:
    st.subheader("Payment Service")
    st.write(get_health_status(latest["payment_error_rate"], 5, 8))

with col4:
    st.subheader("Revenue Flow")
    st.write(get_health_status(1000 - latest["revenue_per_minute"], 200, 400))


# =========================================================
# LIVE CHART
# =========================================================
st.header("Database Load Over Time")

chart_data = metrics.tail(50)
st.line_chart(
    chart_data.set_index("timestamp")["db_connection_usage"],
    use_container_width=True
)


# =========================================================
# INCIDENT DETECTION
# =========================================================
incident = detect_incident(metrics)


# =========================================================
# DEPENDENCY GRAPH
# =========================================================
st.header("System Dependency Graph")
show_dependency_graph(incident=incident)


# =========================================================
# INCIDENT / WARNING / NORMAL FLOW
# =========================================================
if incident:
    st.session_state.normal_streak = 0
    severity = incident.get("severity", "").lower()
    incident_type = incident.get("type", "Unknown Incident")

    # -----------------------------------------------------
    # WARNING FLOW
    # -----------------------------------------------------
    if severity == "warning":
        st.warning(f"Warning Detected: {incident_type}")

        if (
            not st.session_state.warning_active
            or st.session_state.last_incident_type != incident_type
        ):
            st.session_state.warning_active = True
            st.session_state.last_incident_type = incident_type
            add_log(f"WARNING Early signal detected: {incident_type}")

        st.info(
            "NovaSRE is monitoring the degraded database state. "
            "Autonomous mitigation will trigger if conditions become critical."
        )

        reset_critical_only_state()

    # -----------------------------------------------------
    # CRITICAL FLOW
    # -----------------------------------------------------
    elif severity == "critical":
        st.error(f"Critical Incident Detected: {incident_type}")

        if (
            not st.session_state.incident_active
            or st.session_state.last_incident_type != incident_type
        ):
            st.session_state.incident_active = True
            st.session_state.warning_active = False
            st.session_state.reasoning_done = False
            st.session_state.mitigation_done = False
            st.session_state.cached_reasoning = None
            st.session_state.mitigation_action = None
            st.session_state.last_incident_type = incident_type

            add_log(f"CRITICAL Incident detected: {incident_type}")

        if not st.session_state.reasoning_done:
            with st.spinner("Nova AI analyzing root cause..."):
                st.session_state.cached_reasoning = get_nova_reasoning(incident, latest)
            st.session_state.reasoning_done = True
            add_log("INFO Nova reasoning completed")

        st.header("Nova AI Root Cause Analysis")
        st.caption("Generated live using Amazon Nova via Amazon Bedrock")

        if st.session_state.cached_reasoning and "Fallback Note:" in st.session_state.cached_reasoning:
            st.warning("Live Nova response was unavailable. Showing built-in fallback reasoning.")
        else:
            st.success("Live Nova reasoning active")

        st.markdown(st.session_state.cached_reasoning)

        if not st.session_state.mitigation_done:
            healed_metrics, mitigation_action = execute_mitigation(metrics, incident)
            st.session_state.metrics_df = healed_metrics
            st.session_state.mitigation_action = mitigation_action
            st.session_state.mitigation_done = True
            add_log(f"ACTION {mitigation_action}")

        st.header("Autonomous Mitigation Execution")
        st.success(f"Mitigation applied: {st.session_state.mitigation_action}")


# =========================================================
# NORMAL FLOW
# =========================================================
else:
    st.session_state.normal_streak += 1
    st.success("System operating normally")

    # Recovery confirmation only after stable normal readings
    if st.session_state.normal_streak >= 3:
        if st.session_state.incident_active or st.session_state.warning_active:
            add_log("SUCCESS System stabilized and returned to normal operating state")

        reset_incident_state()


# =========================================================
# EVENT LOGS
# =========================================================
st.header("Autonomous System Event Log")

for log in st.session_state.logs[:15]:
    st.info(log)


# =========================================================
# RAW METRICS
# =========================================================
with st.expander("View Raw Live Metrics"):
    st.dataframe(metrics.tail(20), use_container_width=True)