import os
import sys
import uvicorn
from fastapi import FastAPI
from google.adk.cli.fast_api import get_fast_api_app
from dotenv import load_dotenv
from control_agent import root_agent

# Set up paths
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
AGENT_DIR = BASE_DIR  # Parent directory containing multi_tool_agent

# Set up DB path for sessions
DB_FILE = os.path.join(BASE_DIR, 'bot_sessions.db')
SESSION_DB_URL = f"sqlite:///{DB_FILE}"
# Initialize SQLite database

# Create the FastAPI app using ADK's helper
app: FastAPI = get_fast_api_app(
    agent_dir=AGENT_DIR,
    session_db_url=SESSION_DB_URL,
    allow_origins=["*"],  # In production, restrict this
    web=True,  # Enable the ADK Web UI
)

# Add custom endpoints
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/agent-info")
async def agent_info():
    """Provide agent information"""

    return {
        "agent_name": root_agent.name,
        "description": root_agent.description,
        "model": root_agent.model,
        "tools": [tool.name for tool in root_agent.tools],
    }

if __name__ == "__main__":
    # Run as web server (default)
    print("Starting Web server mode...")
    uvicorn.run(
            app, 
            host="0.0.0.0", 
            port=9999, 
            reload=False
    )