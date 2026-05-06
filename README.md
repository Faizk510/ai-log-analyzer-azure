🚀 AI Log Analyzer (Azure + Ollama)  

Automated cloud observability solution that analyzes production logs and generates structured insights using a local AI model.  

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

📌 Overview

This project simulates a real-world cloud support scenario where production logs are analyzed to:

- Detect recurring errors and failures  
- Identify root causes  
- Recommend actionable fixes  

The system integrates Azure services with a local LLM (Ollama) to automate log analysis and improve incident response efficiency.

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 🎯 Why This Matters

In production environments, log analysis is often manual, time-consuming, and reactive.

This project demonstrates how AI can:
- Reduce incident triage time
- Detect patterns across large log datasets
- Provide structured insights for faster root cause analysis

This is directly applicable to cloud support and production operations roles.

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

🏗 Architecture

![Architecture Diagram](architecture/ai-log-analyzer-architecture.png)  


---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

⚙️ How It Works  

1. Azure Function (Timer Trigger) runs on a scheduled interval (every 5 minutes)  
2. Queries logs from Azure Log Analytics (KQL)  
3. Sends logs to Ollama API (running on VM)  
4. AI model analyzes logs and generates structured output  
5. Results are written back to Log Analytics (custom table)  

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

📊 End-to-End Flow (Proof)  

Azure Resources Overview

![Azure Resources](images/azure-architecture-resources.png)  


## 🖥 Infrastructure Setup (Azure VM (Ollama Host) + Networking) 


![Azure VM](images/Azure-VM.png)


NSG Configuration (Port 11434)  

- NSG configured to allow inbound traffic on port 11434 for Ollama API access  

![Azure VNet NSG](images/Azure-VM-NSG.png)

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

🔍 Log Collection (KQL)

- Azure Log Analytics Workspace, AppLogsAPI_CL table collects application logs and AIInsights_CL table ingests AI Analysis from LLM, creating a feedback loop for monitoring and investigation

- Raw application logs collected from Azure Log Analytics

![Azure Log Analytics_logs](images/log-analytics-applogs.png)  

- AI-generated insights stored in custom AIInsights table

![Azure Log Analytics_aiinsights](images/log-analytics-aiinsights.png)

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

🤖 AI Analysis (Ollama)  

Ollama Running

- Locally run LLM tool (Ollama), hosted on Linux VM, showing version and port information

![Ollama Version](images/ollama-version.png)

![Ollama Port](images/ollama-port.png)


API Test  

- Performed test run locally by calling Ollama api to generate AI analysis  

![Ollama API_Test](images/ollama-curl.png)

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

🧠 AI Output (Insights Table)  

📡 Function Execution & Observability  

- Function execution logs showing successful log retrieval and processing

![Azure Function_Insights_table](images/funcapp-appinsights-log-analytics.png)  

- API interaction with Ollama model, including request/response flow  

![Azure Function_Insights_Ollama_log](images/funcapp-appinsights-log-ollama.png)  

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

⚙️ Function App Implementation  

-  Key components of the Function App are shown below. Full implementation is available in the repository under /function-code.

![Azure Function_app_code](images/functionapp-code.png)


---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

🔧 Configuration  

## 🔧 Function Configuration (Environment Variables)  

- Application settings used to configure Log Analytics workspace, Ollama endpoint, and model parameters via environment variables  

![Azure Function_App_settings](images/functionapp_appsettings.png)

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

🛠 Tech Stack  

- Azure Functions (Python, Timer Trigger)  
- Azure Log Analytics (KQL)  
- Azure Virtual Machine (Ollama – Local LLM)  
- Azure Monitor / Data Collection Rules (DCR/DCE)  
- Python (API integration & automation)

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

🔐 Security (Lab Context)  

- Managed Identity used (no secrets in code)  
- Configuration stored in Function App settings  
- NSG used to control access to Ollama API  

⚠️ Lab Limitation  
- Public access was temporarily enabled for subscription plan limitation.  

⚠️ Production Recommendation

- Use VNet integration for Function App  
- Use private endpoints instead of public IP  
- Restrict NSG rules to internal traffic only

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  
🚧 Challenges & Learnings

- Handling connectivity between Azure Function and VM  
- Managing LLM response latency on limited compute  
- Designing structured AI prompts for consistent output  
- Balancing cost vs performance for cloud resources  

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

🚀 Production Enhancements  

To scale this solution for real-world enterprise environments:  

- Replace VM-hosted Ollama with managed AI services (Azure OpenAI)  
- Implement private endpoints and remove public access entirely  
- Add retry logic and circuit breaker patterns for API reliability  
- Introduce alerting and incident integration (PagerDuty / ServiceNow)  
- Enable autoscaling and workload distribution for high-volume log ingestion  

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

📂 Code

Function implementation available here:

function-code/log_analyzer_functionapp.py  

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

👨‍💻 Author

Faiz Qaiser Khan  
Cloud Support Engineer | Azure | Production Operations
