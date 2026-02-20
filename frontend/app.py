import streamlit as st

st.set_page_config(
    page_title="MedZentic AI",
    page_icon="",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Outfit:wght@200;300;400;600;700;900&display=swap');

:root {
    --bg:        #030507;
    --surface:   #080d12;
    --border:    rgba(255,255,255,0.07);
    --border-hi: rgba(255,255,255,0.18);
    --text:      #f0f4f8;
    --muted:     rgba(240,244,248,0.35);
    --pulse:     #4af0c4;
    --danger:    #f05a4a;
    --mono:      'Space Mono', monospace;
    --sans:      'Outfit', sans-serif;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: var(--sans) !important;
    overflow-x: hidden;
}

#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stSidebarNav"],
section[data-testid="stSidebar"] { display: none !important; }

[data-testid="stAppViewContainer"] > .main > div {
    padding: 0 !important; max-width: 100% !important;
}

/* Scanlines */
body::before {
    content: '';
    position: fixed; inset: 0; pointer-events: none; z-index: 9999;
    background: repeating-linear-gradient(
        0deg, transparent, transparent 2px,
        rgba(0,0,0,0.06) 2px, rgba(0,0,0,0.06) 4px
    );
}

/* ECG BG */
.ecg-bg {
    position: fixed; top: 0; left: 0;
    width: 100%; height: 100%;
    pointer-events: none; z-index: 0; overflow: hidden;
}
.ecg-line {
    position: absolute; width: 200%; top: 35%; left: -100%;
}
.ecg-line svg {
    width: 100%; height: 80px; margin-top: -40px;
    opacity: 0.05;
    animation: ecgScroll 14s linear infinite;
}
@keyframes ecgScroll {
    from { transform: translateX(0); }
    to   { transform: translateX(50%); }
}
.ecg-bg::after {
    content: '';
    position: absolute; inset: 0;
    background-image:
        linear-gradient(rgba(255,255,255,0.015) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.015) 1px, transparent 1px);
    background-size: 48px 48px;
}

/* PAGE */
.mz-page {
    position: relative; z-index: 1;
    min-height: 100vh;
    display: flex; flex-direction: column; align-items: center;
    padding: 0 40px 80px;
}

/* NAV */
.mz-nav {
    width: 100%; max-width: 1200px;
    display: flex; align-items: center; justify-content: space-between;
    padding: 32px 0;
    border-bottom: 1px solid var(--border);
    animation: fadeDown 0.8s ease both;
}
.mz-wordmark {
    font-family: var(--sans);
    font-weight: 900; font-size: 17px; letter-spacing: 4px;
    text-transform: uppercase; color: var(--text);
}
.mz-wordmark span { color: var(--pulse); }
.mz-nav-meta {
    font-family: var(--mono); font-size: 10px; letter-spacing: 2px;
    color: var(--muted); text-transform: uppercase;
}
.mz-status-dot {
    display: inline-flex; align-items: center; gap: 8px;
    font-family: var(--mono); font-size: 10px; letter-spacing: 2px;
    text-transform: uppercase; color: var(--pulse);
}
.mz-status-dot::before {
    content: '';
    width: 7px; height: 7px; border-radius: 50%;
    background: var(--pulse); box-shadow: 0 0 8px var(--pulse);
    animation: blink 1.4s ease-in-out infinite;
}
@keyframes blink {
    0%,100% { opacity: 1; } 50% { opacity: 0.2; }
}

/* HERO */
.mz-hero {
    width: 100%; max-width: 1200px;
    padding: 96px 0 72px;
    display: grid;
    grid-template-columns: 1fr 400px;
    gap: 80px; align-items: center;
    animation: fadeUp 1s ease 0.15s both;
}
.mz-tag {
    font-family: var(--mono); font-size: 10px; letter-spacing: 3px;
    text-transform: uppercase; color: var(--muted);
    margin-bottom: 28px;
    display: flex; align-items: center; gap: 12px;
}
.mz-tag::before { content: ''; display: block; width: 24px; height: 1px; background: var(--muted); }
.mz-h1 {
    font-family: var(--sans);
    font-size: clamp(50px, 5.5vw, 84px);
    font-weight: 900; line-height: 0.95;
    letter-spacing: -4px; color: var(--text); margin-bottom: 32px;
}
.mz-h1 em {
    font-style: normal;
    -webkit-text-fill-color: transparent;
    -webkit-text-stroke: 1px rgba(240,244,248,0.45);
}
.mz-hero-desc {
    font-size: 15px; font-weight: 300; line-height: 1.85;
    color: var(--muted); max-width: 460px;
}

/* VITALS PANEL */
.mz-vitals {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 3px; padding: 28px;
    position: relative; overflow: hidden;
}
.mz-vitals::before {
    content: '';
    position: absolute; top: 0; left: 0;
    height: 2px; width: 0%;
    background: var(--pulse);
    animation: topScan 3s ease-in-out infinite;
}
@keyframes topScan {
    0%   { width: 0%;   opacity: 1; }
    60%  { width: 100%; opacity: 1; }
    100% { width: 100%; opacity: 0; }
}
.mz-vitals-title {
    font-family: var(--mono); font-size: 9px; letter-spacing: 3px;
    text-transform: uppercase; color: var(--muted); margin-bottom: 22px;
}
.mz-vital-row {
    display: flex; justify-content: space-between; align-items: center;
    padding: 11px 0; border-bottom: 1px solid var(--border);
}
.mz-vital-row:last-child { border-bottom: none; }
.mz-vital-label {
    font-family: var(--mono); font-size: 9px; letter-spacing: 1px;
    color: var(--muted); text-transform: uppercase;
}
.mz-vital-value {
    font-family: var(--mono); font-size: 16px; font-weight: 700; color: var(--text);
}
.mz-vital-value.ok { color: var(--pulse); }
.mz-vital-bar { width: 72px; height: 2px; background: var(--border); border-radius: 2px; overflow: hidden; margin-top: 5px; }
.mz-vital-fill { height: 100%; background: var(--pulse); border-radius: 2px; animation: fillAnim 2s ease both; }
@keyframes fillAnim { from { width: 0%; } }

/* STATS */
.mz-stats {
    width: 100%; max-width: 1200px;
    display: grid; grid-template-columns: repeat(4,1fr);
    border: 1px solid var(--border); border-radius: 3px; overflow: hidden;
    margin-bottom: 80px;
    animation: fadeUp 1s ease 0.3s both;
}
.mz-stat {
    padding: 32px 28px; border-right: 1px solid var(--border);
    position: relative;
}
.mz-stat:last-child { border-right: none; }
.mz-stat::after {
    content: attr(data-idx);
    position: absolute; bottom: 14px; right: 18px;
    font-family: var(--mono); font-size: 9px; color: rgba(255,255,255,0.06); letter-spacing: 2px;
}
.mz-stat-n {
    font-family: var(--sans); font-size: 44px; font-weight: 900;
    letter-spacing: -2px; color: var(--text); line-height: 1; margin-bottom: 8px;
}
.mz-stat-n span { font-size: 22px; color: var(--pulse); }
.mz-stat-l {
    font-family: var(--mono); font-size: 9px; letter-spacing: 2px;
    text-transform: uppercase; color: var(--muted);
}

/* FEATURES */
.mz-features {
    width: 100%; max-width: 1200px;
    display: grid; grid-template-columns: repeat(3,1fr);
    gap: 1px; background: var(--border);
    border: 1px solid var(--border); border-radius: 3px; overflow: hidden;
    margin-bottom: 80px;
    animation: fadeUp 1s ease 0.45s both;
}
.mz-feat {
    background: var(--bg); padding: 44px 36px;
    position: relative; overflow: hidden;
    transition: background 0.3s ease;
}
.mz-feat:hover { background: var(--surface); }
.mz-feat-accent {
    position: absolute; top: 0; left: 0; width: 2px; height: 0;
    background: var(--pulse); transition: height 0.4s ease;
}
.mz-feat:hover .mz-feat-accent { height: 100%; }
.mz-feat-num {
    font-family: var(--mono); font-size: 9px; letter-spacing: 3px;
    color: var(--muted); text-transform: uppercase; margin-bottom: 32px;
    display: flex; align-items: center; gap: 10px;
}
.mz-feat-num::after { content: ''; flex: 1; height: 1px; background: var(--border); }
.mz-feat-title {
    font-family: var(--sans); font-size: 20px; font-weight: 700;
    letter-spacing: -0.5px; color: var(--text); margin-bottom: 14px; line-height: 1.2;
}
.mz-feat-desc { font-size: 13px; font-weight: 300; line-height: 1.85; color: var(--muted); }
.mz-feat-glyph {
    position: absolute; bottom: 20px; right: 24px;
    font-family: var(--mono); font-size: 44px; font-weight: 700;
    color: rgba(255,255,255,0.025); line-height: 1; user-select: none;
}

/* CTA */
.mz-cta-wrap {
    width: 100%; max-width: 1200px;
    display: grid; grid-template-columns: 1fr auto;
    align-items: center; gap: 60px;
    border: 1px solid var(--border); border-radius: 3px;
    padding: 52px 56px; background: var(--surface);
    position: relative; overflow: hidden;
    animation: fadeUp 1s ease 0.6s both;
}
.mz-cta-wrap::before {
    content: '';
    position: absolute; inset: 0;
    background: radial-gradient(ellipse 55% 80% at 100% 50%, rgba(74,240,196,0.04), transparent);
    pointer-events: none;
}
.mz-cta-label {
    font-family: var(--mono); font-size: 9px; letter-spacing: 3px;
    text-transform: uppercase; color: var(--pulse); margin-bottom: 14px;
}
.mz-cta-title {
    font-family: var(--sans); font-size: 34px; font-weight: 900;
    letter-spacing: -1.5px; color: var(--text); line-height: 1.1; margin-bottom: 12px;
}
.mz-cta-sub { font-size: 13px; font-weight: 300; color: var(--muted); }

/* BUTTON */
div[data-testid="stButton"] > button {
    background: var(--text) !important; color: var(--bg) !important;
    font-family: var(--sans) !important; font-weight: 700 !important;
    font-size: 12px !important; letter-spacing: 2.5px !important;
    text-transform: uppercase !important;
    border: none !important; border-radius: 2px !important;
    padding: 18px 44px !important;
    transition: all 0.25s ease !important; white-space: nowrap !important;
}
div[data-testid="stButton"] > button:hover {
    background: var(--pulse) !important; color: var(--bg) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(74,240,196,0.28) !important;
}

/* FOOTER */
.mz-foot {
    width: 100%; max-width: 1200px;
    margin-top: 60px; padding-top: 26px;
    border-top: 1px solid var(--border);
    display: flex; justify-content: space-between; align-items: center;
    animation: fadeUp 1s ease 0.75s both;
}
.mz-foot-l { font-family: var(--mono); font-size: 9px; letter-spacing: 2px; text-transform: uppercase; color: var(--muted); }
.mz-foot-r { font-family: var(--mono); font-size: 9px; letter-spacing: 1px; color: rgba(240,244,248,0.14); text-align: right; max-width: 380px; }

@keyframes fadeUp   { from { opacity:0; transform:translateY(28px); } to { opacity:1; transform:translateY(0); } }
@keyframes fadeDown { from { opacity:0; transform:translateY(-18px); } to { opacity:1; transform:translateY(0); } }

hr { display:none !important; }
[data-testid="stCaptionContainer"] { display:none !important; }

@media (max-width: 900px) {
    .mz-hero { grid-template-columns: 1fr; }
    .mz-vitals { display: none; }
    .mz-stats { grid-template-columns: repeat(2,1fr); }
    .mz-features { grid-template-columns: 1fr; }
    .mz-cta-wrap { grid-template-columns: 1fr; text-align: center; padding: 40px 28px; }
    .mz-foot { flex-direction: column; gap: 12px; text-align: center; }
    .mz-foot-r { text-align: center; }
}
</style>

<div class="ecg-bg">
  <div class="ecg-line">
    <svg viewBox="0 0 1200 80" preserveAspectRatio="none" fill="none">
      <polyline stroke="white" stroke-width="1.5"
        points="0,40 100,40 120,40 138,8 148,72 158,18 168,62 180,40 280,40
                300,40 318,8 328,72 338,18 348,62 360,40 460,40
                480,40 498,8 508,72 518,18 528,62 540,40 640,40
                660,40 678,8 688,72 698,18 708,62 720,40 820,40
                840,40 858,8 868,72 878,18 888,62 900,40 1000,40
                1020,40 1038,8 1048,72 1058,18 1068,62 1080,40 1200,40"/>
    </svg>
  </div>
</div>

<div class="mz-page">

  <nav class="mz-nav">
    <div class="mz-wordmark">Med<span>Zentic</span></div>
    <div class="mz-nav-meta">AI Health Platform / v2.0</div>
    <div class="mz-status-dot">Systems Nominal</div>
  </nav>

  <section class="mz-hero">
    <div>
      <div class="mz-tag">Clinical Intelligence System</div>
      <h1 class="mz-h1">Know Your<br><em>Risk.</em><br>Own Your<br>Health.</h1>
      <p class="mz-hero-desc">Upload a medical report. Our AI reads clinical values, models disease probability, and delivers a clear picture of your health in seconds.</p>
    </div>
    <div class="mz-vitals">
      <div class="mz-vitals-title">// Live System Status</div>
      <div class="mz-vital-row">
        <div><div class="mz-vital-label">AI Model</div><div class="mz-vital-value ok">ONLINE</div></div>
        <div style="text-align:right"><div class="mz-vital-bar"><div class="mz-vital-fill" style="width:98%"></div></div><div class="mz-vital-label" style="margin-top:5px">98% Uptime</div></div>
      </div>
      <div class="mz-vital-row">
        <div><div class="mz-vital-label">Analysis Speed</div><div class="mz-vital-value">&#60;2s</div></div>
        <div style="text-align:right"><div class="mz-vital-bar"><div class="mz-vital-fill" style="width:94%;animation-delay:0.3s"></div></div><div class="mz-vital-label" style="margin-top:5px">Sub-second</div></div>
      </div>
      <div class="mz-vital-row">
        <div><div class="mz-vital-label">Risk Markers</div><div class="mz-vital-value">12+</div></div>
        <div style="text-align:right"><div class="mz-vital-bar"><div class="mz-vital-fill" style="width:83%;animation-delay:0.6s"></div></div><div class="mz-vital-label" style="margin-top:5px">Conditions</div></div>
      </div>
      <div class="mz-vital-row">
        <div><div class="mz-vital-label">Accuracy</div><div class="mz-vital-value ok">98.4%</div></div>
        <div style="text-align:right"><div class="mz-vital-bar"><div class="mz-vital-fill" style="width:98%;animation-delay:0.9s"></div></div><div class="mz-vital-label" style="margin-top:5px">Validated</div></div>
      </div>
    </div>
  </section>

  <div class="mz-stats">
    <div class="mz-stat" data-idx="01"><div class="mz-stat-n">98<span>%</span></div><div class="mz-stat-l">Model Accuracy</div></div>
    <div class="mz-stat" data-idx="02"><div class="mz-stat-n">12<span>+</span></div><div class="mz-stat-l">Risk Markers</div></div>
    <div class="mz-stat" data-idx="03"><div class="mz-stat-n">2<span>s</span></div><div class="mz-stat-l">Analysis Time</div></div>
    <div class="mz-stat" data-idx="04"><div class="mz-stat-n">3<span>x</span></div><div class="mz-stat-l">Disease Models</div></div>
  </div>

  <div class="mz-features">
    <div class="mz-feat"><div class="mz-feat-accent"></div><div class="mz-feat-num">Function 01</div><div class="mz-feat-title">Smart Risk Detection</div><div class="mz-feat-desc">Advanced ML models analyze clinical values and estimate health risk levels across multiple conditions simultaneously.</div><div class="mz-feat-glyph">Rx</div></div>
    <div class="mz-feat"><div class="mz-feat-accent"></div><div class="mz-feat-num">Function 02</div><div class="mz-feat-title">Clear Health Insights</div><div class="mz-feat-desc">Complex medical numbers translated into plain language. Understand what your results mean without a medical background.</div><div class="mz-feat-glyph">Dx</div></div>
    <div class="mz-feat"><div class="mz-feat-accent"></div><div class="mz-feat-num">Function 03</div><div class="mz-feat-title">AI Medical Assistant</div><div class="mz-feat-desc">Discuss your results with an intelligent AI assistant. Ask questions, understand implications, get personalized context.</div><div class="mz-feat-glyph">Ai</div></div>
  </div>

  <div class="mz-cta-wrap">
    <div>
      <div class="mz-cta-label">// Begin Analysis</div>
      <div class="mz-cta-title">Start Your Health<br>Analysis Now</div>
      <div class="mz-cta-sub">Upload your medical report. Results in under two seconds.</div>
    </div>
""", unsafe_allow_html=True)

if st.button("Open Health Dashboard"):
    st.switch_page("pages/1_Dashboard.py")

st.markdown("""
  </div>

  <footer class="mz-foot">
    <div class="mz-foot-l">MedZentic AI / 2025 / All Rights Reserved</div>
    <div class="mz-foot-r">For educational and risk assessment purposes only. Not a substitute for professional medical diagnosis or advice.</div>
  </footer>

</div>
""", unsafe_allow_html=True)