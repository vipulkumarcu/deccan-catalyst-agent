import streamlit as st
import os
import json
import time
from datetime import datetime
from agents.catalyst_agent import CatalystAgent
from tools.file_ops import extract_text

# ==========================================
# 1. PAGE CONFIGURATION & ASSETS
# ==========================================
st.set_page_config(page_title="Nexus AI", layout="wide")

USER_ICON = "https://cdn-icons-png.flaticon.com/512/9187/9187532.png"
AGENT_ICON = "https://cdn-icons-png.flaticon.com/512/8744/8744028.png"

# ==========================================
# 2. NEXUS TOOLBOX (REGISTER YOUR TOOLS HERE)
# ==========================================

# EXAMPLE TOOL: Learning Roadmap Generator
# 1. Define the Schema (What the AI reads)
ROADMAP_SCHEMA = {
    "type": "function",
    "function": {
        "name": "get_learning_roadmap",
        "description": "Generates a list of high-quality resources for a specific technical skill gap.",
        "parameters": {
            "type": "object",
            "properties": {
                "skill": {"type": "string", "description": "The skill to research (e.g., 'Docker', 'FastAPI')."}
            },
            "required": ["skill"]
        }
    }
}

# 2. Define the Logic (The actual Python code)
def get_learning_roadmap(skill):
    # This is where you'd call a real API or search a database
    # For the demo, we return structured mock data
    return {
        "skill": skill,
        "resources": [
            f"Official {skill} Documentation",
            f"Advanced {skill} Course on Coursera",
            f"Nexus AI Hands-on Lab: Mastering {skill}"
        ],
        "estimated_time": "2 weeks"
    }

# ==========================================
# 3. NEXUS SYSTEM STYLING (CSS) - UNTOUCHED
# ==========================================
st.markdown(f"""
    <style>
    /* Global Branding */
    .nexus-gradient {{
        font-weight: 800;
        background: -webkit-linear-gradient(#00d4ff, #0072ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
    }}
    .sidebar-nexus {{ font-size: 2.8rem; margin-top: -60px; margin-bottom: 0px; }}
    .main-nexus {{ font-size: 7rem; margin-bottom: 0px; line-height: 1; text-align: center; }}
    .tagline {{ text-align: center; color: #888; font-size: 1.1rem; margin-top: -10px; }}

    /* VIBRANT BLUE BUTTONS (New & Initialize) */
    .stButton>button.vibrant-btn {{
        border-radius: 12px;
        background: linear-gradient(90deg, #00d4ff 0%, #0072ff 100%) !important;
        color: white !important; border: none !important; font-weight: 600 !important;
        box-shadow: 0 4px 15px rgba(0, 114, 255, 0.3);
        height: 48px; width: 240px !important; transition: 0.3s;
    }}

    /* CHAT PILLS - SIDEBAR NAVIGATION */
    .chat-pill-wrapper {{
        display: flex; align-items: center; justify-content: space-between;
        border-radius: 10px; margin-bottom: 6px; padding: 2px 8px;
        transition: all 0.2s ease; position: relative; width: 100%;
    }}
    .chat-pill-wrapper:hover {{ background-color: #1f2937 !important; }}

    button[kind="primary"] {{
        border-top: none !important;
    }}

    .chat-pill-wrapper button {{
        background: transparent !important; border: none !important;
        text-align: left !important; padding: 12px 16px !important;
        border-radius: 8px !important; width: 100% !important;
        box-shadow: none !important; height: auto !important; min-height: 44px;
    }}

    [data-testid="stPopover"] > button {{
        background: transparent !important; border: none !important;
        color: #94a3b8 !important; opacity: 0 !important;
        transition: opacity 0.2s ease; font-size: 1.3rem; padding: 8px 4px;
    }}
    .chat-pill-wrapper:hover [data-testid="stPopover"] > button {{ opacity: 1 !important; }}

    [data-testid="stPopover"] button[kind="secondary"] {{
        background: transparent !important; border: none !important;
        font-weight: 500; text-align: left; padding: 10px 16px;
    }}
    [data-testid="stPopover"] button[kind="secondary"]:hover {{ background-color: #7f1d1d !important; }}

    hr {{ margin: 12px 0 !important; border-top: 1px solid rgba(255,255,255,0.1); }}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 4. STATE INITIALIZATION & TOOL PLUGINS
# ==========================================
if "agent" not in st.session_state:
    # 1. Instantiate the Brain
    st.session_state.agent = CatalystAgent()

    # 2. PLUG IN THE TOOLS (Register them here)
    st.session_state.agent.tools.register_tool(ROADMAP_SCHEMA, get_learning_roadmap)

    st.session_state.messages = []
    st.session_state.current_session_id = None

# ==========================================
# 5. SIDEBAR NAVIGATION
# ==========================================
with st.sidebar:
    st.markdown('<h1 class="nexus-gradient sidebar-nexus">NEXUS</h1>', unsafe_allow_html=True)
    st.markdown('<p class="tagline">Decoding Potential. Architecting Mastery.</p>', unsafe_allow_html=True)

    st.markdown('<div class="centered-btn stButton">', unsafe_allow_html=True)
    if st.button("New Assessment", key="new_as_btn"):
        st.session_state.agent = CatalystAgent()
        # Register tools again for the new agent instance
        st.session_state.agent.tools.register_tool(ROADMAP_SCHEMA, get_learning_roadmap)
        st.session_state.messages = []
        st.session_state.current_session_id = None
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("Chats")

    if not os.path.exists("sessions"):
        os.makedirs("sessions")

    history_files = sorted(os.listdir("sessions"), reverse=True)

    for file in history_files:
        s_id = file.replace('.json', '')
        s_name = s_id.split('_')[0]
        is_active = (st.session_state.current_session_id == s_id)

        st.markdown('<div class="chat-pill-wrapper">', unsafe_allow_html=True)
        col_text, col_menu = st.columns([5, 1])

        with col_text:
            if st.button(
                f"{s_name}",
                key=f"btn_{file}",
                use_container_width=True,
                type="primary" if is_active else "secondary"
            ):
                with open(f"sessions/{file}", "r") as f:
                    data = json.load(f)
                    st.session_state.messages = data.get("messages", [])
                    st.session_state.agent.resume_text = data.get("resume", "")
                    st.session_state.agent.jd_text = data.get("jd", "")
                    st.session_state.current_session_id = s_id
                st.rerun()

        with col_menu:
            with st.popover("⋮", use_container_width=True):
                if st.button("Delete", key=f"del_{file}", use_container_width=True):
                    if os.path.exists(f"sessions/{file}"):
                        os.remove(f"sessions/{file}")
                    if st.session_state.current_session_id == s_id:
                        st.session_state.current_session_id = None
                        st.session_state.agent = CatalystAgent()
                        # Register tools again
                        st.session_state.agent.tools.register_tool(ROADMAP_SCHEMA, get_learning_roadmap)
                        st.session_state.messages = []
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

st.components.v1.html("""
    <script>
    const btns = window.parent.document.querySelectorAll('button');
    btns.forEach(btn => {
        if (btn.innerText === "New Assessment" || btn.innerText === "Initialize Assessment") {
            btn.classList.add('vibrant-btn');
        }
    });
    </script>
""", height=0)

# ==========================================
# 6. MAIN INTERFACE
# ==========================================
if not st.session_state.current_session_id or not st.session_state.agent.resume_text:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('<h1 class="nexus-gradient main-nexus">NEXUS</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #888; font-size:1.2rem; margin-top:-15px;">Decoding Potential. Architecting Mastery.</p>', unsafe_allow_html=True)

    u_col1, u_col2, u_col3 = st.columns([1, 2, 1])
    with u_col2:
        st.markdown("<hr>", unsafe_allow_html=True)
        res_file = st.file_uploader("Upload Resume", type=["pdf", "docx", "txt"])
        jd_file = st.file_uploader("Upload Job Description", type=["pdf", "docx", "txt"])

        st.markdown('<div class="init-container stButton">', unsafe_allow_html=True)
        if st.button("Initialize Assessment", key="init_btn"):
            if res_file and jd_file:
                with st.spinner("Decoding Skills DNA..."):
                    res_txt = extract_text(res_file)
                    jd_txt = extract_text(jd_file)
                    st.session_state.agent.set_context(res_txt, jd_txt)
                    title = st.session_state.agent.generate_chat_title()
                    s_id = f"{title}_{datetime.now().strftime('%H%M')}"
                    st.session_state.current_session_id = s_id

                    first_msg = st.session_state.agent.get_response("Briefly highlight top matches and critical gaps.")
                    st.session_state.messages.append({"role": "assistant", "content": first_msg})

                    with open(f"sessions/{s_id}.json", "w") as f:
                        json.dump({
                            "title": title, "resume": res_txt,
                            "jd": jd_txt, "messages": st.session_state.messages
                        }, f)
                    st.rerun()
            else:
                st.error("Please provide both documents.")
        st.markdown('</div>', unsafe_allow_html=True)

else:
    s_display = st.session_state.current_session_id.split('_')[0]
    st.markdown(f"### <span style='color:#00d4ff'>Assessment:</span> {s_display}", unsafe_allow_html=True)

    for message in st.session_state.messages:
        av = AGENT_ICON if message["role"] == "assistant" else USER_ICON
        with st.chat_message(message["role"], avatar=av):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask a question or type here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar=USER_ICON):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar=AGENT_ICON):
            msg_p = st.empty()
            with st.spinner("Thinking..."):
                response = st.session_state.agent.get_response(prompt)
                msg_p.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})

        session_file = f"sessions/{st.session_state.current_session_id}.json"
        with open(session_file, "w") as f:
            json.dump({
                "title": s_display, "resume": st.session_state.agent.resume_text,
                "jd": st.session_state.agent.jd_text, "messages": st.session_state.messages
            }, f)