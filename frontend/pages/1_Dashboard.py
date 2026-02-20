import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import io
import time
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from datetime import datetime

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(layout="wide", page_title="MedZentic AI", page_icon="🩺")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@300;400;500&display=swap');

:root {
    --bg:         #F8F9FB;
    --bg2:        #F0F2F6;
    --surface:    #FFFFFF;
    --border:     #E2E5EC;
    --border2:    #C8CDD8;
    --text:       #0C111D;
    --text2:      #424E61;
    --muted:      #8895A7;
    --blue:       #2563EB;
    --blue-d:     #1D4ED8;
    --blue-lt:    #EFF4FF;
    --blue-mid:   rgba(37,99,235,0.12);
    --teal:       #0D9488;
    --teal-lt:    #F0FDFA;
    --amber:      #B45309;
    --amber-lt:   #FFFBEB;
    --red:        #DC2626;
    --red-lt:     #FFF1F1;
    --sans:       'Syne', sans-serif;
    --serif:      'Instrument Serif', serif;
    --mono:       'JetBrains Mono', monospace;
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
    padding: 0 60px 120px !important;
    max-width: 1240px !important;
    margin: 0 auto !important;
}

/* ══ NAV ══════════════════════════════════ */
.mz-nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 26px 0 22px;
    border-bottom: 1px solid var(--border);
    animation: navSlide .6s cubic-bezier(.16,1,.3,1) both;
}
.mz-brand { display: flex; align-items: center; gap: 12px; }
.mz-brand-icon {
    width: 38px; height: 38px;
    background: linear-gradient(135deg, #2563EB 0%, #0D9488 100%);
    border-radius: 11px;
    display: flex; align-items: center; justify-content: center;
    box-shadow: 0 4px 14px rgba(37,99,235,.28);
    position: relative; overflow: hidden;
}
.mz-brand-icon::after {
    content: '';
    position: absolute; inset: 0;
    background: linear-gradient(135deg, rgba(255,255,255,.25) 0%, transparent 60%);
}
.mz-brand-icon svg { width: 20px; height: 20px; fill: white; position: relative; z-index:1; }
.mz-brand-name { font-size: 18px; font-weight: 800; letter-spacing: -0.5px; color: var(--text); }
.mz-brand-name em { font-style: normal; color: var(--blue); }
.mz-nav-center {
    display: flex; align-items: center; gap: 6px;
    font-family: var(--mono); font-size: 10.5px; color: var(--muted);
    background: var(--bg2); border: 1px solid var(--border);
    padding: 6px 14px; border-radius: 100px; letter-spacing: 0.3px;
}
.mz-nav-center span { color: var(--blue); font-weight: 500; }
.mz-status { display: flex; align-items: center; gap: 7px; font-size: 12px; font-weight: 600; color: var(--teal); }
.mz-pulse {
    width: 8px; height: 8px; background: var(--teal); border-radius: 50%;
    box-shadow: 0 0 0 0 rgba(13,148,136,.4);
    animation: pulseRing 2s ease-in-out infinite;
}
@keyframes pulseRing {
    0%   { box-shadow: 0 0 0 0 rgba(13,148,136,.4); }
    70%  { box-shadow: 0 0 0 8px rgba(13,148,136,0); }
    100% { box-shadow: 0 0 0 0 rgba(13,148,136,0); }
}
@keyframes navSlide { from{opacity:0;transform:translateY(-16px)} to{opacity:1;transform:translateY(0)} }

/* ══ HERO ══════════════════════════════════ */
.mz-hero {
    display: grid;
    grid-template-columns: 1fr 1fr;
    min-height: 420px;
    position: relative; overflow: hidden;
}
.mz-hero::before {
    content: '';
    position: absolute; right: -120px; top: -120px;
    width: 600px; height: 600px; border-radius: 50%;
    background: radial-gradient(circle, rgba(37,99,235,.06) 0%, transparent 65%);
    pointer-events: none;
}
.mz-hero::after {
    content: '';
    position: absolute; left: 30%; bottom: -80px;
    width: 400px; height: 400px; border-radius: 50%;
    background: radial-gradient(circle, rgba(13,148,136,.05) 0%, transparent 65%);
    pointer-events: none;
}
.mz-hero-left {
    display: flex; flex-direction: column; justify-content: center;
    padding: 72px 48px 72px 0;
    position: relative; z-index: 2;
    animation: heroL .7s cubic-bezier(.16,1,.3,1) .1s both;
}
.mz-hero-right {
    display: flex; flex-direction: column; justify-content: center;
    padding: 72px 0 72px 48px;
    position: relative; z-index: 2;
    border-left: 1px solid var(--border);
    animation: heroR .7s cubic-bezier(.16,1,.3,1) .15s both;
}
@keyframes heroL { from{opacity:0;transform:translateX(-28px)} to{opacity:1;transform:translateX(0)} }
@keyframes heroR { from{opacity:0;transform:translateX(28px)} to{opacity:1;transform:translateX(0)} }

.mz-pill {
    display: inline-flex; align-items: center; gap: 8px;
    font-family: var(--mono); font-size: 10px; font-weight: 500;
    color: var(--blue); background: var(--blue-lt);
    border: 1px solid var(--blue-mid);
    padding: 6px 14px; border-radius: 100px; margin-bottom: 28px; width: fit-content;
    letter-spacing: 0.5px;
}
.mz-pill::before {
    content: ''; width: 6px; height: 6px;
    background: var(--blue); border-radius: 50%;
    animation: pillBlink 2s ease-in-out infinite;
}
@keyframes pillBlink { 0%,100%{opacity:1} 50%{opacity:.3} }
.mz-hero-title {
    font-family: var(--serif); font-size: 52px; font-weight: 400;
    line-height: 1.1; letter-spacing: -1px; color: var(--text); margin-bottom: 18px;
}
.mz-hero-title strong {
    font-style: italic; font-weight: 400;
    background: linear-gradient(135deg, var(--blue) 0%, var(--teal) 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.mz-hero-sub {
    font-size: 15px; font-weight: 400; line-height: 1.7;
    color: var(--text2); max-width: 400px; margin-bottom: 36px;
}
.mz-hero-stats { display: flex; gap: 32px; }
.mz-stat { display: flex; flex-direction: column; gap: 3px; }
.mz-stat-num { font-size: 24px; font-weight: 800; color: var(--text); letter-spacing: -1px; }
.mz-stat-label { font-family: var(--mono); font-size: 10px; color: var(--muted); letter-spacing: 0.3px; }

.mz-upload-label { font-family: var(--mono); font-size: 10px; color: var(--muted); letter-spacing: 1px; text-transform: uppercase; margin-bottom: 16px; }
.mz-upload-title { font-size: 20px; font-weight: 700; color: var(--text); letter-spacing: -0.3px; margin-bottom: 6px; }
.mz-upload-sub { font-size: 13px; color: var(--muted); margin-bottom: 24px; line-height: 1.6; }

[data-testid="stFileUploader"] {
    background: var(--surface) !important;
    border: 2px dashed var(--border2) !important;
    border-radius: 16px !important;
    padding: 28px 20px !important;
    transition: all .25s ease !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--blue) !important;
    background: var(--blue-lt) !important;
    box-shadow: 0 0 0 5px rgba(37,99,235,.06) !important;
}
[data-testid="stFileUploader"] label { display: none !important; }

/* ══ 5-SEC ANALYSIS ANIMATION ══════════════ */
.analysis-overlay {
    position: relative;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 24px;
    padding: 64px 48px;
    overflow: hidden;
    box-shadow: 0 8px 48px rgba(0,0,0,.06), 0 2px 8px rgba(0,0,0,.04);
    animation: overlayIn .4s ease both;
}
@keyframes overlayIn { from{opacity:0;transform:scale(.98)} to{opacity:1;transform:scale(1)} }

.analysis-bg {
    position: absolute; inset: 0; z-index: 0;
    background:
        radial-gradient(ellipse 60% 50% at 20% 30%, rgba(37,99,235,.05) 0%, transparent 60%),
        radial-gradient(ellipse 40% 60% at 80% 70%, rgba(13,148,136,.05) 0%, transparent 55%);
}
.analysis-grid {
    position: absolute; inset: 0; z-index: 0; pointer-events: none;
    background-image: linear-gradient(var(--border) 1px, transparent 1px), linear-gradient(90deg, var(--border) 1px, transparent 1px);
    background-size: 40px 40px; opacity: .35;
}
.analysis-shimmer {
    position: absolute; top: 0; left: 0; right: 0; height: 3px; z-index: 10;
    background: linear-gradient(90deg, transparent 0%, var(--blue) 40%, var(--teal) 60%, transparent 100%);
    background-size: 200% 100%;
    animation: shimmerSlide 1.5s linear infinite;
}
@keyframes shimmerSlide { from{background-position:-100% 0} to{background-position:200% 0} }

.ac { position: absolute; z-index: 1; width: 24px; height: 24px; border-color: var(--blue); border-style: solid; opacity: .4; }
.ac-tl { top:20px; left:20px; border-width:2px 0 0 2px; }
.ac-tr { top:20px; right:20px; border-width:2px 2px 0 0; }
.ac-bl { bottom:20px; left:20px; border-width:0 0 2px 2px; }
.ac-br { bottom:20px; right:20px; border-width:0 2px 2px 0; }

.analysis-content { position: relative; z-index: 2; display: flex; flex-direction: column; align-items: center; }

.analysis-orbital { width: 100px; height: 100px; position: relative; margin-bottom: 36px; }
.orbital-ring { position: absolute; inset: 0; border-radius: 50%; border: 1.5px solid transparent; }
.ring-1 { border-color: rgba(37,99,235,.3); animation: orbitSpin 2s linear infinite; }
.ring-2 { inset: 10px; border-color: rgba(13,148,136,.35); animation: orbitSpin 1.5s linear infinite reverse; }
.ring-3 { inset: 22px; border-color: rgba(37,99,235,.25); animation: orbitSpin 3s linear infinite; }
@keyframes orbitSpin { to { transform: rotate(360deg); } }
.orbital-dot { position: absolute; width: 8px; height: 8px; border-radius: 50%; top: -4px; left: calc(50% - 4px); }
.dot-blue { background: var(--blue); box-shadow: 0 0 10px rgba(37,99,235,.6); }
.dot-teal { background: var(--teal); box-shadow: 0 0 10px rgba(13,148,136,.6); }
.orbital-core {
    position: absolute; inset: 34px; border-radius: 50%;
    background: linear-gradient(135deg, var(--blue), var(--teal));
    display: flex; align-items: center; justify-content: center;
    box-shadow: 0 0 24px rgba(37,99,235,.3);
    animation: corePulse 2s ease-in-out infinite;
}
@keyframes corePulse {
    0%,100% { box-shadow:0 0 24px rgba(37,99,235,.3); transform:scale(1); }
    50%      { box-shadow:0 0 40px rgba(37,99,235,.5); transform:scale(1.05); }
}
.orbital-core svg { width: 16px; height: 16px; fill: white; }

.analysis-title { font-size: 22px; font-weight: 800; color: var(--text); letter-spacing: -0.4px; margin-bottom: 8px; text-align: center; }
.analysis-sub { font-family: var(--mono); font-size: 11px; color: var(--muted); margin-bottom: 40px; letter-spacing: 0.5px; text-align: center; }

.analysis-steps { width: 100%; max-width: 520px; display: flex; flex-direction: column; gap: 14px; margin-bottom: 36px; }
.a-step { display: flex; align-items: center; gap: 14px; }
.a-step-icon {
    width: 30px; height: 30px; border-radius: 8px;
    background: var(--bg2); border: 1px solid var(--border);
    display: flex; align-items: center; justify-content: center;
    font-size: 13px; flex-shrink: 0;
}
.a-step-icon.s1{animation:iconPop .3s ease .0s both}
.a-step-icon.s2{animation:iconPop .3s ease .3s both}
.a-step-icon.s3{animation:iconPop .3s ease .6s both}
.a-step-icon.s4{animation:iconPop .3s ease .9s both}
.a-step-icon.s5{animation:iconPop .3s ease 1.2s both}
@keyframes iconPop { from{opacity:0;transform:scale(.7)} to{opacity:1;transform:scale(1)} }
.a-step-info { flex: 1; }
.a-step-name { font-size: 13px; font-weight: 600; color: var(--text2); margin-bottom: 5px; }
.a-step-track { height: 5px; background: var(--bg2); border-radius: 100px; overflow: hidden; border: 1px solid var(--border); }
.a-step-bar { height: 100%; border-radius: 100px; background: linear-gradient(90deg, var(--blue), var(--teal)); box-shadow: 0 0 8px rgba(37,99,235,.4); }
/* 5 seconds total */
.b1{animation:barFill 5s cubic-bezier(.4,0,.2,1) 0.0s both}
.b2{animation:barFill 5s cubic-bezier(.4,0,.2,1) 0.3s both}
.b3{animation:barFill 5s cubic-bezier(.4,0,.2,1) 0.6s both}
.b4{animation:barFill 5s cubic-bezier(.4,0,.2,1) 0.9s both}
.b5{animation:barFill 5s cubic-bezier(.4,0,.2,1) 1.2s both}
@keyframes barFill { from{width:0} to{width:100%} }
.a-step-pct { font-family: var(--mono); font-size: 10px; color: var(--blue); flex-shrink: 0; width: 36px; text-align: right; }

.analysis-timer { display: flex; flex-direction: column; align-items: center; gap: 8px; }
.timer-arc { position: relative; width: 56px; height: 56px; }
.timer-svg { transform: rotate(-90deg); }
.timer-track { fill: none; stroke: var(--border); stroke-width: 3; }
.timer-fill {
    fill: none; stroke: url(#timerGrad); stroke-width: 3; stroke-linecap: round;
    stroke-dasharray: 138.2; stroke-dashoffset: 138.2;
    animation: arcDrain 5s linear .1s both;
}
@keyframes arcDrain { from{stroke-dashoffset:138.2} to{stroke-dashoffset:0} }
.timer-num {
    position: absolute; inset: 0;
    display: flex; align-items: center; justify-content: center;
    font-family: var(--mono); font-size: 13px; font-weight: 500; color: var(--blue);
}
.timer-label { font-family: var(--mono); font-size: 10px; color: var(--muted); letter-spacing: 0.5px; }
.analysis-ticker {
    margin-top: 20px; font-family: var(--mono); font-size: 10px;
    color: var(--muted); letter-spacing: 0.5px;
    display: flex; align-items: center; gap: 8px;
}
.ticker-dot { width: 5px; height: 5px; background: var(--teal); border-radius: 50%; animation: pillBlink 1s ease-in-out infinite; }

/* ══ SECTIONS ══════════════════════════════ */
.mz-section {
    display: flex; align-items: center; gap: 16px;
    margin: 60px 0 28px;
    animation: fadeUp .5s ease both;
}
.mz-sec-badge {
    font-family: var(--mono); font-size: 10px; font-weight: 500;
    color: var(--blue); background: var(--blue-lt);
    border: 1px solid var(--blue-mid);
    padding: 4px 11px; border-radius: 100px; flex-shrink: 0;
}
.mz-sec-title { font-size: 20px; font-weight: 800; color: var(--text); letter-spacing: -0.4px; }
.mz-sec-rule { flex: 1; height: 1px; background: var(--border); }

/* ══ GAUGE CARDS ════════════════════════════ */
.gauge-card {
    background: var(--surface); border: 1px solid var(--border); border-radius: 20px;
    padding: 24px 20px 16px;
    box-shadow: 0 2px 12px rgba(0,0,0,.04);
    transition: all .25s ease; position: relative; overflow: hidden;
}
.gauge-card::before { content:''; position:absolute; top:0; left:0; right:0; height:3px; }
.gauge-card.low::before  { background:linear-gradient(90deg,var(--teal),#34D399); }
.gauge-card.mid::before  { background:linear-gradient(90deg,var(--amber),#F59E0B); }
.gauge-card.high::before { background:linear-gradient(90deg,var(--red),#F87171); }
.gauge-card:hover { transform:translateY(-3px); box-shadow:0 8px 32px rgba(0,0,0,.08); }
.gauge-label { font-family:var(--mono); font-size:10px; font-weight:500; color:var(--muted); letter-spacing:1px; text-transform:uppercase; margin-bottom:4px; }
.gauge-risk-pill { display:inline-block; font-size:11px; font-weight:700; padding:3px 12px; border-radius:100px; margin-top:8px; }
.pill-low  { background:var(--teal-lt); color:var(--teal); }
.pill-mid  { background:var(--amber-lt); color:var(--amber); }
.pill-high { background:var(--red-lt); color:var(--red); }

/* ══ CHART WRAP ══════════════════════════════ */
.chart-wrap {
    background: var(--surface); border: 1px solid var(--border); border-radius: 20px;
    padding: 28px 24px 20px;
    box-shadow: 0 2px 12px rgba(0,0,0,.04);
}

/* ══ FLAGS ════════════════════════════════════ */
.flag-item {
    display:flex; align-items:flex-start; gap:16px;
    background:var(--red-lt); border:1px solid rgba(220,38,38,.18); border-left:3px solid var(--red);
    border-radius:12px; padding:16px 20px; margin-bottom:10px;
    animation:flagIn .4s ease both;
}
.flag-ok-item {
    display:flex; align-items:center; gap:16px;
    background:var(--teal-lt); border:1px solid rgba(13,148,136,.2); border-left:3px solid var(--teal);
    border-radius:12px; padding:18px 20px;
}
.flag-emoji { font-size:18px; margin-top:1px; }
.flag-heading { font-size:13px; font-weight:700; color:var(--red); margin-bottom:2px; }
.flag-detail  { font-family:var(--mono); font-size:10px; color:rgba(220,38,38,.6); }
.flag-ok-text { font-size:13px; font-weight:700; color:var(--teal); }
@keyframes flagIn { from{opacity:0;transform:translateX(-12px)} to{opacity:1;transform:translateX(0)} }

/* ══ INTERP CARDS ════════════════════════════ */
.interp-card {
    background:var(--surface); border:1px solid var(--border); border-radius:20px;
    overflow:hidden; margin-bottom:16px;
    box-shadow:0 2px 12px rgba(0,0,0,.04);
    transition:box-shadow .25s ease; animation:fadeUp .45s ease both;
}
.interp-card:hover { box-shadow:0 8px 32px rgba(0,0,0,.08); }
.interp-head {
    display:flex; align-items:center; justify-content:space-between;
    padding:18px 24px; background:var(--bg2); border-bottom:1px solid var(--border);
}
.interp-head-left { display:flex; align-items:center; gap:12px; }
.interp-icon {
    width:32px; height:32px; border-radius:9px;
    background:var(--blue-lt); border:1px solid var(--blue-mid);
    display:flex; align-items:center; justify-content:center; font-size:15px;
}
.interp-name { font-size:13px; font-weight:700; color:var(--text); letter-spacing:-0.2px; }
.interp-sub  { font-family:var(--mono); font-size:10px; color:var(--muted); margin-top:1px; }
.interp-risk-badge { font-size:11px; font-weight:700; padding:4px 12px; border-radius:100px; }
.interp-body { padding:22px 24px; font-size:14px; line-height:1.75; color:var(--text2); }

/* ══ BUTTONS ══════════════════════════════════ */
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, var(--blue) 0%, #1D4ED8 100%) !important;
    color: white !important; font-family: var(--sans) !important;
    font-weight: 700 !important; font-size: 14px !important; letter-spacing: -0.2px !important;
    border: none !important; border-radius: 12px !important;
    padding: 14px 32px !important;
    box-shadow: 0 4px 16px rgba(37,99,235,.3) !important;
    transition: all .2s ease !important; position: relative !important; overflow: hidden !important;
}
div[data-testid="stButton"] > button::before {
    content:'' !important; position:absolute !important; inset:0 !important;
    background:linear-gradient(135deg,rgba(255,255,255,.15) 0%,transparent 60%) !important;
}
div[data-testid="stButton"] > button:hover { transform:translateY(-2px) !important; box-shadow:0 8px 28px rgba(37,99,235,.4) !important; }

div[data-testid="stDownloadButton"] > button {
    background: var(--surface) !important; color: var(--blue) !important;
    font-family: var(--sans) !important; font-weight: 700 !important; font-size: 13px !important;
    border: 1.5px solid var(--blue) !important; border-radius: 12px !important;
    padding: 13px 28px !important; transition: all .2s ease !important; box-shadow: none !important;
}
div[data-testid="stDownloadButton"] > button:hover {
    background: var(--blue-lt) !important; box-shadow: 0 4px 16px rgba(37,99,235,.15) !important; transform: translateY(-1px) !important;
}

/* ══ METRICS ══════════════════════════════════ */
[data-testid="stMetric"] {
    background:var(--surface) !important; border:1px solid var(--border) !important;
    border-radius:16px !important; padding:24px !important;
    box-shadow:0 2px 8px rgba(0,0,0,.04) !important; transition:all .2s ease !important;
}
[data-testid="stMetric"]:hover { box-shadow:0 6px 24px rgba(0,0,0,.07) !important; transform:translateY(-2px) !important; border-color:var(--blue) !important; }
[data-testid="stMetricLabel"] { font-family:var(--mono) !important; font-size:10px !important; text-transform:uppercase !important; letter-spacing:0.8px !important; color:var(--muted) !important; }
[data-testid="stMetricValue"] { font-size:34px !important; font-weight:800 !important; letter-spacing:-1.5px !important; color:var(--text) !important; }

[data-testid="stAlert"] { border-radius:12px !important; font-size:13px !important; font-weight:500 !important; }

hr { border:none !important; height:1px !important; background:var(--border) !important; margin:52px 0 !important; }

/* ══ EXPORT / AI CARDS ════════════════════════ */
.export-card {
    background: linear-gradient(135deg, var(--blue-lt) 0%, var(--teal-lt) 100%);
    border: 1px solid var(--blue-mid); border-radius: 20px;
    padding: 36px 40px;
}
.export-card-title { font-size:18px; font-weight:800; color:var(--text); letter-spacing:-0.4px; margin:12px 0 6px; }
.export-card-desc  { font-size:13px; color:var(--text2); line-height:1.6; margin-bottom:20px; }

.ai-card {
    background: linear-gradient(135deg, #0C111D 0%, #1e293b 100%);
    border: 1px solid rgba(255,255,255,.08); border-radius: 20px;
    padding: 40px; position: relative; overflow: hidden;
}
.ai-card::before {
    content:''; position:absolute; top:-60px; right:-60px;
    width:300px; height:300px; border-radius:50%;
    background:radial-gradient(circle,rgba(37,99,235,.2) 0%,transparent 65%);
}
.ai-card::after {
    content:''; position:absolute; bottom:-40px; left:30%;
    width:200px; height:200px; border-radius:50%;
    background:radial-gradient(circle,rgba(13,148,136,.15) 0%,transparent 65%);
}
.ai-card-inner  { position:relative; z-index:1; }
.ai-card-eyebrow{ font-family:var(--mono); font-size:10px; color:rgba(255,255,255,.4); letter-spacing:1px; text-transform:uppercase; margin-bottom:10px; }
.ai-card-title  { font-family:var(--serif); font-size:32px; color:white; letter-spacing:-0.5px; margin-bottom:10px; font-style:italic; }
.ai-card-desc   { font-size:14px; color:rgba(255,255,255,.55); line-height:1.7; max-width:480px; margin-bottom:28px; }

/* ══ ANIMATIONS ═══════════════════════════════ */
@keyframes fadeUp { from{opacity:0;transform:translateY(22px)} to{opacity:1;transform:translateY(0)} }
@keyframes fadeIn { from{opacity:0} to{opacity:1} }
[data-testid="stHorizontalBlock"] { gap:20px !important; }
</style>
""", unsafe_allow_html=True)

# ═══ NAV
st.markdown("""
<div class="mz-nav">
  <div class="mz-brand">
    <div class="mz-brand-icon">
      <svg viewBox="0 0 24 24"><path d="M12 2a10 10 0 100 20A10 10 0 0012 2zm1 14.5h-2v-6h2v6zm0-8h-2V6h2v2.5z"/></svg>
    </div>
    <div class="mz-brand-name">Med<em>Zentic</em></div>
  </div>
  <div class="mz-nav-center">AI Health Intelligence &nbsp;·&nbsp; <span>Clinical Edition</span></div>
  <div class="mz-status"><div class="mz-pulse"></div>All systems operational</div>
</div>
""", unsafe_allow_html=True)

# ═══ HERO
st.markdown("""
<div class="mz-hero">
  <div class="mz-hero-left">
    <div class="mz-pill">AI-Powered Medical Analysis</div>
    <div class="mz-hero-title">Your health data,<br><strong>intelligently decoded.</strong></div>
    <div class="mz-hero-sub">Upload your medical report and receive a detailed risk assessment across diabetes, cardiac health, and neurological indicators — powered by clinical-grade AI models.</div>
    <div class="mz-hero-stats">
      <div class="mz-stat"><div class="mz-stat-num">3</div><div class="mz-stat-label">AI Models</div></div>
      <div class="mz-stat"><div class="mz-stat-num">~5s</div><div class="mz-stat-label">Analysis Time</div></div>
      <div class="mz-stat"><div class="mz-stat-num">PDF</div><div class="mz-stat-label">Export Ready</div></div>
    </div>
  </div>
  <div class="mz-hero-right">
    <div class="mz-upload-label">// Step 01 — Input</div>
    <div class="mz-upload-title">Upload Medical Report</div>
    <div class="mz-upload-sub">Drag & drop your PDF below. Clinical data is extracted and analyzed automatically.</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"], label_visibility="collapsed")

st.markdown("</div></div>", unsafe_allow_html=True)

# ═══ INIT
results = {}
extracted_values = {}

if uploaded_file:

    # ═══ 5-SECOND ANALYSIS ANIMATION
    scan_ph = st.empty()
    scan_ph.markdown("""
    <div class="analysis-overlay">
      <div class="analysis-bg"></div>
      <div class="analysis-grid"></div>
      <div class="analysis-shimmer"></div>
      <div class="ac ac-tl"></div>
      <div class="ac ac-tr"></div>
      <div class="ac ac-bl"></div>
      <div class="ac ac-br"></div>
      <div class="analysis-content">
        <div class="analysis-orbital">
          <div class="orbital-ring ring-1"><div class="orbital-dot dot-blue"></div></div>
          <div class="orbital-ring ring-2"><div class="orbital-dot dot-teal"></div></div>
          <div class="orbital-ring ring-3"></div>
          <div class="orbital-core">
            <svg viewBox="0 0 24 24"><path d="M12 2a10 10 0 100 20A10 10 0 0012 2zm1 14.5h-2v-6h2v6zm0-8h-2V6h2v2.5z"/></svg>
          </div>
        </div>
        <div class="analysis-title">Analyzing your medical report</div>
        <div class="analysis-sub">Clinical AI models are processing your data — approx. 5 seconds</div>
        <div class="analysis-steps">
          <div class="a-step"><div class="a-step-icon s1">🔬</div><div class="a-step-info"><div class="a-step-name">Extracting Lab Values</div><div class="a-step-track"><div class="a-step-bar b1"></div></div></div><div class="a-step-pct p1">100%</div></div>
          <div class="a-step"><div class="a-step-icon s2">🧠</div><div class="a-step-info"><div class="a-step-name">Running ML Models</div><div class="a-step-track"><div class="a-step-bar b2"></div></div></div><div class="a-step-pct p2">100%</div></div>
          <div class="a-step"><div class="a-step-icon s3">🩸</div><div class="a-step-info"><div class="a-step-name">Diabetes Assessment</div><div class="a-step-track"><div class="a-step-bar b3"></div></div></div><div class="a-step-pct p3">100%</div></div>
          <div class="a-step"><div class="a-step-icon s4">❤️</div><div class="a-step-info"><div class="a-step-name">Cardiac Risk Analysis</div><div class="a-step-track"><div class="a-step-bar b4"></div></div></div><div class="a-step-pct p4">100%</div></div>
          <div class="a-step"><div class="a-step-icon s5">🧬</div><div class="a-step-info"><div class="a-step-name">Neurological Scan</div><div class="a-step-track"><div class="a-step-bar b5"></div></div></div><div class="a-step-pct p5">100%</div></div>
        </div>
        <div class="analysis-timer">
          <div class="timer-arc">
            <svg class="timer-svg" width="56" height="56" viewBox="0 0 56 56">
              <defs>
                <linearGradient id="timerGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stop-color="#2563EB"/>
                  <stop offset="100%" stop-color="#0D9488"/>
                </linearGradient>
              </defs>
              <circle class="timer-track" cx="28" cy="28" r="22"/>
              <circle class="timer-fill" cx="28" cy="28" r="22"/>
            </svg>
            <div class="timer-num">5s</div>
          </div>
          <div class="timer-label">estimated time</div>
        </div>
        <div class="analysis-ticker"><div class="ticker-dot"></div>Processing clinical parameters in real-time…</div>
      </div>
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

    # ═══ 01 RISK GAUGE CARDS
    st.markdown("""
    <div class="mz-section">
      <span class="mz-sec-badge">01</span>
      <span class="mz-sec-title">Condition Risk Summary</span>
      <div class="mz-sec-rule"></div>
    </div>
    """, unsafe_allow_html=True)

    if valid_results:
        cols = st.columns(len(valid_results))
        cond_icons = {"diabetes": "🩸", "heart": "❤️", "parkinson": "🧬"}
        for idx, (condition, analysis) in enumerate(valid_results.items()):
            summary = analysis["summary"]
            prob = summary["risk_probability"] * 100
            risk = summary["risk_level"]
            icon = cond_icons.get(condition, "🔬")
            if prob < 40:
                gc, cc, pc = "#0D9488", "low", "pill-low"
                steps = [{'range':[0,40],'color':'rgba(13,148,136,0.1)'},{'range':[40,70],'color':'rgba(217,119,6,0.04)'},{'range':[70,100],'color':'rgba(220,38,38,0.04)'}]
            elif prob < 70:
                gc, cc, pc = "#B45309", "mid", "pill-mid"
                steps = [{'range':[0,40],'color':'rgba(13,148,136,0.04)'},{'range':[40,70],'color':'rgba(180,83,9,0.1)'},{'range':[70,100],'color':'rgba(220,38,38,0.04)'}]
            else:
                gc, cc, pc = "#DC2626", "high", "pill-high"
                steps = [{'range':[0,40],'color':'rgba(13,148,136,0.04)'},{'range':[40,70],'color':'rgba(217,119,6,0.04)'},{'range':[70,100],'color':'rgba(220,38,38,0.1)'}]
            with cols[idx]:
                st.markdown(f'<div class="gauge-card {cc}"><div class="gauge-label">{icon} {condition.upper()}</div>', unsafe_allow_html=True)
                fig = go.Figure(go.Indicator(
                    mode="gauge+number", value=prob,
                    number={'suffix':"%",'font':{'color':'#0C111D','size':32,'family':'Syne'},'valueformat':'.1f'},
                    gauge={'axis':{'range':[0,100],'tickcolor':'#C8CDD8','tickfont':{'color':'#8895A7','size':9,'family':'JetBrains Mono'},'tickwidth':1,'nticks':5},
                           'bar':{'color':gc,'thickness':0.28},'bgcolor':'rgba(0,0,0,0)','borderwidth':0,
                           'steps':steps,'threshold':{'line':{'color':gc,'width':2},'thickness':0.85,'value':prob}}
                ))
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
                                  margin=dict(t=16,b=0,l=16,r=16),height=200,font_color='#0C111D')
                st.plotly_chart(fig, use_container_width=True)
                st.markdown(f'<div class="gauge-risk-pill {pc}">{risk}</div></div>', unsafe_allow_html=True)

    st.divider()

    # ═══ 02 COMPOSITE SCORE
    st.markdown("""
    <div class="mz-section">
      <span class="mz-sec-badge">02</span>
      <span class="mz-sec-title">Composite Health Risk Score</span>
      <div class="mz-sec-rule"></div>
    </div>
    """, unsafe_allow_html=True)

valid_results = {k: v for k, v in results.items() if "status" not in v}

if valid_results:
    weights = {"diabetes": 0.4, "heart": 0.4, "parkinson": 0.2}
    weighted_score, probabilities = 0, []
    for disease, analysis in valid_results.items():
        p = analysis["summary"]["risk_probability"]
        probabilities.append(p)
        if disease in weights: weighted_score += p * weights[disease]
    overall = weighted_score
    if max(probabilities) >= 0.75: overall = max(overall, 0.75)
    if sum(p >= 0.6 for p in probabilities) >= 2: overall = min(overall + 0.10, 1.0)
    pct = int(overall * 100)

    if pct < 40:
        sc, vbg, vc = "#0D9488", "#F0FDFA", "#0D9488"; verdict = "Low Risk"
        desc = "Your combined health indicators suggest a low overall risk profile. Continue with routine wellness check-ups and maintain your current health habits."
    elif pct < 70:
        sc, vbg, vc = "#B45309", "#FFFBEB", "#B45309"; verdict = "Moderate Risk"
        desc = "Moderate combined health risk detected across your indicators. We recommend scheduling a consultation with your healthcare provider for a more detailed evaluation."
    else:
        sc, vbg, vc = "#DC2626", "#FFF1F1", "#DC2626"; verdict = "High Risk"
        desc = "High combined health risk identified. Please seek medical consultation promptly. Early intervention significantly improves outcomes."

    fig_score = go.Figure(go.Pie(
        values=[pct, 100-pct], labels=["Risk","Safe"], hole=0.75,
        marker=dict(colors=[sc,"#F0F2F6"], line=dict(color='white',width=3)),
        showlegend=False, hoverinfo='skip', textinfo='none',
    ))
    fig_score.update_layout(paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=0,b=0,l=0,r=0), height=140, width=140)

    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown(f"""
        <div style="background:var(--surface,#fff); border:1px solid var(--border,#E2E5EC); border-radius:20px; padding:32px; box-shadow:0 2px 12px rgba(0,0,0,.04); display:flex; flex-direction:column; align-items:center; gap:8px;">
          <div style="font-family:'JetBrains Mono',monospace; font-size:10px; color:#8895A7; text-transform:uppercase; letter-spacing:0.8px; align-self:flex-start;">Overall Score</div>
          <div style="font-family:'Syne',sans-serif; font-size:72px; font-weight:800; letter-spacing:-4px; line-height:1; color:{sc};">{pct}</div>
          <div style="font-size:12px; font-weight:700; color:{vc}; background:{vbg}; padding:5px 14px; border-radius:100px;">{verdict}</div>
        </div>
        """, unsafe_allow_html=True)
        st.plotly_chart(fig_score, use_container_width=False)
    with c2:
        st.markdown(f"""
        <div style="background:var(--surface,#fff); border:1px solid var(--border,#E2E5EC); border-radius:20px; padding:32px; height:100%; box-shadow:0 2px 12px rgba(0,0,0,.04);">
          <div style="font-family:'JetBrains Mono',monospace; font-size:10px; color:#8895A7; text-transform:uppercase; letter-spacing:0.8px; margin-bottom:12px;">Clinical Assessment</div>
          <div style="font-family:'Syne',sans-serif; font-size:16px; font-weight:700; color:#0C111D; line-height:1.5; margin-bottom:14px;">{verdict}</div>
          <div style="font-size:14px; color:#424E61; line-height:1.75;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ═══ 03 RISK COMPARISON
    st.markdown("""
    <div class="mz-section">
      <span class="mz-sec-badge">03</span>
      <span class="mz-sec-title">Disease Risk Comparison</span>
      <div class="mz-sec-rule"></div>
    </div>
    """, unsafe_allow_html=True)

    risk_df = pd.DataFrame([
        {"Condition": c.capitalize(), "Risk": round(a["summary"]["risk_probability"]*100,1)}
        for c,a in valid_results.items()
    ])
    def bcolor(v):
        if v<40: return "#0D9488"
        if v<70: return "#B45309"
        return "#DC2626"

    fig_bar = go.Figure()
    for _, row in risk_df.iterrows():
        fig_bar.add_trace(go.Bar(
            x=[row["Condition"]], y=[row["Risk"]],
            marker_color=bcolor(row["Risk"]), marker_line_width=0,
            text=[f'{row["Risk"]:.1f}%'], textposition='outside',
            textfont=dict(family='Syne',size=14,color='#0C111D'), width=0.38, name=row["Condition"],
        ))
    fig_bar.add_hline(y=40, line_dash="dot", line_color="rgba(13,148,136,.4)", line_width=1,
                      annotation_text="Low / Moderate", annotation_font_size=9, annotation_font_color="#8895A7", annotation_position="right")
    fig_bar.add_hline(y=70, line_dash="dot", line_color="rgba(220,38,38,.4)", line_width=1,
                      annotation_text="Moderate / High", annotation_font_size=9, annotation_font_color="#8895A7", annotation_position="right")
    fig_bar.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False,
        font=dict(family='Syne',color='#0C111D'),
        xaxis=dict(showgrid=False, showline=False, tickfont=dict(size=14,color='#424E61',family='Syne')),
        yaxis=dict(showgrid=True, gridcolor='#E2E5EC', gridwidth=1, tickfont=dict(color='#8895A7',size=10,family='JetBrains Mono'), ticksuffix='%', range=[0,115], zeroline=False),
        margin=dict(t=20,b=10,l=0,r=90), height=340, bargap=0.5,
    )
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    # ═══ 04 LAB DISTRIBUTION
    if extracted_values:
        st.markdown("""
        <div class="mz-section">
          <span class="mz-sec-badge">04</span>
          <span class="mz-sec-title">Lab Parameter Distribution</span>
          <div class="mz-sec-rule"></div>
        </div>
        """, unsafe_allow_html=True)

        elevated = sum(1 for v in extracted_values.values() if v > 200)
        normal = len(extracted_values) - elevated
        total = len(extracted_values)

        col_a, col_b = st.columns(2)
        with col_a:
            fig_pie = go.Figure(go.Pie(
                labels=["Within Range","Elevated"], values=[normal, elevated], hole=0.65,
                marker=dict(colors=["#0D9488","#DC2626"], line=dict(color='#F8F9FB',width=4)),
                textfont=dict(family='Syne',size=13),
                hovertemplate='<b>%{label}</b><br>%{value} parameters<br>%{percent}<extra></extra>',
                showlegend=False,
            ))
            fig_pie.add_annotation(text=f"<b>{total}</b>", x=0.5, y=0.58, font=dict(family='Syne',size=36,color='#0C111D'), showarrow=False)
            fig_pie.add_annotation(text="parameters",   x=0.5, y=0.40, font=dict(family='JetBrains Mono',size=11,color='#8895A7'), showarrow=False)
            fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(family='Syne'), margin=dict(t=8,b=8,l=8,r=8), height=300)
            st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
            st.plotly_chart(fig_pie, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with col_b:
            nr = round(normal/total*100) if total else 0
            er = round(elevated/total*100) if total else 0
            st.markdown(f"""
            <div style="display:flex;flex-direction:column;gap:16px;padding-top:8px;">
              <div style="background:#F0FDFA;border:1px solid rgba(13,148,136,.2);border-left:3px solid #0D9488;border-radius:14px;padding:24px 28px;">
                <div style="font-family:'JetBrains Mono',monospace;font-size:10px;color:#0D9488;text-transform:uppercase;letter-spacing:0.8px;margin-bottom:10px;">Within Normal Range</div>
                <div style="font-family:'Syne',sans-serif;font-size:48px;font-weight:800;color:#0C111D;letter-spacing:-2px;line-height:1;">{normal}</div>
                <div style="font-size:13px;color:#424E61;margin-top:6px;font-weight:500;">{nr}% of parameters tested</div>
              </div>
              <div style="background:#FFF1F1;border:1px solid rgba(220,38,38,.2);border-left:3px solid #DC2626;border-radius:14px;padding:24px 28px;">
                <div style="font-family:'JetBrains Mono',monospace;font-size:10px;color:#DC2626;text-transform:uppercase;letter-spacing:0.8px;margin-bottom:10px;">Elevated / Flagged</div>
                <div style="font-family:'Syne',sans-serif;font-size:48px;font-weight:800;color:#0C111D;letter-spacing:-2px;line-height:1;">{elevated}</div>
                <div style="font-size:13px;color:#424E61;margin-top:6px;font-weight:500;">{er}% require attention</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # ═══ 05 RISK FLAGS
    st.markdown("""
    <div class="mz-section">
      <span class="mz-sec-badge">05</span>
      <span class="mz-sec-title">Clinical Risk Flags</span>
      <div class="mz-sec-rule"></div>
    </div>
    """, unsafe_allow_html=True)

    flags = []
    if extracted_values.get("Glucose",0) > 140:        flags.append(("🩸","Elevated Blood Glucose",f"Detected: {extracted_values.get('Glucose')} mg/dL · Threshold: 140 mg/dL"))
    if extracted_values.get("Cholesterol",0) > 240:    flags.append(("⚠️","High Cholesterol",f"Detected: {extracted_values.get('Cholesterol')} mg/dL · Threshold: 240 mg/dL"))
    if extracted_values.get("Blood Pressure",0) > 140: flags.append(("💓","High Blood Pressure",f"Detected: {extracted_values.get('Blood Pressure')} mmHg · Threshold: 140 mmHg"))
    if extracted_values.get("BMI",0) > 30:             flags.append(("📊","Obesity Indicator",f"BMI: {extracted_values.get('BMI')} · Threshold: 30"))

    if flags:
        for emoji,title,detail in flags:
            st.markdown(f'<div class="flag-item"><div class="flag-emoji">{emoji}</div><div><div class="flag-heading">{title}</div><div class="flag-detail">{detail}</div></div></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="flag-ok-item"><div class="flag-emoji">✅</div><div class="flag-ok-text">No major cardiometabolic risk indicators detected. All key parameters within safe thresholds.</div></div>', unsafe_allow_html=True)

    st.divider()

    # ═══ 06 CLINICAL INTERPRETATION
    st.markdown("""
    <div class="mz-section">
      <span class="mz-sec-badge">06</span>
      <span class="mz-sec-title">Clinical Interpretation</span>
      <div class="mz-sec-rule"></div>
    </div>
    """, unsafe_allow_html=True)

    cond_icons = {"diabetes":"🩸","heart":"❤️","parkinson":"🧬"}
    for condition, analysis in results.items():
        icon = cond_icons.get(condition,"🔬")
        if "status" in analysis:
            st.markdown(f"""
            <div class="interp-card">
              <div class="interp-head">
                <div class="interp-head-left"><div class="interp-icon">{icon}</div><div><div class="interp-name">{condition.capitalize()} Assessment</div><div class="interp-sub">Insufficient data for full analysis</div></div></div>
                <div class="interp-risk-badge" style="background:#FFFBEB;color:#B45309;">Skipped</div>
              </div>
              <div class="interp-body" style="color:#B45309;">{analysis['status']}</div>
            </div>""", unsafe_allow_html=True)
        else:
            rp = round(analysis["summary"]["risk_probability"]*100,1)
            rl = analysis["summary"]["risk_level"]
            bs = "background:#F0FDFA;color:#0D9488;" if rp<40 else ("background:#FFFBEB;color:#B45309;" if rp<70 else "background:#FFF1F1;color:#DC2626;")
            st.markdown(f"""
            <div class="interp-card">
              <div class="interp-head">
                <div class="interp-head-left"><div class="interp-icon">{icon}</div><div><div class="interp-name">{condition.capitalize()} Risk Assessment</div><div class="interp-sub">Probability: {rp}% · Based on clinical parameters</div></div></div>
                <div class="interp-risk-badge" style="{bs}">{rl}</div>
              </div>
              <div class="interp-body">{analysis['doctor_explanation']}</div>
            </div>""", unsafe_allow_html=True)

    st.divider()

    # ═══ 07 EXPORT
    st.markdown("""
    <div class="mz-section">
      <span class="mz-sec-badge">07</span>
      <span class="mz-sec-title">Export Report</span>
      <div class="mz-sec-rule"></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="export-card">
      <div style="font-size:32px;margin-bottom:12px;">📄</div>
      <div class="export-card-title">Download Full Clinical Report</div>
      <div class="export-card-desc">Generate a comprehensive PDF with all risk assessments, clinical interpretations, and recommendations — ready to share with your healthcare provider.</div>
    </div><br/>
    """, unsafe_allow_html=True)

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

    # ═══ 08 AI ASSISTANT
    st.markdown("""
    <div class="mz-section">
      <span class="mz-sec-badge">08</span>
      <span class="mz-sec-title">AI Medical Assistant</span>
      <div class="mz-sec-rule"></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="ai-card">
      <div class="ai-card-inner">
        <div class="ai-card-eyebrow">// Powered by Clinical AI</div>
        <div class="ai-card-title">Talk to your results.</div>
        <div class="ai-card-desc">Our AI assistant has full context of your medical report and analysis. Ask about your specific risk factors, what your results mean in plain language, or what lifestyle changes may improve your scores.</div>
      </div>
    </div><br/>
    """, unsafe_allow_html=True)

    if st.button("Open AI Medical Assistant →"):
        st.switch_page("pages/2_Chatbot.py")