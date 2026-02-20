import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(layout="wide", page_title="MedZentic AI — Assistant", page_icon="")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Outfit:wght@200;300;400;600;700;900&display=swap');

:root {
    --bg:      #030507;
    --surface: #080d12;
    --surface2:#0d1420;
    --border:  rgba(255,255,255,0.07);
    --text:    #f0f4f8;
    --muted:   rgba(240,244,248,0.35);
    --pulse:   #4af0c4;
    --blue:    #4a90f0;
    --mono:    'Space Mono', monospace;
    --sans:    'Outfit', sans-serif;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: var(--sans) !important;
}

#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stSidebarNav"],
section[data-testid="stSidebar"] { display: none !important; }

[data-testid="stAppViewContainer"] > .main { padding: 0 !important; }
[data-testid="stAppViewContainer"] > .main > div {
    padding: 0 48px 100px !important;
    max-width: 900px !important;
    margin: 0 auto !important;
}

body::before {
    content: ''; position: fixed; inset: 0; pointer-events: none; z-index: 9999;
    background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.05) 2px, rgba(0,0,0,0.05) 4px);
}
body::after {
    content: ''; position: fixed; inset: 0; pointer-events: none; z-index: 0;
    background-image:
        linear-gradient(rgba(255,255,255,0.015) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.015) 1px, transparent 1px);
    background-size: 48px 48px;
}

/* NAV */
.mz-nav {
    display: flex; align-items: center; justify-content: space-between;
    padding: 30px 0; border-bottom: 1px solid var(--border);
    margin-bottom: 52px;
    position: relative; z-index: 10;
    animation: fadeDown 0.7s ease both;
}
.mz-wordmark { font-family: var(--sans); font-weight: 900; font-size: 16px; letter-spacing: 4px; text-transform: uppercase; color: var(--text); }
.mz-wordmark span { color: var(--pulse); }
.mz-nav-center { font-family: var(--mono); font-size: 10px; letter-spacing: 3px; text-transform: uppercase; color: var(--muted); }
.mz-status-dot {
    display: inline-flex; align-items: center; gap: 8px;
    font-family: var(--mono); font-size: 10px; letter-spacing: 2px;
    text-transform: uppercase; color: var(--pulse);
}
.mz-status-dot::before {
    content: ''; width: 7px; height: 7px; border-radius: 50%;
    background: var(--pulse); box-shadow: 0 0 8px var(--pulse);
    animation: blink 1.4s ease-in-out infinite;
}
@keyframes blink { 0%,100% { opacity:1; } 50% { opacity:0.2; } }

/* PAGE HEADER */
.chat-header {
    text-align: center; padding: 8px 0 44px;
    animation: fadeUp 0.7s ease 0.1s both;
    position: relative; z-index: 2;
}
.chat-header-ring {
    width: 60px; height: 60px; border-radius: 50%;
    border: 1px solid rgba(74,240,196,0.25);
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto 20px;
    position: relative;
    animation: ringPulse 3s ease-in-out infinite;
}
.chat-header-ring::before {
    content: ''; position: absolute;
    width: 100%; height: 100%; border-radius: 50%;
    border: 1px solid rgba(74,240,196,0.1);
    animation: ringExpand 3s ease-in-out infinite;
}
.chat-header-cross {
    width: 22px; height: 22px; position: relative;
}
.chat-header-cross::before,
.chat-header-cross::after {
    content: ''; position: absolute;
    background: var(--pulse); border-radius: 1px;
}
.chat-header-cross::before { width: 2px; height: 22px; top: 0; left: 50%; transform: translateX(-50%); }
.chat-header-cross::after  { width: 22px; height: 2px; top: 50%; left: 0; transform: translateY(-50%); }
@keyframes ringPulse {
    0%,100% { box-shadow: 0 0 0 0 rgba(74,240,196,0.25); }
    50%      { box-shadow: 0 0 0 12px rgba(74,240,196,0); }
}
@keyframes ringExpand {
    0%   { transform: scale(1);   opacity: 0.5; }
    100% { transform: scale(1.8); opacity: 0; }
}

.chat-h1 {
    font-family: var(--sans); font-size: 30px; font-weight: 900;
    letter-spacing: -1px; color: var(--text); margin-bottom: 10px;
}
.chat-sub {
    font-family: var(--mono); font-size: 10px; letter-spacing: 2px;
    text-transform: uppercase; color: var(--muted);
}

/* CHAT HISTORY */
.chat-wrap {
    display: flex; flex-direction: column; gap: 20px;
    margin-bottom: 36px;
    position: relative; z-index: 2;
    animation: fadeUp 0.7s ease 0.2s both;
}
.msg-row { display: flex; gap: 14px; align-items: flex-start; animation: msgIn 0.35s ease both; }
.msg-row.user { flex-direction: row-reverse; }
@keyframes msgIn { from { opacity:0; transform:translateY(10px); } to { opacity:1; transform:translateY(0); } }

.msg-avatar {
    width: 34px; height: 34px; border-radius: 2px; flex-shrink: 0;
    display: flex; align-items: center; justify-content: center;
    font-family: var(--mono); font-size: 9px; letter-spacing: 1px;
    text-transform: uppercase;
}
.msg-avatar.user-av {
    background: rgba(74,144,240,0.12); border: 1px solid rgba(74,144,240,0.25); color: var(--blue);
}
.msg-avatar.ai-av {
    background: rgba(74,240,196,0.08); border: 1px solid rgba(74,240,196,0.2); color: var(--pulse);
}

.msg-body { max-width: 78%; }
.msg-sender {
    font-family: var(--mono); font-size: 8px; letter-spacing: 2px;
    text-transform: uppercase; margin-bottom: 8px;
}
.msg-row.user  .msg-sender { color: var(--blue);  text-align: right; }
.msg-row.ai    .msg-sender { color: var(--pulse); }

.msg-bubble {
    padding: 14px 18px; border-radius: 2px;
    font-size: 13px; line-height: 1.8; font-weight: 300;
}
.msg-bubble.user-bub {
    background: rgba(74,144,240,0.08);
    border: 1px solid rgba(74,144,240,0.18);
    color: var(--text);
    border-top-right-radius: 0;
}
.msg-bubble.ai-bub {
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 2px solid rgba(74,240,196,0.4);
    color: rgba(240,244,248,0.8);
    border-top-left-radius: 0;
}

/* EMPTY STATE */
.chat-empty {
    border: 1px dashed rgba(255,255,255,0.06);
    border-radius: 3px; padding: 60px 40px;
    text-align: center; margin-bottom: 36px;
    position: relative; z-index: 2;
    animation: fadeUp 0.7s ease 0.25s both;
}
.chat-empty-pulse {
    width: 40px; height: 40px; border-radius: 50%;
    border: 1px solid rgba(74,240,196,0.2);
    margin: 0 auto 18px;
    animation: ringPulse 2.5s ease-in-out infinite;
}
.chat-empty-title {
    font-family: var(--mono); font-size: 9px; letter-spacing: 3px;
    text-transform: uppercase; color: var(--muted);
}

/* INPUT AREA */
.input-area {
    position: relative; z-index: 2;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 3px; padding: 3px 3px 3px 20px;
    display: flex; align-items: center; gap: 10px;
    transition: border-color 0.3s;
    animation: fadeUp 0.7s ease 0.3s both;
}
.input-area:focus-within {
    border-color: rgba(74,240,196,0.3);
    box-shadow: 0 0 20px rgba(74,240,196,0.04);
}

div[data-testid="stTextInput"] input {
    background: transparent !important;
    border: none !important; box-shadow: none !important; outline: none !important;
    color: var(--text) !important;
    font-family: var(--mono) !important; font-size: 12px !important;
    letter-spacing: 0.5px !important; padding: 10px 0 !important;
}
div[data-testid="stTextInput"] input::placeholder { color: var(--muted) !important; }
div[data-testid="stTextInput"] > div {
    background: transparent !important; border: none !important; box-shadow: none !important;
}

/* BUTTONS */
div[data-testid="stButton"] > button {
    background: var(--text) !important; color: var(--bg) !important;
    font-family: var(--sans) !important; font-weight: 700 !important;
    font-size: 11px !important; letter-spacing: 2.5px !important;
    text-transform: uppercase !important;
    border: none !important; border-radius: 2px !important;
    padding: 14px 28px !important;
    transition: all 0.25s ease !important;
}
div[data-testid="stButton"] > button:hover {
    background: var(--pulse) !important; color: var(--bg) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 24px rgba(74,240,196,0.25) !important;
}
/* Clear — ghost style */
div[data-testid="stButton"]:last-of-type > button {
    background: transparent !important; color: var(--muted) !important;
    border: 1px solid var(--border) !important;
    box-shadow: none !important;
}
div[data-testid="stButton"]:last-of-type > button:hover {
    background: rgba(255,255,255,0.04) !important;
    color: var(--text) !important; transform: none !important;
    box-shadow: none !important;
}

[data-testid="stAlert"] {
    background: transparent !important; border-radius: 2px !important;
    border-left-width: 2px !important;
    font-family: var(--mono) !important; font-size: 11px !important;
}

hr {
    border: none !important; height: 1px !important;
    background: var(--border) !important; margin: 32px 0 !important;
}

@keyframes fadeUp   { from { opacity:0; transform:translateY(22px); } to { opacity:1; transform:translateY(0); } }
@keyframes fadeDown { from { opacity:0; transform:translateY(-16px); } to { opacity:1; transform:translateY(0); } }
</style>
""", unsafe_allow_html=True)

# ── NAV ────────────────────────────────────────────────────
st.markdown("""
<div class="mz-nav">
  <div class="mz-wordmark">Med<span>Zentic</span></div>
  <div class="mz-nav-center">AI Medical Assistant</div>
  <div class="mz-status-dot">AI Online</div>
</div>
""", unsafe_allow_html=True)

# ── GUARD ──────────────────────────────────────────────────
if "analysis_data" not in st.session_state:
    st.error("No health analysis found. Please upload a report first.")
    if st.button("Return to Dashboard"):
        st.switch_page("pages/1_Dashboard.py")
    st.stop()

analysis_data = st.session_state["analysis_data"]

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ── HEADER ─────────────────────────────────────────────────
st.markdown("""
<div class="chat-header">
  <div class="chat-header-ring"><div class="chat-header-cross"></div></div>
  <div class="chat-h1">AI Medical Assistant</div>
  <div class="chat-sub">// Ask questions about your health report — plain language responses</div>
</div>
""", unsafe_allow_html=True)

# ── MESSAGES ───────────────────────────────────────────────
if st.session_state.chat_history:
    html = '<div class="chat-wrap">'
    for chat in st.session_state.chat_history:
        u = chat['user'].replace("<","&lt;").replace(">","&gt;")
        a = chat['assistant'].replace("<","&lt;").replace(">","&gt;")
        html += f"""
        <div class="msg-row user">
          <div class="msg-avatar user-av">You</div>
          <div class="msg-body">
            <div class="msg-sender">Patient</div>
            <div class="msg-bubble user-bub">{u}</div>
          </div>
        </div>
        <div class="msg-row ai">
          <div class="msg-avatar ai-av">AI</div>
          <div class="msg-body">
            <div class="msg-sender">MedZentic AI</div>
            <div class="msg-bubble ai-bub">{a}</div>
          </div>
        </div>
        """
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="chat-empty">
      <div class="chat-empty-pulse"></div>
      <div class="chat-empty-title">No messages yet — ask anything about your report</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ── INPUT ──────────────────────────────────────────────────
user_input = st.text_input(
    label="message",
    placeholder="e.g. What does my glucose level mean?",
    label_visibility="collapsed"
)

c1, c2 = st.columns([3, 1])
send  = c1.button("Send Message",  use_container_width=True)
clear = c2.button("Clear Chat",    use_container_width=True)

# ── BACKEND (untouched) ────────────────────────────────────
if clear:
    st.session_state.chat_history = []
    st.rerun()

if send and user_input:
    with st.spinner("Analyzing..."):
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