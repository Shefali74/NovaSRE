import json
import boto3
from botocore.config import Config

# Add timeout configuration
bedrock = boto3.client(
    "bedrock-runtime",
    region_name="us-east-1",
    config=Config(
        read_timeout=15,
        connect_timeout=10,
        retries={"max_attempts": 1}
    )
)

MODEL_ID = "amazon.nova-lite-v1:0"


def get_nova_reasoning(incident, latest_metrics):
    incident_type = incident.get("type", "Unknown Incident")
    severity = incident.get("severity", "Unknown")
    affected_services = ", ".join(incident.get("affected_services", []))
    business_impact = incident.get("business_impact", "Unknown impact")

    db_connection_usage = float(latest_metrics.get("db_connection_usage", 0))
    db_latency_ms = float(latest_metrics.get("db_latency_ms", 0))
    api_cpu_percent = float(latest_metrics.get("api_cpu_percent", 0))
    payment_error_rate = float(latest_metrics.get("payment_error_rate", 0))
    revenue_per_minute = float(latest_metrics.get("revenue_per_minute", 0))

    prompt = f"""
You are Nova, an AI cloud reliability engineer.

Analyze the incident and system performance metrics below and provide a concise, structured technical assessment.

Incident Details:
- Incident Type: {incident_type}
- Severity: {severity}
- Affected Services: {affected_services}
- Business Impact: {business_impact}

System Metrics:
- Database Connection Usage: {db_connection_usage:.2f} percent
- Database Latency: {db_latency_ms:.2f} milliseconds
- API CPU Utilization: {api_cpu_percent:.2f} percent
- Payment Error Rate: {payment_error_rate:.2f} percent
- Revenue Throughput: {revenue_per_minute:.2f}

Respond using exactly these sections:

Root Cause:
Explain the likely technical cause of the issue.

System Impact:
Explain which services are affected and how the issue propagates.

Recommended Mitigation:
Provide clear infrastructure or application mitigation steps.
""".strip()

    body = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {"text": prompt}
                ]
            }
        ],
        "inferenceConfig": {
            "max_new_tokens": 300,
            "temperature": 0.2
        }
    }

    try:
        response = bedrock.invoke_model(
            modelId=MODEL_ID,
            body=json.dumps(body),
            contentType="application/json",
            accept="application/json"
        )

        result = json.loads(response["body"].read())
        return result["output"]["message"]["content"][0]["text"]

    except Exception as e:
        return f"""Root Cause:
High database connection usage and latency indicate saturation at the database layer, likely causing slow query execution and increasing load on dependent services.

System Impact:
The database bottleneck affects API responsiveness and payment transaction reliability. This can reduce system throughput and create revenue risk.

Recommended Mitigation:
Scale database resources, optimize connection pooling, reduce expensive queries, and strengthen alerting for latency, connection usage, and payment failure spikes.

Fallback Note:
Live Nova reasoning was unavailable, so the system used built-in resilience analysis instead. Error: {str(e)}
"""