"""
AI Log Analyzer - Azure Function

Purpose:
- Fetch logs from Azure Log Analytics
- Send logs to local LLM (Ollama) for analysis
- Generate structured insights (Incident Summary, Root Cause, Fixes)

Trigger:
- Timer-based (runs every 5 minutes)

Notes:
- Uses Managed Identity for authentication (no secrets in code)
- All configuration (URLs, workspace IDs, model name) is stored in Azure Function App settings
- Calls external VM (Ollama API) over HTTP
"""



import logging
import os
import requests
from datetime import timedelta, datetime
from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient
import azure.functions as func

app = func.FunctionApp()

@app.timer_trigger(schedule="0 */5 * * * *", arg_name="mytimer")
def LogAnalyzer(mytimer: func.TimerRequest) -> None:
    logging.info("Function started")

    workspace_id = os.environ["WORKSPACE_ID"]
    ollama_url = os.environ["OLLAMA_URL"]
    model = os.environ["OLLAMA_MODEL"]

    dce_endpoint = os.environ["DCE_ENDPOINT"]
    ai_insights_dcr_id = os.environ["AI_INSIGHTS_DCR_ID"]
    ai_insights_stream = os.environ["AI_INSIGHTS_STREAM"]

    credential = DefaultAzureCredential()
    client = LogsQueryClient(credential)

    # Query last 30 minutes of logs from App Insights
    # Limiting results to reduce payload size for LLM processing

    query = """
    AppLogsApi_CL
    | where TimeGenerated > ago(1h)
    | project TimeGenerated, LogEntry
    | sort by TimeGenerated desc
    | take 20
    """

    log_response = client.query_workspace(
        workspace_id,
        query,
        timespan=timedelta(hours=1)
    )

    logs = []
    for table in log_response.tables:
        for row in table.rows:
            logs.append(row[1])

    # Combine logs into a single string for LLM input

    log_text = "\n".join(logs)

    if not log_text.strip():
        logging.info("No logs found. Exiting.")
        return

    logging.info("Collected logs")

    # Promp engineered to generate structured output for incident analysis

    prompt = f"""
    You are a cloud support engineer.

    Analyze the following production logs.

    ONLY return structured output in this format:

    1. Incident Summary:
    2. Error Patterns:
    3. Likely Root Cause:
    4. Recommended Fixes:

    Do NOT explain how to analyze logs.
    Do NOT give general advice.

    Logs:
    {log_text}
    """

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    # Sends Logs to Ollama (local LLM running on VM)
    # Timeout increased due to slower inference on small VM

    try:
        ai_response = requests.post(ollama_url, json=payload, timeout=120)
        ai_response.raise_for_status()

        ai_json = ai_response.json()
        analysis = ai_json.get("response", "")

        if not analysis:
            logging.error("Ollama returned no analysis.")
            return

        logging.info("AI analysis generated")

        token = credential.get_token("https://monitor.azure.com/.default").token

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        # Send AI-generated insights back to Log Analytics (custom table)
        # Enables querying and visualization of analysis results

        insight_payload = [
            {
                "TimeGenerated": datetime.utcnow().isoformat() + "Z",
                "Analysis": analysis
            }
        ]

        insight_url = (
            f"{dce_endpoint}/dataCollectionRules/{ai_insights_dcr_id}"
            f"/streams/{ai_insights_stream}?api-version=2023-01-01"
        )

        insight_response = requests.post(
            insight_url,
            headers=headers,
            json=insight_payload,
            timeout=30
        )

        logging.info("AIInsights ingestion status: %s", insight_response.status_code)
        logging.info("AIInsights ingestion response: %s", insight_response.text)

    except Exception as e:
        logging.exception("Pipeline failed")