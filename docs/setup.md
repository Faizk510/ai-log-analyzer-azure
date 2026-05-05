Setup Notes (Lab)  

This project was built using Azure resources and a locally hosted LLM (Ollama).  

Key Components 

- Azure Function App (Timer Trigger)
- Azure Log Analytics Workspace
- Azure VM (Ollama)
- Data Collection Endpoint (DCE)
- Data Collection Rule (DCR)  

Key Steps  

- Deploy Azure VM and install Ollama  
- Open port 11434 via NSG for API access  
- Create Log Analytics workspace  
- Configure Function App with Managed Identity  
- Store configuration in Function App settings  
- Deploy Python function  
- Validate logs and AI output  

Notes  

- Public access was used for lab simplicity
- Production setup would use private networking
