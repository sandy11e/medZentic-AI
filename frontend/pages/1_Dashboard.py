import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import io
import time
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from datetime import datetime

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(layout="wide", page_title="MedZentic — Dashboard", page_icon="🫀")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400;1,600&family=DM+Sans:wght@300;400;500&family=DM+Mono:wght@300;400&display=swap');

:root {
  --cream:    #F7F3EE;
  --warm:     #EDE8E0;
  --sage:     #7B9E87;
  --sage-lt:  #EAF2EC;
  --clay:     #C4856A;
  --clay-lt:  #F8EDE7;
  --amber:    #C4913A;
  --amber-lt: #FBF4E6;
  --red:      #B85C52;
  --red-lt:   #FAEAE8;
  --ink:      #1C1917;
  --ink2:     #44403C;
  --dust:     #A8A29E;
  --white:    #FEFCFA;
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
  padding: 0 60px 100px !important;
  max-width: 1280px !important;
  margin: 0 auto !important;
}

/* ── NAV ── */
.nav {
  display: flex; align-items: center; justify-content: space-between;
  padding: 28px 0;
  border-bottom: 1px solid var(--warm);
  margin-bottom: 56px;
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

/* ── HERO UPLOAD ── */
.upload-hero {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2px;
  background: var(--warm);
  border-radius: 24px; overflow: hidden;
  margin-bottom: 24px;
  animation: fadeUp 0.6s ease 0.1s both;
}
.upload-left {
  background: var(--ink);
  padding: 56px 52px;
  position: relative; overflow: hidden;
}
.upload-left::before {
  content: '';
  position: absolute; top: -100px; right: -100px;
  width: 400px; height: 400px; border-radius: 50%;
  background: radial-gradient(circle, rgba(123,158,135,0.2), transparent 65%);
}
.upload-left::after {
  content: '';
  position: absolute; bottom: -60px; left: 20%;
  width: 250px; height: 250px; border-radius: 50%;
  background: radial-gradient(circle, rgba(196,133,106,0.1), transparent 65%);
}
.upload-eyebrow {
  font-family: 'DM Mono', monospace; font-size: 10px; letter-spacing: 2px;
  text-transform: uppercase; color: var(--sage); margin-bottom: 20px;
  position: relative; z-index: 1;
}
.upload-title {
  font-family: 'Playfair Display', serif;
  font-size: 38px; font-weight: 700; line-height: 1.1;
  letter-spacing: -1px; color: white; margin-bottom: 14px;
  position: relative; z-index: 1;
}
.upload-title em { font-style: italic; color: var(--sage-lt); }
.upload-desc {
  font-size: 14px; font-weight: 300; line-height: 1.75;
  color: rgba(255,255,255,0.5); max-width: 340px;
  position: relative; z-index: 1;
}
.upload-stats {
  display: flex; gap: 36px; margin-top: 44px;
  position: relative; z-index: 1;
  padding-top: 32px;
  border-top: 1px solid rgba(255,255,255,0.1);
}
.u-stat-n {
  font-family: 'Playfair Display', serif;
  font-size: 28px; font-weight: 700;
  color: white; letter-spacing: -1px; line-height: 1;
}
.u-stat-l { font-family: 'DM Mono', monospace; font-size: 9px; letter-spacing: 1px; color: rgba(255,255,255,0.4); text-transform: uppercase; margin-top: 4px; }

.upload-right {
  background: var(--white);
  padding: 56px 52px;
  display: flex; flex-direction: column; justify-content: center;
}
.upload-form-label {
  font-family: 'DM Mono', monospace; font-size: 10px; letter-spacing: 2px;
  text-transform: uppercase; color: var(--dust); margin-bottom: 14px;
}
.upload-form-title {
  font-family: 'Playfair Display', serif;
  font-size: 24px; font-weight: 700; color: var(--ink);
  letter-spacing: -0.4px; margin-bottom: 8px;
}
.upload-form-sub { font-size: 13px; color: var(--dust); line-height: 1.6; margin-bottom: 28px; }

[data-testid="stFileUploader"] {
  background: var(--cream) !important;
  border: 1.5px dashed rgba(123,158,135,0.4) !important;
  border-radius: 16px !important;
  padding: 24px !important;
  transition: all 0.25s ease !important;
}
[data-testid="stFileUploader"]:hover {
  border-color: var(--sage) !important;
  background: var(--sage-lt) !important;
}
[data-testid="stFileUploader"] label { display: none !important; }

/* ── ANALYSIS OVERLAY ── */
.scan-wrap {
  background: var(--white);
  border: 1px solid var(--warm);
  border-radius: 24px; padding: 64px;
  text-align: center;
  box-shadow: 0 8px 40px rgba(28,25,23,0.06);
  position: relative; overflow: hidden;
  animation: fadeUp 0.4s ease both;
}
.scan-wrap::before {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; height: 3px;
  background: linear-gradient(90deg, var(--sage), var(--clay));
  animation: scanSlide 1.5s linear infinite;
  background-size: 200% 100%;
}
@keyframes scanSlide { from{background-position:-100% 0} to{background-position:200% 0} }
.scan-icon { font-size: 48px; margin-bottom: 24px; animation: spinSlow 4s linear infinite; display: inline-block; }
@keyframes spinSlow { 0%{transform:rotate(0deg)} 100%{transform:rotate(360deg)} }
.scan-title {
  font-family: 'Playfair Display', serif;
  font-size: 28px; font-weight: 700; color: var(--ink);
  letter-spacing: -0.5px; margin-bottom: 8px;
}
.scan-sub {
  font-family: 'DM Mono', monospace; font-size: 11px;
  letter-spacing: 1px; color: var(--dust); margin-bottom: 44px;
}
.scan-steps { display: flex; flex-direction: column; gap: 16px; max-width: 460px; margin: 0 auto 36px; text-align: left; }
.scan-step { display: flex; align-items: center; gap: 14px; }
.scan-step-icon {
  width: 36px; height: 36px; border-radius: 10px;
  background: var(--cream); border: 1px solid var(--warm);
  display: flex; align-items: center; justify-content: center; font-size: 16px; flex-shrink: 0;
}
.scan-step-name { font-size: 13px; font-weight: 500; color: var(--ink2); margin-bottom: 6px; }
.scan-step-bar { height: 4px; background: var(--warm); border-radius: 100px; overflow: hidden; }
.scan-step-fill { height: 100%; background: linear-gradient(90deg, var(--sage), var(--clay)); border-radius: 100px; }
.b1{animation:bFill 5s ease 0.0s both}
.b2{animation:bFill 5s ease 0.4s both}
.b3{animation:bFill 5s ease 0.8s both}
.b4{animation:bFill 5s ease 1.2s both}
.b5{animation:bFill 5s ease 1.6s both}
@keyframes bFill { from{width:0} to{width:100%} }
.scan-ticker {
  font-family: 'DM Mono', monospace; font-size: 10px;
  color: var(--dust); display: flex; align-items: center; gap: 8px; justify-content: center;
}
.ticker-dot { width: 5px; height: 5px; background: var(--sage); border-radius: 50%; animation: breathe 1s ease-in-out infinite; }

/* ── SECTION HEADER ── */
.sec-head {
  display: flex; align-items: center; gap: 16px;
  margin: 64px 0 28px;
  animation: fadeUp 0.5s ease both;
}
.sec-tag {
  font-family: 'DM Mono', monospace; font-size: 9px;
  letter-spacing: 2px; text-transform: uppercase;
  color: var(--clay); background: var(--clay-lt);
  padding: 5px 12px; border-radius: 100px; flex-shrink: 0;
}
.sec-title {
  font-family: 'Playfair Display', serif;
  font-size: 22px; font-weight: 700; color: var(--ink); letter-spacing: -0.4px;
}
.sec-rule { flex: 1; height: 1px; background: var(--warm); }

/* ── GAUGE CARDS ── */
.gauge-card {
  background: var(--white);
  border: 1px solid var(--warm);
  border-radius: 20px; padding: 24px 20px 16px;
  box-shadow: 0 2px 12px rgba(28,25,23,0.04);
  transition: all 0.25s ease; position: relative; overflow: hidden;
}
.gauge-card::before { content:''; position:absolute; top:0; left:0; right:0; height:3px; }
.gauge-card.low::before  { background: linear-gradient(90deg, var(--sage), #a3c9ae); }
.gauge-card.mid::before  { background: linear-gradient(90deg, var(--amber), #e0b76a); }
.gauge-card.high::before { background: linear-gradient(90deg, var(--red), #d48a82); }
.gauge-card:hover { transform: translateY(-3px); box-shadow: 0 8px 32px rgba(28,25,23,0.08); }
.gauge-lbl { font-family: 'DM Mono', monospace; font-size: 9px; letter-spacing: 1.5px; text-transform: uppercase; color: var(--dust); margin-bottom: 4px; }
.gauge-pill { display:inline-block; font-size:11px; font-weight:600; padding:4px 14px; border-radius:100px; margin-top:8px; }
.pill-low  { background: var(--sage-lt); color: var(--sage); }
.pill-mid  { background: var(--amber-lt); color: var(--amber); }
.pill-high { background: var(--red-lt); color: var(--red); }

/* ── FLAGS ── */
.flag {
  display: flex; align-items: flex-start; gap: 14px;
  background: var(--red-lt); border: 1px solid rgba(184,92,82,0.2);
  border-left: 3px solid var(--red);
  border-radius: 14px; padding: 16px 20px; margin-bottom: 10px;
}
.flag-ok {
  display: flex; align-items: center; gap: 14px;
  background: var(--sage-lt); border: 1px solid rgba(123,158,135,0.25);
  border-left: 3px solid var(--sage);
  border-radius: 14px; padding: 18px 20px;
}
.flag-ico { font-size: 18px; }
.flag-h { font-size: 13px; font-weight: 600; color: var(--red); margin-bottom: 2px; }
.flag-d { font-family: 'DM Mono', monospace; font-size: 10px; color: rgba(184,92,82,0.6); }
.flag-ok-t { font-size: 13px; font-weight: 600; color: var(--sage); }

/* ── INTERPRETATION CARDS ── */
.interp {
  background: var(--white); border: 1px solid var(--warm); border-radius: 20px;
  overflow: hidden; margin-bottom: 14px;
  box-shadow: 0 2px 10px rgba(28,25,23,0.04);
  transition: box-shadow 0.25s;
}
.interp:hover { box-shadow: 0 8px 28px rgba(28,25,23,0.08); }
.interp-head {
  display: flex; align-items: center; justify-content: space-between;
  padding: 18px 24px; background: var(--cream); border-bottom: 1px solid var(--warm);
}
.interp-head-l { display: flex; align-items: center; gap: 12px; }
.interp-icon {
  width: 34px; height: 34px; border-radius: 10px;
  background: var(--sage-lt); display: flex; align-items: center; justify-content: center; font-size: 16px;
}
.interp-name { font-size: 13px; font-weight: 600; color: var(--ink); }
.interp-sub { font-family: 'DM Mono', monospace; font-size: 10px; color: var(--dust); margin-top: 1px; }
.interp-badge { font-size: 11px; font-weight: 600; padding: 4px 12px; border-radius: 100px; }
.interp-body { padding: 22px 24px; font-size: 14px; line-height: 1.75; color: var(--ink2); }

/* ── CHART WRAP ── */
.chart-wrap {
  background: var(--white); border: 1px solid var(--warm); border-radius: 20px;
  padding: 28px 24px 16px;
  box-shadow: 0 2px 10px rgba(28,25,23,0.04);
}

/* ── EXPORT / AI CARDS ── */
.export-card {
  background: linear-gradient(135deg, var(--sage-lt), var(--clay-lt));
  border: 1px solid rgba(123,158,135,0.25); border-radius: 20px; padding: 36px;
}
.ai-card {
  background: var(--ink); border-radius: 20px; padding: 44px;
  position: relative; overflow: hidden;
}
.ai-card::before {
  content: ''; position: absolute; top: -80px; right: -80px;
  width: 320px; height: 320px; border-radius: 50%;
  background: radial-gradient(circle, rgba(123,158,135,0.2), transparent 65%);
}
.ai-card-inner { position: relative; z-index: 1; }
.ai-eyebrow { font-family: 'DM Mono', monospace; font-size: 10px; letter-spacing: 1.5px; text-transform: uppercase; color: rgba(255,255,255,0.4); margin-bottom: 12px; }
.ai-title { font-family: 'Playfair Display', serif; font-size: 30px; font-style: italic; color: white; margin-bottom: 10px; }
.ai-desc { font-size: 14px; color: rgba(255,255,255,0.5); line-height: 1.7; max-width: 440px; margin-bottom: 28px; }

/* ── BUTTONS ── */
div[data-testid="stButton"] > button {
  background: var(--sage) !important; color: white !important;
  font-family: 'DM Sans', sans-serif !important; font-weight: 500 !important;
  font-size: 14px !important; border: none !important;
  border-radius: 100px !important; padding: 14px 36px !important;
  box-shadow: 0 4px 16px rgba(123,158,135,0.35) !important;
  transition: all 0.2s ease !important;
}
div[data-testid="stButton"] > button:hover {
  background: #6a8f76 !important; transform: translateY(-2px) !important;
  box-shadow: 0 8px 24px rgba(123,158,135,0.45) !important;
}
div[data-testid="stDownloadButton"] > button {
  background: var(--white) !important; color: var(--sage) !important;
  font-family: 'DM Sans', sans-serif !important; font-weight: 600 !important;
  font-size: 13px !important; border: 1.5px solid var(--sage) !important;
  border-radius: 100px !important; padding: 12px 28px !important; box-shadow: none !important;
  transition: all 0.2s ease !important;
}
div[data-testid="stDownloadButton"] > button:hover {
  background: var(--sage-lt) !important; transform: translateY(-1px) !important;
}

[data-testid="stMetric"] {
  background: var(--white) !important; border: 1px solid var(--warm) !important;
  border-radius: 16px !important; padding: 24px !important;
  box-shadow: 0 2px 8px rgba(28,25,23,0.04) !important;
}
[data-testid="stMetricLabel"] { font-family: 'DM Mono', monospace !important; font-size: 9px !important; text-transform: uppercase !important; letter-spacing: 1px !important; color: var(--dust) !important; }
[data-testid="stMetricValue"] { font-family: 'Playfair Display', serif !important; font-size: 34px !important; font-weight: 700 !important; color: var(--ink) !important; }

[data-testid="stAlert"] { border-radius: 12px !important; font-size: 13px !important; }

hr { border: none !important; height: 1px !important; background: var(--warm) !important; margin: 52px 0 !important; }

@keyframes fadeUp   { from{opacity:0;transform:translateY(20px)} to{opacity:1;transform:translateY(0)} }
@keyframes fadeDown { from{opacity:0;transform:translateY(-14px)} to{opacity:1;transform:translateY(0)} }
[data-testid="stHorizontalBlock"] { gap: 20px !important; }
</style>
""", unsafe_allow_html=True)

# NAV
st.markdown("""
<div class="nav">
  <div class="nav-logo">
    <div class="nav-mark">🫀</div>
    <div class="nav-name">Med<em>Zentic</em></div>
  </div>
  <div class="nav-center">Health Dashboard</div>
  <div class="nav-status"><div class="nav-dot"></div>All systems operational</div>
</div>
""", unsafe_allow_html=True)

# HERO UPLOAD
st.markdown("""
<div class="upload-hero">
  <div class="upload-left">
    <div class="upload-eyebrow">// Step 01 — Scan</div>
    <div class="upload-title">Your health,<br><em>decoded.</em></div>
    <div class="upload-desc">Upload your medical report and our clinical AI models will assess your risk across diabetes, cardiac health, and neurological markers.</div>
    <div class="upload-stats">
      <div><div class="u-stat-n">3</div><div class="u-stat-l">AI Models</div></div>
      <div><div class="u-stat-n">~5s</div><div class="u-stat-l">Analysis</div></div>
      <div><div class="u-stat-n">PDF</div><div class="u-stat-l">Export</div></div>
    </div>
  </div>
  <div class="upload-right">
    <div class="upload-form-label">// Upload Report</div>
    <div class="upload-form-title">Medical Report</div>
    <div class="upload-form-sub">Drag & drop your PDF. Clinical data extracted automatically.</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"], label_visibility="collapsed")
st.markdown("</div></div>", unsafe_allow_html=True)

results = {}
extracted_values = {}

if uploaded_file:
    # SCAN ANIMATION
    scan_ph = st.empty()
    scan_ph.markdown("""
    <div class="scan-wrap">
      <div class="scan-icon">🔬</div>
      <div class="scan-title">Analysing your report</div>
      <div class="scan-sub">// Clinical models processing · approximately 5 seconds</div>
      <div class="scan-steps">
        <div class="scan-step"><div class="scan-step-icon">🧪</div><div style="flex:1"><div class="scan-step-name">Extracting Lab Values</div><div class="scan-step-bar"><div class="scan-step-fill b1"></div></div></div></div>
        <div class="scan-step"><div class="scan-step-icon">🧠</div><div style="flex:1"><div class="scan-step-name">Running ML Models</div><div class="scan-step-bar"><div class="scan-step-fill b2"></div></div></div></div>
        <div class="scan-step"><div class="scan-step-icon">🩸</div><div style="flex:1"><div class="scan-step-name">Diabetes Assessment</div><div class="scan-step-bar"><div class="scan-step-fill b3"></div></div></div></div>
        <div class="scan-step"><div class="scan-step-icon">❤️</div><div style="flex:1"><div class="scan-step-name">Cardiac Risk Analysis</div><div class="scan-step-bar"><div class="scan-step-fill b4"></div></div></div></div>
        <div class="scan-step"><div class="scan-step-icon">🧬</div><div style="flex:1"><div class="scan-step-name">Neurological Scan</div><div class="scan-step-bar"><div class="scan-step-fill b5"></div></div></div></div>
      </div>
      <div class="scan-ticker"><div class="ticker-dot"></div>Processing clinical parameters in real-time…</div>
    </div>
    """, unsafe_allow_html=True)

    files = {"file": uploaded_file}
    response = requests.post(f"{BACKEND_URL}/analyze-report", files=files)
    time.sleep(5)
    scan_ph.empty()

    if response.status_code != 200:
        st.error(response.text)
        st.stop()

    data = response.json()
    st.session_state["analysis_data"] = data
    extracted_values = data.get("extracted_values", {})
    results = data.get("results", {})
    valid_results = {k: v for k, v in results.items() if "status" not in v}

    # 01 RISK GAUGES
    st.markdown("""<div class="sec-head">
      <span class="sec-tag">01</span>
      <span class="sec-title">Condition Risk Summary</span>
      <div class="sec-rule"></div>
    </div>""", unsafe_allow_html=True)

    if valid_results:
        cond_icons = {"diabetes": "🩸", "heart": "❤️", "parkinson": "🧬"}
        cols = st.columns(len(valid_results))
        for idx, (condition, analysis) in enumerate(valid_results.items()):
            summary = analysis["summary"]
            prob = summary["risk_probability"] * 100
            risk = summary["risk_level"]
            icon = cond_icons.get(condition, "🔬")
            if prob < 40:
                gc, cc, pc = "#7B9E87", "low", "pill-low"
                steps = [{'range':[0,40],'color':'rgba(123,158,135,0.15)'},{'range':[40,70],'color':'rgba(196,145,58,0.04)'},{'range':[70,100],'color':'rgba(184,92,82,0.04)'}]
            elif prob < 70:
                gc, cc, pc = "#C4913A", "mid", "pill-mid"
                steps = [{'range':[0,40],'color':'rgba(123,158,135,0.04)'},{'range':[40,70],'color':'rgba(196,145,58,0.12)'},{'range':[70,100],'color':'rgba(184,92,82,0.04)'}]
            else:
                gc, cc, pc = "#B85C52", "high", "pill-high"
                steps = [{'range':[0,40],'color':'rgba(123,158,135,0.04)'},{'range':[40,70],'color':'rgba(196,145,58,0.04)'},{'range':[70,100],'color':'rgba(184,92,82,0.12)'}]
            with cols[idx]:
                st.markdown(f'<div class="gauge-card {cc}"><div class="gauge-lbl">{icon} {condition.upper()}</div>', unsafe_allow_html=True)
                fig = go.Figure(go.Indicator(
                    mode="gauge+number", value=prob,
                    number={'suffix':"%",'font':{'color':'#1C1917','size':32,'family':'Playfair Display'},'valueformat':'.1f'},
                    gauge={'axis':{'range':[0,100],'tickcolor':'#EDE8E0','tickfont':{'color':'#A8A29E','size':9,'family':'DM Mono'},'tickwidth':1,'nticks':5},
                           'bar':{'color':gc,'thickness':0.3},'bgcolor':'rgba(0,0,0,0)','borderwidth':0,
                           'steps':steps,'threshold':{'line':{'color':gc,'width':2},'thickness':0.85,'value':prob}}
                ))
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                                  margin=dict(t=16,b=0,l=16,r=16), height=200, font_color='#1C1917')
                st.plotly_chart(fig, use_container_width=True)
                st.markdown(f'<div class="gauge-pill {pc}">{risk}</div></div>', unsafe_allow_html=True)

    st.divider()

    # 02 COMPOSITE SCORE
    st.markdown("""<div class="sec-head">
      <span class="sec-tag">02</span>
      <span class="sec-title">Composite Health Score</span>
      <div class="sec-rule"></div>
    </div>""", unsafe_allow_html=True)

    valid_results2 = {k: v for k, v in results.items() if "status" not in v}
    if valid_results2:
        weights = {"diabetes": 0.4, "heart": 0.4, "parkinson": 0.2}
        weighted_score, probabilities = 0, []
        for disease, analysis in valid_results2.items():
            p = analysis["summary"]["risk_probability"]
            probabilities.append(p)
            if disease in weights: weighted_score += p * weights[disease]
        overall = weighted_score
        if max(probabilities) >= 0.75: overall = max(overall, 0.75)
        if sum(p >= 0.6 for p in probabilities) >= 2: overall = min(overall + 0.10, 1.0)
        pct = int(overall * 100)

        if pct < 40:
            sc, vbg, vc = "#7B9E87", "#EAF2EC", "#7B9E87"; verdict = "Low Risk"
            desc = "Your combined health indicators suggest a low overall risk profile. Continue with routine wellness check-ups and maintain your current health habits."
        elif pct < 70:
            sc, vbg, vc = "#C4913A", "#FBF4E6", "#C4913A"; verdict = "Moderate Risk"
            desc = "Moderate combined health risk detected. We recommend scheduling a consultation with your healthcare provider for a more detailed evaluation."
        else:
            sc, vbg, vc = "#B85C52", "#FAEAE8", "#B85C52"; verdict = "High Risk"
            desc = "High combined health risk identified. Please seek medical consultation promptly. Early intervention significantly improves outcomes."

        c1, c2 = st.columns([1, 2])
        with c1:
            st.markdown(f"""
            <div style="background:#FEFCFA;border:1px solid #EDE8E0;border-radius:20px;padding:36px;text-align:center;box-shadow:0 2px 12px rgba(28,25,23,.04);">
              <div style="font-family:'DM Mono',monospace;font-size:9px;letter-spacing:1.5px;text-transform:uppercase;color:#A8A29E;margin-bottom:16px;">Overall Score</div>
              <div style="font-family:'Playfair Display',serif;font-size:80px;font-weight:700;letter-spacing:-4px;line-height:1;color:{sc};">{pct}</div>
              <div style="font-size:12px;font-weight:600;color:{vc};background:{vbg};padding:6px 18px;border-radius:100px;display:inline-block;margin-top:16px;">{verdict}</div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div style="background:#FEFCFA;border:1px solid #EDE8E0;border-radius:20px;padding:36px;height:100%;box-shadow:0 2px 12px rgba(28,25,23,.04);">
              <div style="font-family:'DM Mono',monospace;font-size:9px;letter-spacing:1.5px;text-transform:uppercase;color:#A8A29E;margin-bottom:14px;">Clinical Assessment</div>
              <div style="font-family:'Playfair Display',serif;font-size:20px;font-weight:700;color:#1C1917;margin-bottom:12px;">{verdict}</div>
              <div style="font-size:14px;color:#44403C;line-height:1.75;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # 03 RISK COMPARISON
    st.markdown("""<div class="sec-head">
      <span class="sec-tag">03</span>
      <span class="sec-title">Disease Risk Comparison</span>
      <div class="sec-rule"></div>
    </div>""", unsafe_allow_html=True)

    risk_df = pd.DataFrame([
        {"Condition": c.capitalize(), "Risk": round(a["summary"]["risk_probability"]*100,1)}
        for c,a in valid_results2.items()
    ])
    def bcolor(v):
        if v < 40: return "#7B9E87"
        if v < 70: return "#C4913A"
        return "#B85C52"

    fig_bar = go.Figure()
    for _, row in risk_df.iterrows():
        fig_bar.add_trace(go.Bar(
            x=[row["Condition"]], y=[row["Risk"]],
            marker_color=bcolor(row["Risk"]), marker_line_width=0,
            text=[f'{row["Risk"]:.1f}%'], textposition='outside',
            textfont=dict(family='Playfair Display',size=14,color='#1C1917'), width=0.38, name=row["Condition"],
        ))
    fig_bar.add_hline(y=40, line_dash="dot", line_color="rgba(123,158,135,.5)", line_width=1.5,
                      annotation_text="Low / Moderate", annotation_font_size=9, annotation_font_color="#A8A29E", annotation_position="right")
    fig_bar.add_hline(y=70, line_dash="dot", line_color="rgba(184,92,82,.5)", line_width=1.5,
                      annotation_text="Moderate / High", annotation_font_size=9, annotation_font_color="#A8A29E", annotation_position="right")
    fig_bar.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False,
        font=dict(family='DM Sans',color='#1C1917'),
        xaxis=dict(showgrid=False, showline=False, tickfont=dict(size=14,color='#44403C',family='DM Sans')),
        yaxis=dict(showgrid=True, gridcolor='#EDE8E0', gridwidth=1, tickfont=dict(color='#A8A29E',size=10,family='DM Mono'), ticksuffix='%', range=[0,115], zeroline=False),
        margin=dict(t=20,b=10,l=0,r=90), height=340, bargap=0.5,
    )
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    # 04 LAB DISTRIBUTION
    if extracted_values:
        st.markdown("""<div class="sec-head">
          <span class="sec-tag">04</span>
          <span class="sec-title">Lab Parameter Distribution</span>
          <div class="sec-rule"></div>
        </div>""", unsafe_allow_html=True)

        elevated = sum(1 for v in extracted_values.values() if v > 200)
        normal = len(extracted_values) - elevated
        total = len(extracted_values)
        nr = round(normal/total*100) if total else 0
        er = round(elevated/total*100) if total else 0

        col_a, col_b = st.columns(2)
        with col_a:
            fig_pie = go.Figure(go.Pie(
                labels=["Within Range","Elevated"], values=[normal, elevated], hole=0.7,
                marker=dict(colors=["#7B9E87","#B85C52"], line=dict(color='#F7F3EE',width=5)),
                textfont=dict(family='DM Sans',size=13), showlegend=False,
                hovertemplate='<b>%{label}</b><br>%{value} parameters<extra></extra>',
            ))
            fig_pie.add_annotation(text=f"<b>{total}</b>", x=0.5, y=0.58, font=dict(family='Playfair Display',size=36,color='#1C1917'), showarrow=False)
            fig_pie.add_annotation(text="parameters", x=0.5, y=0.40, font=dict(family='DM Mono',size=11,color='#A8A29E'), showarrow=False)
            fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(family='DM Sans'), margin=dict(t=8,b=8,l=8,r=8), height=300)
            st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
            st.plotly_chart(fig_pie, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with col_b:
            st.markdown(f"""
            <div style="display:flex;flex-direction:column;gap:14px;padding-top:4px;">
              <div class="flag-ok">
                <div class="flag-ico">✅</div>
                <div><div class="flag-ok-t" style="margin-bottom:2px;">Within Normal Range</div>
                <div style="font-family:'Playfair Display',serif;font-size:40px;font-weight:700;color:#1C1917;letter-spacing:-1px;line-height:1.1;">{normal}</div>
                <div style="font-size:12px;color:#A8A29E;margin-top:4px;">{nr}% of parameters tested</div></div>
              </div>
              <div class="flag" style="margin-bottom:0">
                <div class="flag-ico">⚠️</div>
                <div><div class="flag-h" style="margin-bottom:2px;">Elevated / Flagged</div>
                <div style="font-family:'Playfair Display',serif;font-size:40px;font-weight:700;color:#1C1917;letter-spacing:-1px;line-height:1.1;">{elevated}</div>
                <div style="font-family:'DM Mono',monospace;font-size:10px;color:rgba(184,92,82,0.6);margin-top:4px;">{er}% require attention</div></div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # 05 FLAGS
    st.markdown("""<div class="sec-head">
      <span class="sec-tag">05</span>
      <span class="sec-title">Clinical Risk Flags</span>
      <div class="sec-rule"></div>
    </div>""", unsafe_allow_html=True)

    flags = []
    if extracted_values.get("Glucose",0) > 140:        flags.append(("🩸","Elevated Blood Glucose",f"Detected: {extracted_values.get('Glucose')} mg/dL · Threshold: 140 mg/dL"))
    if extracted_values.get("Cholesterol",0) > 240:    flags.append(("⚠️","High Cholesterol",f"Detected: {extracted_values.get('Cholesterol')} mg/dL · Threshold: 240 mg/dL"))
    if extracted_values.get("Blood Pressure",0) > 140: flags.append(("💓","High Blood Pressure",f"Detected: {extracted_values.get('Blood Pressure')} mmHg · Threshold: 140 mmHg"))
    if extracted_values.get("BMI",0) > 30:             flags.append(("📊","Obesity Indicator",f"BMI: {extracted_values.get('BMI')} · Threshold: 30"))

    if flags:
        for emoji, title, detail in flags:
            st.markdown(f'<div class="flag"><div class="flag-ico">{emoji}</div><div><div class="flag-h">{title}</div><div class="flag-d">{detail}</div></div></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="flag-ok"><div class="flag-ico">✅</div><div class="flag-ok-t">No major cardiometabolic risk indicators detected. All key parameters within safe thresholds.</div></div>', unsafe_allow_html=True)

    st.divider()

    # 06 CLINICAL INTERPRETATION
    st.markdown("""<div class="sec-head">
      <span class="sec-tag">06</span>
      <span class="sec-title">Clinical Interpretation</span>
      <div class="sec-rule"></div>
    </div>""", unsafe_allow_html=True)

    cond_icons = {"diabetes":"🩸","heart":"❤️","parkinson":"🧬"}
    for condition, analysis in results.items():
        icon = cond_icons.get(condition,"🔬")
        if "status" in analysis:
            st.markdown(f"""<div class="interp">
              <div class="interp-head"><div class="interp-head-l"><div class="interp-icon">{icon}</div><div><div class="interp-name">{condition.capitalize()} Assessment</div><div class="interp-sub">Insufficient data</div></div></div>
              <div class="interp-badge" style="background:#FBF4E6;color:#C4913A;">Skipped</div></div>
              <div class="interp-body" style="color:#C4913A;">{analysis['status']}</div></div>""", unsafe_allow_html=True)
        else:
            rp = round(analysis["summary"]["risk_probability"]*100,1)
            rl = analysis["summary"]["risk_level"]
            bs = "background:#EAF2EC;color:#7B9E87;" if rp<40 else ("background:#FBF4E6;color:#C4913A;" if rp<70 else "background:#FAEAE8;color:#B85C52;")
            st.markdown(f"""<div class="interp">
              <div class="interp-head"><div class="interp-head-l"><div class="interp-icon">{icon}</div><div><div class="interp-name">{condition.capitalize()} Risk Assessment</div><div class="interp-sub">Probability: {rp}% · Based on clinical parameters</div></div></div>
              <div class="interp-badge" style="{bs}">{rl}</div></div>
              <div class="interp-body">{analysis['doctor_explanation']}</div></div>""", unsafe_allow_html=True)

    st.divider()

    # 07 EXPORT
    st.markdown("""<div class="sec-head">
      <span class="sec-tag">07</span>
      <span class="sec-title">Export Report</span>
      <div class="sec-rule"></div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""<div class="export-card" style="margin-bottom:16px;">
      <div style="font-size:32px;margin-bottom:14px;">📄</div>
      <div style="font-family:'Playfair Display',serif;font-size:20px;font-weight:700;color:#1C1917;margin-bottom:8px;">Download Full Clinical Report</div>
      <div style="font-size:13px;color:#44403C;line-height:1.6;margin-bottom:20px;max-width:440px;">Generate a comprehensive PDF with all risk assessments, clinical interpretations, and recommendations — ready to share with your provider.</div>
    </div>""", unsafe_allow_html=True)

    if st.button("Generate PDF Report"):
        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=A4)
        els, styles = [], getSampleStyleSheet()
        els.append(Paragraph("AI Health Screening Report", styles["Heading1"]))
        els.append(Spacer(1,.3*inch))
        els.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles["Normal"]))
        els.append(Spacer(1,.4*inch))
        for condition, analysis in results.items():
            els.append(Paragraph(f"{condition.upper()} Assessment", styles["Heading2"]))
            els.append(Spacer(1,.2*inch))
            if "status" in analysis:
                els.append(Paragraph(analysis["status"], styles["Normal"])); els.append(Spacer(1,.3*inch)); continue
            s = analysis["summary"]
            els.append(Paragraph(f"Risk Level: {s['risk_level']}", styles["Normal"]))
            els.append(Paragraph(f"Risk Probability: {round(s['risk_probability']*100,2)}%", styles["Normal"]))
            els.append(Spacer(1,.2*inch))
            els.append(Paragraph("Clinical Interpretation:", styles["Heading3"]))
            els.append(Paragraph(analysis["doctor_explanation"], styles["Normal"]))
            els.append(Spacer(1,.4*inch))
        doc.build(els)
        st.download_button("⬇  Download PDF Report", buf.getvalue(), "AI_Health_Screening_Report.pdf", "application/pdf")

    st.divider()

    # 08 AI ASSISTANT
    st.markdown("""<div class="sec-head">
      <span class="sec-tag">08</span>
      <span class="sec-title">AI Medical Assistant</span>
      <div class="sec-rule"></div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""<div class="ai-card" style="margin-bottom:16px;">
      <div class="ai-card-inner">
        <div class="ai-eyebrow">// Powered by Clinical AI</div>
        <div class="ai-title">Talk to your results.</div>
        <div class="ai-desc">Our AI assistant has full context of your medical report. Ask about your risk factors, what your results mean in plain language, or what lifestyle changes may help.</div>
      </div>
    </div>""", unsafe_allow_html=True)

    if st.button("Open AI Medical Assistant →"):
        st.switch_page("pages/2_Chatbot.py")