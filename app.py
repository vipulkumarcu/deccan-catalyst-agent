# import streamlit as st
# import os
# import json
# import time
# from datetime import datetime
# from agents.catalyst_agent import CatalystAgent
# from tools.file_ops import extract_text

# st.set_page_config(page_title="NEXUS", page_icon="🎯", layout="wide")

# # CSS: Refined Sidebar & Nexus Branding
# st.markdown("""
#     <style>
#     .nexus-text { font-weight: 800; background: -webkit-linear-gradient(#00d4ff, #0072ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
#     .sidebar-nexus { font-size: 2rem; margin-bottom: 0px; text-align: center; }
#     .main-nexus { font-size: 4rem; text-align: center; }
#     .stButton>button { border-radius: 6px; background: #1a73e8; color: white; border: none; transition: 0.2s; }
#     .stButton>button:hover { background: #1557b0; color: white; }
#     /* Delete button style */
#     .delete-btn>button { background: #30363d !important; color: #ff4b4b !important; border: 1px solid #ff4b4b !important; font-size: 0.8rem !important; height: 2rem !important; }
#     </style>
# """, unsafe_allow_html=True)

# if "agent" not in st.session_state:
#     st.session_state.agent = CatalystAgent()
#     st.session_state.messages = []
#     st.session_state.current_session_id = None

# # 3. Sidebar with Delete Functionality
# with st.sidebar:
#     st.markdown('<h1 class="nexus-text sidebar-nexus">NEXUS</h1>', unsafe_allow_html=True)
#     st.markdown('<p style="color:#888; font-size:0.9rem; margin-top:-10px; text-align: center;">Bridging Ambition & Mastery</p>', unsafe_allow_html=True)

#     if st.button("➕ New Assessment", use_container_width=True):
#         st.session_state.agent = CatalystAgent()
#         st.session_state.messages = []
#         st.session_state.current_session_id = None
#         st.rerun()

#     st.markdown("---")
#     st.subheader("Recent Sessions")
#     if not os.path.exists("sessions"): os.makedirs("sessions")

#     history_files = sorted(os.listdir("sessions"), reverse=True)
#     for file in history_files:
#         col1, col2 = st.columns([4, 1])
#         session_name = file.replace('.json', '').split('_')[0]

#         with col1:
#             if st.button(f"📄 {session_name}", key=f"load_{file}", use_container_width=True):
#                 with open(f"sessions/{file}", "r") as f:
#                     data = json.load(f)
#                     st.session_state.messages = data.get("messages", [])
#                     st.session_state.agent.resume_text = data.get("resume", "")
#                     st.session_state.agent.jd_text = data.get("jd", "")
#                     st.session_state.current_session_id = file.replace('.json', '')
#                 st.rerun()
#         with col2:
#             st.markdown('<div class="delete-btn">', unsafe_allow_html=True)
#             if st.button("🗑️", key=f"del_{file}"):
#                 os.remove(f"sessions/{file}")
#                 if st.session_state.current_session_id == file.replace('.json', ''):
#                     st.session_state.current_session_id = None
#                 st.rerun()
#             st.markdown('</div>', unsafe_allow_html=True)

# # 4. Main UI Logic
# if not st.session_state.agent.resume_text:
#     st.markdown("<br><br>", unsafe_allow_html=True)
#     st.markdown('<h1 class="nexus-text main-nexus">NEXUS</h1>', unsafe_allow_html=True)
#     st.markdown('<p style="text-align: center; color: #888; margin-top:-20px;">Decoding Potential. Architecting Mastery.</p>', unsafe_allow_html=True)

#     col1, col2, col3 = st.columns([1, 2, 1])
#     with col2:
#         st.markdown("---")
#         res_file = st.file_uploader("Upload Candidate Resume", type=["pdf", "docx", "txt"])
#         jd_file = st.file_uploader("Upload Job Description", type=["pdf", "docx", "txt"])

#         if st.button("Initialize Assessment", use_container_width=True):
#             if res_file and jd_file:
#                 with st.spinner("Decoding Skills DNA..."):
#                     res_txt = extract_text(res_file)
#                     jd_txt = extract_text(jd_file)
#                     st.session_state.agent.set_context(res_txt, jd_txt)

#                     # Generate spaced title
#                     title = st.session_state.agent.generate_chat_title()
#                     session_id = f"{title}_{datetime.now().strftime('%H%M')}"
#                     st.session_state.current_session_id = session_id

#                     # TRIGGER INITIAL ANALYSIS IMMEDIATELY
#                     first_msg = st.session_state.agent.get_response("Provide a brief initial assessment of matched skills and primary gaps.")
#                     st.session_state.messages.append({"role": "assistant", "content": first_msg})

#                     with open(f"sessions/{session_id}.json", "w") as f:
#                         json.dump({
#                             "title": title, "resume": res_txt, "jd": jd_txt,
#                             "messages": st.session_state.messages
#                         }, f)
#                     st.rerun()
#             else:
#                 st.error("Please provide both documents.")

# else:
#     # --- CHAT SCREEN ---
#     session_display_name = st.session_state.current_session_id.split('_')[0]
#     st.markdown(f"### <span style='color:#00d4ff'>Assessment:</span> {session_display_name}", unsafe_allow_html=True)

#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])

#     if prompt := st.chat_input("Ask about gaps or verify skills..."):
#         st.session_state.messages.append({"role": "user", "content": prompt})
#         response = st.session_state.agent.get_response(prompt)
#         st.session_state.messages.append({"role": "assistant", "content": response})

#         # Sync to file
#         session_file = f"sessions/{st.session_state.current_session_id}.json"
#         with open(session_file, "w") as f:
#             json.dump({
#                 "title": session_display_name,
#                 "resume": st.session_state.agent.resume_text,
#                 "jd": st.session_state.agent.jd_text,
#                 "messages": st.session_state.messages
#             }, f)
#         st.rerun()







import streamlit as st
import os
import json
import time
from datetime import datetime
from agents.catalyst_agent import CatalystAgent
from tools.file_ops import extract_text

st.set_page_config(page_title="NEXUS", page_icon="🎯", layout="wide")

# NEXUS PRO CSS
st.markdown("""
    <style>
    /* Branding & Header */
    .nexus-text { font-weight: 800; background: -webkit-linear-gradient(#00d4ff, #0072ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .sidebar-nexus { font-size: 1.8rem; text-align: center; margin-top: -30px; } /* Reduced top margin */
    .main-nexus { font-size: 3.5rem; text-align: center; margin-bottom: 0px; }

    /* Buttons */
    .stButton>button {
        border-radius: 8px; background: #1a73e8; color: white; border: none;
        font-weight: 500; height: 40px; transition: 0.3s;
    }
    .stButton>button:hover { background: #1557b0; transform: scale(1.02); }

    /* Sidebar Session Buttons */
    .session-btn button {
        background: transparent !important; color: #ccc !important;
        border: 1px solid #333 !important; text-align: left !important;
        font-size: 0.85rem !important; overflow: hidden; text-overflow: ellipsis;
    }
    .session-btn button:hover { border-color: #00d4ff !important; color: #fff !important; }

    /* Delete Button - Compact Red */
    .delete-btn button {
        background: transparent !important; color: #ff4b4b !important;
        border: none !important; padding: 0px !important; margin-top: 5px !important;
    }

    /* Chat Input Customization */
    .stChatInputContainer { border-radius: 25px !important; }
    </style>
""", unsafe_allow_html=True)

if "agent" not in st.session_state:
    st.session_state.agent = CatalystAgent()
    st.session_state.messages = []
    st.session_state.current_session_id = None

# --- SIDEBAR OVERHAUL ---
with st.sidebar:
    st.markdown('<h1 class="nexus-text sidebar-nexus">NEXUS</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#666; font-size:0.8rem; margin-top:-10px;">Bridging Ambition & Mastery</p>', unsafe_allow_html=True)

    # Compact New Assessment Button
    col_a, col_b, col_c = st.columns([1, 6, 1])
    with col_b:
        if st.button("➕ New Assessment", use_container_width=True):
            st.session_state.agent = CatalystAgent()
            st.session_state.messages = []
            st.session_state.current_session_id = None
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("History")

    if not os.path.exists("sessions"): os.makedirs("sessions")
    history_files = sorted(os.listdir("sessions"), reverse=True)

    for file in history_files:
        session_name = file.replace('.json', '').split('_')[0]
        # Clean Sidebar Alignment
        s_col1, s_col2 = st.columns([5, 1])
        with s_col1:
            st.markdown('<div class="session-btn">', unsafe_allow_html=True)
            if st.button(f" {session_name}", key=f"l_{file}", use_container_width=True):
                with open(f"sessions/{file}", "r") as f:
                    data = json.load(f)
                    st.session_state.messages = data.get("messages", [])
                    st.session_state.agent.resume_text = data.get("resume", "")
                    st.session_state.agent.jd_text = data.get("jd", "")
                    st.session_state.current_session_id = file.replace('.json', '')
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with s_col2:
            st.markdown('<div class="delete-btn">', unsafe_allow_html=True)
            if st.button("🗑️", key=f"d_{file}"):
                os.remove(f"sessions/{file}")
                if st.session_state.current_session_id == file.replace('.json', ''):
                    st.session_state.current_session_id = None
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# --- MAIN LOGIC ---
if not st.session_state.agent.resume_text:
    # --- UPLOAD SCREEN (The "Hero" View) ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('<h1 class="nexus-text main-nexus">NEXUS</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #888; margin-top:-10px;">Decoding Potential. Architecting Mastery.</p>', unsafe_allow_html=True)

    u_col1, u_col2, u_col3 = st.columns([1, 2, 1])
    with u_col2:
        st.markdown("---")
        res_file = st.file_uploader("Upload Resume", type=["pdf", "docx", "txt"])
        jd_file = st.file_uploader("Upload Job Description", type=["pdf", "docx", "txt"])

        if st.button("Initialize Assessment", use_container_width=True):
            if res_file and jd_file:
                with st.spinner("Analyzing DNA..."):
                    res_txt = extract_text(res_file)
                    jd_txt = extract_text(jd_file)
                    st.session_state.agent.set_context(res_txt, jd_txt)
                    title = st.session_state.agent.generate_chat_title()
                    session_id = f"{title}_{datetime.now().strftime('%H%M')}"
                    st.session_state.current_session_id = session_id

                    # Initial prompt
                    first_msg = st.session_state.agent.get_response("Briefly highlight top matches and critical gaps.")
                    st.session_state.messages.append({"role": "assistant", "content": first_msg})

                    with open(f"sessions/{session_id}.json", "w") as f:
                        json.dump({"title": title, "resume": res_txt, "jd": jd_txt, "messages": st.session_state.messages}, f)
                    st.rerun()

else:
    # --- CHAT SCREEN ---
    s_name = st.session_state.current_session_id.split('_')[0]
    st.markdown(f"### <span style='color:#00d4ff'>Assessment:</span> {s_name}", unsafe_allow_html=True)

    # Display message history with CUSTOM ICONS
    for message in st.session_state.messages:
        # User = 👤 | Agent = 🧬
        icon = "🧬" if message["role"] == "assistant" else "👤"
        with st.chat_message(message["role"], avatar=icon):
            st.markdown(message["content"])

    # CHAT INPUT LOGIC (Immediate display)
    if prompt := st.chat_input("Ask a question or type here..."):
        # 1. Immediately show user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

        # 2. Show spinner while generating
        with st.chat_message("assistant", avatar="🧬"):
            msg_placeholder = st.empty()
            with st.spinner("Thinking..."):
                response = st.session_state.agent.get_response(prompt)
                msg_placeholder.markdown(response)

        # 3. Save to state and file
        st.session_state.messages.append({"role": "assistant", "content": response})
        session_file = f"sessions/{st.session_state.current_session_id}.json"
        with open(session_file, "w") as f:
            json.dump({
                "title": s_name,
                "resume": st.session_state.agent.resume_text,
                "jd": st.session_state.agent.jd_text,
                "messages": st.session_state.messages
            }, f)