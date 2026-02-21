import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(layout="wide", page_title="MedZentic — Assistant", page_icon="🫀")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400;1,600&family=DM+Sans:wght@300;400;500&family=DM+Mono:wght@300;400&display=swap');

:root {
  --cream:   #F7F3EE;
  --warm:    #EDE8E0;
  --sage:    #7B9E87;
  --sage-lt: #EAF2EC;
  --clay:    #C4856A;
  --clay-lt: #F8EDE7;
  --ink:     #1C1917;
  --ink2:    #44403C;
  --dust:    #A8A29E;
  --white:   #FEFCFA;
  --user-bg: #1C1917;
  --ai-bg:   #FEFCFA;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"] {
  background: var(--cream) !important;
  color: var(--ink) !important;
  font-family: 'DM Sans', sans-serif !important;
}

#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stSidebarNav"],
section[data-testid="stSidebar"] { display: none !important; }

[data-testid="stAppViewContainer"] > .main { padding: 0 !important; }
[data-testid="stAppViewContainer"] > .main > div {
  padding: 0 48px 100px !important;
  max-width: 860px !important;
  margin: 0 auto !important;
}

/* ── NAV ── */
.nav {
  display: flex; align-items: center; justify-content: space-between;
  padding: 28px 0;
  border-bottom: 1px solid var(--warm);
  margin-bottom: 52px;
  animation: fadeDown 0.5s ease both;
}
.nav-logo { display: flex; align-items: center; gap: 10px; }
.nav-mark { width: 34px; height: 34px; background: var(--sage); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 16px; }
.nav-name { font-family: 'Playfair Display', serif; font-size: 19px; font-weight: 700; color: var(--ink); letter-spacing: -0.3px; }
.nav-name em { font-style: normal; color: var(--sage); }
.nav-center { font-family: 'DM Mono', monospace; font-size: 11px; letter-spacing: 1.5px; text-transform: uppercase; color: var(--dust); }
.nav-status { display: flex; align-items: center; gap: 7px; font-size: 12px; font-weight: 500; color: var(--sage); }
.nav-dot { width: 7px; height: 7px; background: var(--sage); border-radius: 50%; animation: breathe 3s ease-in-out infinite; }
@keyframes breathe { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:.4;transform:scale(.8)} }

/* ── CHAT HEADER ── */
.chat-header {
  text-align: center;
  padding: 8px 0 44px;
  animation: fadeUp 0.6s ease 0.1s both;
}
.chat-avatar {
  width: 64px; height: 64px; border-radius: 50%;
  background: var(--ink);
  display: flex; align-items: center; justify-content: center;
  margin: 0 auto 20px;
  font-size: 28px;
  box-shadow: 0 8px 24px rgba(28,25,23,0.2);
  position: relative;
}
.chat-avatar::after {
  content: '';
  position: absolute; inset: -4px;
  border-radius: 50%;
  border: 1.5px solid rgba(123,158,135,0.3);
  animation: ringPulse 3s ease-in-out infinite;
}
@keyframes ringPulse {
  0%,100% { transform: scale(1); opacity: 0.5; }
  50% { transform: scale(1.12); opacity: 0.15; }
}
.chat-h1 {
  font-family: 'Playfair Display', serif;
  font-size: 28px; font-weight: 700; color: var(--ink);
  letter-spacing: -0.5px; margin-bottom: 8px;
}
.chat-sub {
  font-family: 'DM Mono', monospace; font-size: 10px;
  letter-spacing: 1.5px; text-transform: uppercase; color: var(--dust);
}

/* ── MESSAGES ── */
.msgs { display: flex; flex-direction: column; gap: 20px; margin-bottom: 32px; animation: fadeUp 0.6s ease 0.15s both; }

.msg { display: flex; gap: 12px; align-items: flex-start; }
.msg.user { flex-direction: row-reverse; }

.msg-av {
  width: 32px; height: 32px; border-radius: 50%; flex-shrink: 0;
  display: flex; align-items: center; justify-content: center;
  font-family: 'DM Mono', monospace; font-size: 9px; letter-spacing: 0.5px;
  font-weight: 400;
}
.msg-av.user-av { background: var(--ink); color: rgba(255,255,255,0.6); }
.msg-av.ai-av { background: var(--sage); color: white; }

.msg-content { max-width: 80%; }
.msg-who {
  font-family: 'DM Mono', monospace; font-size: 8px; letter-spacing: 2px;
  text-transform: uppercase; margin-bottom: 7px;
}
.msg.user .msg-who { color: var(--dust); text-align: right; }
.msg.ai   .msg-who { color: var(--sage); }

.bubble {
  padding: 14px 18px; border-radius: 18px;
  font-size: 14px; line-height: 1.75; font-weight: 300;
}
.user-bubble {
  background: var(--ink); color: rgba(255,255,255,0.85);
  border-bottom-right-radius: 4px;
}
.ai-bubble {
  background: var(--white); color: var(--ink2);
  border: 1px solid var(--warm);
  border-bottom-left-radius: 4px;
  border-left: 2.5px solid var(--sage);
}

/* ── EMPTY STATE ── */
.empty-state {
  border: 1.5px dashed rgba(168,162,158,0.3);
  border-radius: 20px; padding: 60px 40px;
  text-align: center; margin-bottom: 32px;
  animation: fadeUp 0.6s ease 0.2s both;
}
.empty-icon { font-size: 36px; margin-bottom: 14px; }
.empty-title { font-family: 'DM Mono', monospace; font-size: 10px; letter-spacing: 2px; text-transform: uppercase; color: var(--dust); }

/* ── INPUT AREA ── */
.input-wrap {
  background: var(--white);
  border: 1px solid var(--warm);
  border-radius: 100px;
  padding: 4px 4px 4px 24px;
  display: flex; align-items: center; gap: 10px;
  transition: border-color 0.25s, box-shadow 0.25s;
  animation: fadeUp 0.6s ease 0.25s both;
  box-shadow: 0 2px 12px rgba(28,25,23,0.04);
}
.input-wrap:focus-within {
  border-color: var(--sage);
  box-shadow: 0 0 0 4px rgba(123,158,135,0.1), 0 2px 12px rgba(28,25,23,0.04);
}

div[data-testid="stTextInput"] input {
  background: transparent !important;
  border: none !important; box-shadow: none !important; outline: none !important;
  color: var(--ink) !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 14px !important; padding: 10px 0 !important;
}
div[data-testid="stTextInput"] input::placeholder { color: var(--dust) !important; }
div[data-testid="stTextInput"] > div { background: transparent !important; border: none !important; box-shadow: none !important; }

/* ── BUTTONS ── */
div[data-testid="stButton"] > button {
  background: var(--sage) !important; color: white !important;
  font-family: 'DM Sans', sans-serif !important; font-weight: 500 !important;
  font-size: 14px !important; border: none !important;
  border-radius: 100px !important; padding: 13px 28px !important;
  box-shadow: 0 4px 14px rgba(123,158,135,0.3) !important;
  transition: all 0.2s ease !important; white-space: nowrap !important;
}
div[data-testid="stButton"] > button:hover {
  background: #6a8f76 !important; transform: translateY(-1px) !important;
  box-shadow: 0 6px 20px rgba(123,158,135,0.4) !important;
}
div[data-testid="stButton"]:last-of-type > button {
  background: transparent !important; color: var(--dust) !important;
  border: 1px solid var(--warm) !important; box-shadow: none !important;
}
div[data-testid="stButton"]:last-of-type > button:hover {
  background: var(--warm) !important; color: var(--ink) !important;
  transform: none !important; box-shadow: none !important;
}

[data-testid="stAlert"] { border-radius: 12px !important; font-size: 13px !important; }
hr { border: none !important; height: 1px !important; background: var(--warm) !important; margin: 28px 0 !important; }

@keyframes fadeUp   { from{opacity:0;transform:translateY(18px)} to{opacity:1;transform:translateY(0)} }
@keyframes fadeDown { from{opacity:0;transform:translateY(-12px)} to{opacity:1;transform:translateY(0)} }
</style>
""", unsafe_allow_html=True)

# NAV
st.markdown("""
<div class="nav">
  <div class="nav-logo">
    <div class="nav-mark">🫀</div>
    <div class="nav-name">Med<em>Zentic</em></div>
  </div>
  <div class="nav-center">AI Medical Assistant</div>
  <div class="nav-status"><div class="nav-dot"></div>AI Online</div>
</div>
""", unsafe_allow_html=True)

# GUARD
if "analysis_data" not in st.session_state:
    st.error("No health analysis found. Please upload a report first.")
    if st.button("Return to Dashboard"):
        st.switch_page("pages/1_Dashboard.py")
    st.stop()

analysis_data = st.session_state["analysis_data"]
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# HEADER
st.markdown("""
<div class="chat-header">
  <div class="chat-avatar">🩺</div>
  <div class="chat-h1">AI Medical Assistant</div>
  <div class="chat-sub">// Ask questions about your health report — plain language responses</div>
</div>
""", unsafe_allow_html=True)

# MESSAGES
if st.session_state.chat_history:
    html = '<div class="msgs">'
    for chat in st.session_state.chat_history:
        u = chat['user'].replace("<","&lt;").replace(">","&gt;")
        a = chat['assistant'].replace("<","&lt;").replace(">","&gt;")
        html += f"""
        <div class="msg user">
          <div class="msg-av user-av">You</div>
          <div class="msg-content">
            <div class="msg-who">Patient</div>
            <div class="bubble user-bubble">{u}</div>
          </div>
        </div>
        <div class="msg ai">
          <div class="msg-av ai-av">AI</div>
          <div class="msg-content">
            <div class="msg-who">MedZentic AI</div>
            <div class="bubble ai-bubble">{a}</div>
          </div>
        </div>"""
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="empty-state">
      <div class="empty-icon">💬</div>
      <div class="empty-title">No messages yet — ask anything about your report</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# INPUT
st.markdown('<div class="input-wrap">', unsafe_allow_html=True)
user_input = st.text_input(
    label="message",
    placeholder="e.g. What does my glucose level mean?",
    label_visibility="collapsed"
)
st.markdown('</div>', unsafe_allow_html=True)

c1, c2 = st.columns([3, 1])
send  = c1.button("Send Message",  use_container_width=True)
clear = c2.button("Clear Chat",    use_container_width=True)

if clear:
    st.session_state.chat_history = []
    st.rerun()

if send and user_input:
    with st.spinner("Thinking…"):
        response = requests.post(
            f"{BACKEND_URL}/chat",
            json={
                "question": user_input,
                "analysis": analysis_data,
                "history": st.session_state.chat_history
            }
        )
    if response.status_code == 200:
        answer = response.json()["answer"]
        st.session_state.chat_history.append({"user": user_input, "assistant": answer})
        st.rerun()
    else:
        st.error(response.text)