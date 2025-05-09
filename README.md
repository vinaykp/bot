# AI Bot with Multiple Agents

A FastAPI-based AI bot that uses multiple specialized agents to handle different types of queries including search, time/weather information, and inventory management.

## Features

- **Control Agent**: Routes queries to appropriate specialized agents
- **Search Agent**: Handles general search queries using Google Search
- **Weather & Time Agent**: Provides weather and time information for cities
- **Inventory Management Agent**: Complete CRUD operations for inventory items using SQLite

## Prerequisites

- Python 3.8+
- pip package manager
- Google API key or Vertex AI authentication

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd bot
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
Create a `.env` file with:
```
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=your_api_key_here
```

## Usage

1. Start the server:
```bash
python main.py
```

The server will start on `http://0.0.0.0:9999`

## API Endpoints

- `GET /health`: Health check endpoint
- `GET /agent-info`: Get information about the control agent
- Additional endpoints provided by ADK Web UI

## Project Structure

```
bot/
├── main.py                 # FastAPI application entry point
├── control_agent/         # Control agent for routing queries
├── search_agent/         # Google search agent
├── multi_tool_agent/     # Weather and time agent
├── inventory_agent/      # Inventory management agent
└── requirements.txt      # Project dependencies
```

## Agent Capabilities

### Control Agent
- Routes queries to appropriate specialized agents based on query content

### Search Agent
- Performs Google searches using the Google ADK

### Weather & Time Agent
- Provides weather information for cities
- Returns current time in different timezones

### Inventory Agent
- Create new inventory items
- Read single or all items (with optional filters)
- Update existing items
- Delete items
- Persistent storage using SQLite

## Development

The project uses:
- FastAPI for the web framework
- Google ADK for AI agent functionality
- SQLite for inventory data storage
- Uvicorn as the ASGI server

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

[Add your license information here]