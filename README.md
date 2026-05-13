# AI Employee OS

AI Employee OS is a multi-agent assistant system with a Streamlit GPT-style frontend and a FastAPI backend. It routes user requests to specialized agents for general assistance, coding help, research, data analysis, email automation, and voice conversation.

## Features

- GPT-style Streamlit chat interface
- FastAPI backend with agent routing
- Multiple specialized AI agents
- Voice conversation through the Talkative agent
- Human-in-the-loop email approval flow
- Web research through Tavily
- Tool-using default assistant with calculator, weather, and time tools
- Centralized application logging

## Project Structure

```text
AI_emp/
|-- AGENTS/
|   |-- Coding_agent.py
|   |-- DEFAULT_agent.py
|   |-- DTA.py
|   |-- Email_agent.py
|   |-- Research_agent.py
|   `-- TALKATIVE_agent.py
|-- BACKEND_SERVER/
|   |-- backend.py
|   `-- orchestrator.py
|-- FRONTEND_SERVER/
|   `-- frontend.py
|-- CHAT_HISTORY/
|-- logs/
|-- logger.py
|-- requirements.txt
|-- pyproject.toml
`-- SYSTEM_ARCHITECTURE.md
```

## Agents

| Agent | Key | Purpose |
| --- | --- | --- |
| Default Agent | `default_agent` | General assistant with tools for calculator, weather, and time |
| Code Debugger | `code_debugger` | Helps debug coding issues |
| Code Explainer | `code_explainer` | Explains code and failures |
| Code Reviewer | `code_reviewer` | Reviews code and suggests improvements |
| DTA Bot | `dta_bot` | Analyzes dataset information and business insights |
| WebSearch Agent | `websearch_agent` | Basic Tavily-powered web search |
| DeepSearch Agent | `deepsearch_agent` | Advanced Tavily-powered research |
| Q&A Agent | `question_&_answer_agent` | Tavily Q&A-style research |
| Email Agent | `email_agent` | Generates and sends email with human approval |
| Talkative Agent | `talkative_agent` | Voice input, transcription, short reply, and audio output |

## Requirements

- Python 3.11+
- Groq API key
- Tavily API key, for research agents
- OpenWeather API key, for weather tool
- Gmail app password, for email sending

## Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
weather_api_key=your_openweather_api_key
APP_PASSWORD=your_gmail_app_password
```

Do not commit real secrets.

## Installation

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

If you use `uv`, you can install from `pyproject.toml` instead:

```powershell
uv sync
```

## Running the App

Start the FastAPI backend:

```powershell
.\.venv\Scripts\python.exe -m uvicorn BACKEND_SERVER.backend:app --host 127.0.0.1 --port 8000
```

Start the Streamlit frontend in another terminal:

```powershell
.\.venv\Scripts\python.exe -m streamlit run FRONTEND_SERVER/frontend.py --server.port 8501 --server.address 127.0.0.1
```

Open:

```text
http://127.0.0.1:8501
```

Backend API docs:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

### `POST /server`

Handles text-based agents.

Request:

```json
{
  "query": "Explain this Python error",
  "agent": "code_explainer",
  "thread_id": "optional-thread-id"
}
```

Response:

```json
{
  "status": "completed",
  "response": "Agent response..."
}
```

### `POST /talkative`

Handles audio upload for the Talkative agent.

Form fields:

- `audio_file`: uploaded audio file
- `thread_id`: optional thread id

Response includes:

- `transcription`
- `response`
- `audio_base64`
- `audio_mime`

### `POST /approve`

Resumes the email agent after a human decision.

Request:

```json
{
  "decision": "approve",
  "thread_id": "thread-id"
}
```

Supported decisions:

- `approve`
- `edit`
- `reject`

For edit:

```json
{
  "decision": "edit",
  "thread_id": "thread-id",
  "edited_content": "Updated tool argument or email content"
}
```

## Main Workflows

### Text Agent Workflow

1. User selects an agent in the Streamlit sidebar.
2. User sends a message through the chat input.
3. Frontend calls `POST /server`.
4. Backend looks up the selected agent in `BACKEND_SERVER/orchestrator.py`.
5. Backend invokes the matching agent function.
6. Frontend renders the response in the chat.

### Talkative Voice Workflow

1. User selects Talkative Agent.
2. User records or uploads audio in the frontend.
3. Frontend sends multipart audio to `POST /talkative`.
4. Backend saves the audio under `CHAT_HISTORY/talkative_uploads`.
5. Talkative agent transcribes audio using Groq Whisper.
6. Talkative agent generates a short reply.
7. Talkative agent generates speech audio.
8. Frontend displays the transcript, reply, and audio player.

### Email Approval Workflow

1. User asks the Email Agent to send an email.
2. Email Agent prepares a tool call.
3. Human-in-the-loop middleware interrupts before sending.
4. Frontend shows approval controls.
5. User approves, edits, or rejects.
6. Backend calls `/approve` to resume the agent.
7. Email is sent only if approved.

## Logging

Logs are written to:

```text
logs/app.log
```

The shared logger is defined in:

```text
logger.py
```

## Architecture

See the full architecture document:

[SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md)

It includes Mermaid diagrams for:

- High-level system architecture
- Default agent graph
- Email approval flow
- Talkative voice flow
- Text request flow

## Troubleshooting

### Port 8000 is already in use

Find the process using the port:

```powershell
Get-NetTCPConnection -LocalAddress 127.0.0.1 -LocalPort 8000
```

Stop the process:

```powershell
Stop-Process -Id <PID>
```

Then restart the backend.

### Backend offline in frontend

Make sure FastAPI is running:

```text
http://127.0.0.1:8000/docs
```

### Talkative agent fails

Check:

- `GROQ_API_KEY` exists in `.env`
- backend was restarted after code changes
- uploaded audio format is supported
- `logs/app.log` for detailed traceback

### Email agent fails

Check:

- `APP_PASSWORD` exists in `.env`
- Gmail app password is valid
- receiver email contains `@`
- approval flow was completed

## Current Notes

- Streamlit chat history is session-local.
- Talkative currently writes the latest generated speech to `AGENTS/speech.wav`.
- Email sending is protected by human approval.
- True continuous voice streaming would require WebSocket or WebRTC support.

## License

No license has been specified yet.
