import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt


def show_dependency_graph(incident=None):
    """
    incident: dict or None
    Example:
    {
        "type": "Database Saturation Cascade",
        "severity": "Critical",
        "affected_services": ["Database", "API", "Payment"]
    }
    """

    graph = nx.DiGraph()

    # System dependency flow
    graph.add_edge("User Traffic", "API Service")
    graph.add_edge("API Service", "Database")
    graph.add_edge("Database", "Payment Service")
    graph.add_edge("Payment Service", "Revenue System")

    # Fixed positions for stable UI
    pos = {
        "User Traffic": (0, 0),
        "API Service": (1.8, 0),
        "Database": (3.6, 0),
        "Payment Service": (5.4, 0),
        "Revenue System": (7.2, 0),
    }

    severity = incident["severity"] if incident else None
    affected_services = incident.get("affected_services", []) if incident else []

    node_colors = []
    edge_colors = []

    for node in graph.nodes():
        if not incident:
            node_colors.append("#b7d7e8")  # normal soft blue
        elif node == "Database":
            if severity == "Critical":
                node_colors.append("#ff4b4b")  # red
            elif severity == "Warning":
                node_colors.append("#f4c542")  # yellow
            else:
                node_colors.append("#b7d7e8")
        elif node in affected_services:
            node_colors.append("#f7a072")  # impacted downstream/upstream service
        else:
            node_colors.append("#b7d7e8")

    for u, v in graph.edges():
        if incident and (u in affected_services or v in affected_services):
            edge_colors.append("#d62728" if severity == "Critical" else "#e0a800")
        else:
            edge_colors.append("#5a5a5a")

    fig, ax = plt.subplots(figsize=(11, 2.8))
    ax.set_facecolor("white")

    nx.draw_networkx_nodes(
        graph,
        pos,
        node_color=node_colors,
        node_size=2600,
        ax=ax,
        edgecolors="#2f2f2f",
        linewidths=1.2
    )

    nx.draw_networkx_edges(
        graph,
        pos,
        ax=ax,
        edge_color=edge_colors,
        width=2.2,
        arrows=True,
        arrowsize=24,
        arrowstyle="-|>"
    )

    nx.draw_networkx_labels(
        graph,
        pos,
        ax=ax,
        font_size=10,
        font_weight="bold"
    )

    ax.set_title("Cloud Service Dependency Flow", fontsize=14, fontweight="bold", pad=14)
    ax.axis("off")
    plt.tight_layout()

    st.pyplot(fig, width="stretch")

    # Optional legend/status text
    if incident:
        severity_badge = "🔴 Critical" if severity == "Critical" else "🟡 Warning"
        st.caption(
            f"{severity_badge} incident path highlighted | "
            f"Affected services: {', '.join(affected_services)}"
        )
    else:
        st.caption("🟢 All services operating in normal dependency flow")