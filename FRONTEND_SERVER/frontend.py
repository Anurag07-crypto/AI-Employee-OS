# =========================================================
# ADVANCED AI EMPLOYEE FRONTEND UI
# =========================================================

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import requests
import uuid
from datetime import datetime
import time
import base64
import html

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Employee OS",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# BACKEND CONFIG
# =========================================================

BACKEND_URL = "http://127.0.0.1:8000"

# =========================================================
# SESSION STATE
# =========================================================

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "pending_interrupt" not in st.session_state:
    st.session_state.pending_interrupt = None

if "selected_agent" not in st.session_state:
    st.session_state.selected_agent = "default_agent"

# =========================================================
# AGENTS
# =========================================================

AGENTS = {
    "default_agent": {
        "name": "🧠 Default Agent",
        "desc": "General AI assistant"
    },

    "code_debugger": {
        "name": "🐞 Code Debugger",
        "desc": "Fix coding errors"
    },

    "code_explainer": {
        "name": "📘 Code Explainer",
        "desc": "Explain code step-by-step"
    },

    "code_reviewer": {
        "name": "🔍 Code Reviewer",
        "desc": "Review and optimize code"
    },

    "dta_bot": {
        "name": "📊 DTA Bot",
        "desc": "Data analysis assistant"
    },

    "websearch_agent": {
        "name": "🌐 WebSearch Agent",
        "desc": "Internet research AI"
    },

    "deepsearch_agent": {
        "name": "🛰️ DeepSearch Agent",
        "desc": "Advanced research system"
    },

    "question_&_answer_agent": {
        "name": "❓ Q&A Agent",
        "desc": "Answer questions intelligently"
    },

    "email_agent": {
        "name": "📧 Email Agent",
        "desc": "Generate professional emails"
    },

    "talkative_agent": {
        "name": "🗣️ Talkative Agent",
        "desc": "Voice chat with your AI best friend"
    }
}

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(circle at top left, #1e293b, #020617);
    color: white;
}

[data-testid="stSidebar"] {
    background: rgba(15,23,42,0.95);
    border-right: 1px solid rgba(255,255,255,0.08);
}

[data-testid="stToolbar"], header, #MainMenu, footer {
    visibility: hidden;
    height: 0;
}

.block-container {
    padding-top: 2rem;
}

.main-title {
    font-size: 54px;
    font-weight: 800;
    background: linear-gradient(90deg,#38bdf8,#818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0;
}

.sub-title {
    color: #94a3b8;
    font-size: 18px;
    margin-top: 0;
}

.glass-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    backdrop-filter: blur(14px);
    border-radius: 22px;
    padding: 20px;
    margin-bottom: 20px;
    transition: 0.3s ease;
}

.glass-card:hover {
    border: 1px solid rgba(56,189,248,0.4);
    transform: translateY(-2px);
}

.workspace-panel {
    background: rgba(15,23,42,0.72);
    border: 1px solid rgba(148,163,184,0.16);
    border-radius: 18px;
    padding: 22px;
    margin-bottom: 18px;
}

.call-panel {
    background: linear-gradient(135deg, rgba(14,165,233,0.16), rgba(16,185,129,0.12));
    border: 1px solid rgba(125,211,252,0.24);
    border-radius: 18px;
    padding: 22px;
    margin-bottom: 16px;
}

.call-title {
    font-size: 24px;
    font-weight: 800;
    margin-bottom: 6px;
}

.call-subtitle {
    color: #cbd5e1;
    font-size: 14px;
    margin-bottom: 0;
}

.live-dot {
    display: inline-block;
    width: 10px;
    height: 10px;
    border-radius: 999px;
    background: #22c55e;
    box-shadow: 0 0 0 6px rgba(34,197,94,0.12);
    margin-right: 8px;
}

.agent-card {
    background: rgba(255,255,255,0.04);
    border-radius: 12px;
    padding: 15px;
    margin-bottom: 12px;
    border: 1px solid rgba(255,255,255,0.06);
}

.response-card {
    background: rgba(15,23,42,0.84);
    border: 1px solid rgba(148,163,184,0.18);
    border-radius: 14px;
    padding: 18px;
    margin: 12px 0 18px 0;
}

.response-label {
    color: #93c5fd;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.response-text {
    color: #e2e8f0;
    font-size: 16px;
    line-height: 1.65;
}

.meta-row {
    color: #94a3b8;
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    font-size: 13px;
    margin-top: 8px;
}

.status-pill {
    background: rgba(34,197,94,0.12);
    border: 1px solid rgba(34,197,94,0.25);
    color: #bbf7d0;
    border-radius: 999px;
    padding: 4px 10px;
}

.empty-chat {
    min-height: 220px;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    color: #94a3b8;
    background: rgba(15,23,42,0.54);
    border: 1px solid rgba(148,163,184,0.14);
    border-radius: 18px;
    padding: 24px;
    margin-bottom: 16px;
}

.empty-chat h2 {
    color: #e2e8f0;
    margin-bottom: 8px;
}

.composer-panel {
    background: rgba(15,23,42,0.82);
    border: 1px solid rgba(148,163,184,0.16);
    border-radius: 18px;
    padding: 16px;
    margin-top: 8px;
}

.agent-chip {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    border-radius: 999px;
    padding: 6px 12px;
    color: #dbeafe;
    background: rgba(37,99,235,0.16);
    border: 1px solid rgba(96,165,250,0.22);
    font-size: 13px;
    margin-bottom: 12px;
}

.chat-user {
    background: linear-gradient(90deg,#2563eb,#3b82f6);
    padding: 16px;
    border-radius: 18px;
    margin-bottom: 10px;
    color: white;
}

.chat-ai {
    background: rgba(255,255,255,0.05);
    padding: 16px;
    border-radius: 18px;
    margin-bottom: 20px;
    border: 1px solid rgba(255,255,255,0.08);
}

.metric-card {
    background: rgba(255,255,255,0.05);
    padding: 18px;
    border-radius: 18px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.08);
}

.stButton button {
    width: 100%;
    border-radius: 14px;
    height: 48px;
    border: none;
    background: linear-gradient(90deg,#2563eb,#7c3aed);
    color: white;
    font-weight: 700;
    transition: 0.3s ease;
}

.stButton button:hover {
    transform: scale(1.02);
}

[data-testid="stChatInput"] {
    background: rgba(15,23,42,0.96);
    border-radius: 18px;
}

textarea {
    border-radius: 16px !important;
    background-color: rgba(15,23,42,0.9) !important;
    color: white !important;
}

.code-box {
    background: #020617;
    border-radius: 16px;
    padding: 15px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<p class="main-title">🤖 AI Employee OS</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="sub-title">Next Generation Multi-Agent AI Workforce System</p>',
    unsafe_allow_html=True
)

# =========================================================
# BACKEND FUNCTIONS
# =========================================================

def send_query(query: str, agent: str):

    try:

        response = requests.post(
            f"{BACKEND_URL}/server",
            json={
                "query": query,
                "agent": agent,
                "thread_id": st.session_state.thread_id
            },
            timeout=120
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.ConnectionError:
        st.error("❌ Backend server is offline")
        return None

    except requests.exceptions.Timeout:
        st.error("⏳ Request timeout")
        return None

    except Exception as e:
        st.error(f"❌ Error: {e}")
        return None


def resume_agent(decision, edited_content=None):

    payload = {
        "decision": decision,
        "thread_id": st.session_state.thread_id
    }

    if edited_content:
        payload["edited_content"] = edited_content

    try:

        response = requests.post(
            f"{BACKEND_URL}/approve",
            json=payload,
            timeout=120
        )

        response.raise_for_status()

        return response.json()

    except Exception as e:
        st.error(f"❌ Resume failed: {e}")
        return None


def send_talkative_audio(uploaded_audio):

    try:
        audio_name = getattr(uploaded_audio, "name", "voice_message.wav")
        audio_type = getattr(uploaded_audio, "type", None) or "audio/wav"

        files = {
            "audio_file": (
                audio_name,
                uploaded_audio.getvalue(),
                audio_type
            )
        }

        data = {
            "thread_id": st.session_state.thread_id
        }

        response = requests.post(
            f"{BACKEND_URL}/talkative",
            files=files,
            data=data,
            timeout=180
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.ConnectionError:
        st.error("❌ Backend server is offline")
        return None

    except requests.exceptions.Timeout:
        st.error("⏳ Talkative agent request timeout")
        return None

    except Exception as e:
        st.error(f"❌ Talkative agent error: {e}")
        return None


def safe_text(value):

    if value is None:
        return ""

    return html.escape(str(value))


def format_time(value):

    try:
        return datetime.fromisoformat(value).strftime("%d %b %Y, %I:%M %p")
    except Exception:
        return str(value)


def render_text_response(response):

    if isinstance(response, dict):
        preferred_keys = ["answer", "response", "result", "output", "content", "message", "text"]
        for key in preferred_keys:
            value = response.get(key)
            if isinstance(value, str) and value.strip():
                st.markdown(value)
                return

        st.json(response)
        return

    if isinstance(response, list):
        st.json(response)
        return

    st.markdown(str(response))


def render_talkative_response(response):

    transcript = safe_text(response.get("transcription"))
    reply = safe_text(response.get("text"))

    st.markdown(
        f"""
        <div class="response-card">
            <div class="response-label">You said</div>
            <div class="response-text">{transcript}</div>
        </div>
        <div class="response-card">
            <div class="response-label">Talkie replied</div>
            <div class="response-text">{reply}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if response.get("audio_bytes"):

        st.audio(
            response["audio_bytes"],
            format=response.get("audio_mime", "audio/wav")
        )


def render_chat_turn(chat):

    with st.chat_message("user"):
        st.markdown(chat["query"])

    avatar = "🗣️" if chat["agent"] == "talkative_agent" else "🤖"

    with st.chat_message("assistant", avatar=avatar):
        st.caption(
            f"{AGENTS[chat['agent']]['name']} · {format_time(chat['timestamp'])}"
        )

        if chat["agent"] == "talkative_agent" and isinstance(chat["response"], dict):
            render_talkative_response(chat["response"])
        else:
            render_text_response(chat["response"])

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## ⚙️ Control Center")

    try:
        requests.get(f"{BACKEND_URL}/docs", timeout=3)
        st.success("🟢 Backend Connected")

    except:
        st.error("🔴 Backend Offline")

    st.markdown("---")

    st.markdown("## 🧠 Select AI Agent")

    selected_agent = st.selectbox(
        "Choose Agent",
        list(AGENTS.keys()),
        format_func=lambda x: AGENTS[x]["name"]
    )

    st.session_state.selected_agent = selected_agent

    st.markdown("---")

    st.markdown("## 🛰️ Available Agents")

    for key, value in AGENTS.items():

        st.markdown(f"""
        <div class="agent-card">
            <h4>{value['name']}</h4>
            <p>{value['desc']}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("## 🧵 Thread ID")

    st.code(st.session_state.thread_id)

    if st.button("🔄 New Conversation"):

        st.session_state.thread_id = str(uuid.uuid4())
        st.session_state.chat_history = []
        st.session_state.pending_interrupt = None

        st.rerun()

    if st.button("🗑️ Clear History"):

        st.session_state.chat_history = []

        st.success("History Cleared")

# =========================================================
# LAYOUT
# =========================================================

left_col, right_col = st.columns([3, 1])

# =========================================================
# LEFT PANEL
# =========================================================

with left_col:

    st.markdown("""
    <div class="workspace-panel">
    <h3>💬 Conversation</h3>
    </div>
    """, unsafe_allow_html=True)

    current_agent_name = safe_text(AGENTS[st.session_state.selected_agent]["name"])
    current_agent_desc = safe_text(AGENTS[st.session_state.selected_agent]["desc"])

    st.markdown(
        f"""
        <div class="agent-chip">{current_agent_name} · {current_agent_desc}</div>
        """,
        unsafe_allow_html=True
    )

    if st.session_state.chat_history:

        for chat in st.session_state.chat_history:
            render_chat_turn(chat)

    else:

        st.markdown(
            """
            <div class="empty-chat">
                <div>
                    <h2>What should we work on?</h2>
                    <p>Choose an agent, send a message, or start a Talkie voice turn.</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    if st.session_state.selected_agent == "talkative_agent":

        st.markdown("""
        <div class="call-panel">
            <div class="call-title"><span class="live-dot"></span>Live Talkie Call</div>
            <p class="call-subtitle">Record one voice turn, send it to Talkie, then listen to the reply.</p>
        </div>
        """, unsafe_allow_html=True)

        call_audio = st.audio_input(
            "Speak to Talkie"
        )

        with st.expander("Upload audio instead"):

            uploaded_audio_file = st.file_uploader(
                "Upload Voice Message",
                type=["wav", "mp3", "m4a", "ogg", "flac", "webm"]
            )

        uploaded_audio = call_audio or uploaded_audio_file
        user_input = ""
        execute_label = "Send Voice Turn"
        execute = st.button(execute_label)

    else:

        uploaded_audio = None

        st.markdown(
            """
            <div class="composer-panel">
                Message your selected agent below.
            </div>
            """,
            unsafe_allow_html=True
        )

        user_input = st.chat_input(
            f"Message {AGENTS[st.session_state.selected_agent]['name']}"
        )
        execute = bool(user_input)

# =========================================================
# RIGHT PANEL
# =========================================================

with right_col:

    st.markdown("""
    <div class="glass-card">
    <h3>📡 System Metrics</h3>
    </div>
    """, unsafe_allow_html=True)

    st.metric(
        "Conversation Count",
        len(st.session_state.chat_history)
    )

    st.metric(
        "Current Agent",
        AGENTS[st.session_state.selected_agent]["name"]
    )

    approval_status = (
        "Pending"
        if st.session_state.pending_interrupt
        else "Idle"
    )

    st.metric(
        "Approval Status",
        approval_status
    )

    st.progress(78)

    st.caption("Workflow Activity")

# =========================================================
# EXECUTION
# =========================================================

if execute:

    if st.session_state.selected_agent == "talkative_agent":

        if uploaded_audio is None:

            st.warning("⚠️ Please upload an audio file")

        else:

            with st.status(
                "🗣️ Talkative Agent Listening...",
                expanded=True
            ) as status:

                st.write("🎙️ Uploading Voice Message...")
                time.sleep(0.5)

                st.write("🧠 Transcribing Audio...")
                time.sleep(0.5)

                st.write("🔊 Generating Voice Reply...")
                time.sleep(0.5)

                response = send_talkative_audio(uploaded_audio)

                if response and response.get("status") == "completed":

                    audio_bytes = base64.b64decode(
                        response.get("audio_base64", "")
                    )

                    status.update(
                        label="✅ Voice Reply Ready",
                        state="complete"
                    )

                    st.session_state.chat_history.append({
                        "query": f"Voice message: {getattr(uploaded_audio, 'name', 'microphone recording')}",
                        "response": {
                            "transcription": response.get("transcription"),
                            "text": response.get("response"),
                            "audio_bytes": audio_bytes,
                            "audio_mime": response.get("audio_mime", "audio/wav")
                        },
                        "agent": st.session_state.selected_agent,
                        "timestamp": str(datetime.now()),
                        "status": "completed"
                    })

                    st.rerun()

    elif not user_input.strip():

        st.warning("⚠️ Please enter a query")

    else:

        with st.status(
            "🤖 AI Agents Executing...",
            expanded=True
        ) as status:

            st.write("🧠 Planning Task...")
            time.sleep(0.5)

            st.write("🌐 Selecting Agent...")
            time.sleep(0.5)

            st.write("⚙️ Executing Workflow...")
            time.sleep(0.5)

            response = send_query(
                query=user_input,
                agent=st.session_state.selected_agent
            )

            if response:

                if response.get("status") == "completed":

                    status.update(
                        label="✅ Task Completed",
                        state="complete"
                    )

                    st.session_state.chat_history.append({
                        "query": user_input,
                        "response": response.get("response"),
                        "agent": st.session_state.selected_agent,
                        "timestamp": str(datetime.now()),
                        "status": "completed"
                    })

                    st.rerun()

                elif response.get("status") == "approval_required":

                    st.session_state.pending_interrupt = response

                    status.update(
                        label="🛑 Approval Required",
                        state="error"
                    )

                    st.warning(
                        "⚠️ Human approval required"
                    )

# =========================================================
# HUMAN APPROVAL SECTION
# =========================================================

if st.session_state.pending_interrupt:

    st.divider()

    st.markdown("""
    <div class="glass-card">
    <h2>🛑 Human Approval Required</h2>
    </div>
    """, unsafe_allow_html=True)

    interrupt_data = st.session_state.pending_interrupt

    st.json(interrupt_data)

    edited_content = st.text_area(
        "✏️ Modify Tool Arguments",
        height=180
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        approve_btn = st.button("✅ Approve")

    with col2:

        edit_btn = st.button("✏️ Approve With Edit")

    with col3:

        reject_btn = st.button("❌ Reject")

    # APPROVE

    if approve_btn:

        result = resume_agent("approve")

        if result:

            st.success("✅ Execution Approved")

            st.session_state.pending_interrupt = None

            st.rerun()

    # EDIT

    if edit_btn:

        result = resume_agent(
            "edit",
            edited_content
        )

        if result:

            st.success("✅ Edited Execution Completed")

            st.session_state.pending_interrupt = None

            st.rerun()

    # REJECT

    if reject_btn:

        result = resume_agent("reject")

        if result:

            st.error("❌ Execution Rejected")

            st.session_state.pending_interrupt = None

            st.rerun()

# =========================================================
# TRANSCRIPT
# =========================================================

st.divider()

with st.expander("Full transcript and run details", expanded=False):

    if st.session_state.chat_history:

        for chat in reversed(st.session_state.chat_history):
            st.markdown(
                f"**{AGENTS[chat['agent']]['name']}** · "
                f"`{chat['status']}` · {format_time(chat['timestamp'])}"
            )
            st.markdown(f"**User:** {chat['query']}")

            if chat["agent"] == "talkative_agent" and isinstance(chat["response"], dict):
                st.markdown(f"**Transcript:** {chat['response'].get('transcription')}")
                st.markdown(f"**Reply:** {chat['response'].get('text')}")
            else:
                render_text_response(chat["response"])

            st.divider()

    else:

        st.info("No transcript yet.")

# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div style='text-align:center;
padding:20px;
color:gray;'>

🚀 AI Employee Operating System<br>
Built with Streamlit + FastAPI + Multi-Agent AI

</div>
""", unsafe_allow_html=True)
