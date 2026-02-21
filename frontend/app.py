import streamlit as st

st.set_page_config(
    page_title="MedZentic",
    page_icon="🫀",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400;1,600&family=DM+Sans:wght@300;400;500&family=DM+Mono:wght@300;400&display=swap');

:root {
  --cream:   #F7F3EE;
  --warm:    #EDE8E0;
  --sage:    #7B9E87;
  --sage-lt: #C8DCCF;
  --clay:    #C4856A;
  --clay-lt: #F0D9CE;
  --ink:     #1C1917;
  --ink2:    #44403C;
  --dust:    #A8A29E;
  --white:   #FEFCFA;
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

[data-testid="stAppViewContainer"] > .main > div {
  padding: 0 !important;
  max-width: 100% !important;
}

/* ── WRAPPER ── */
.mz {
  min-height: 100vh;
  background: var(--cream);
  position: relative;
  overflow: hidden;
}

/* Organic BG shapes */
.mz-blob1 {
  position: fixed;
  top: -180px; right: -120px;
  width: 600px; height: 600px;
  border-radius: 50%;
  background: radial-gradient(circle at 40% 40%, rgba(123,158,135,0.15), transparent 65%);
  pointer-events: none;
}
.mz-blob2 {
  position: fixed;
  bottom: -200px; left: -150px;
  width: 700px; height: 700px;
  border-radius: 50%;
  background: radial-gradient(circle at 60% 60%, rgba(196,133,106,0.12), transparent 65%);
  pointer-events: none;
}
.mz-noise {
  position: fixed; inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E");
  pointer-events: none;
  opacity: 0.4;
}

/* ── NAV ── */
.nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 28px 60px;
  position: relative;
  animation: fadeDown 0.6s ease both;
}
.nav-logo {
  display: flex; align-items: center; gap: 10px;
}
.nav-mark {
  width: 36px; height: 36px;
  background: var(--sage);
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 16px;
}
.nav-name {
  font-family: 'Playfair Display', serif;
  font-size: 20px; font-weight: 700;
  color: var(--ink); letter-spacing: -0.3px;
}
.nav-name em { font-style: normal; color: var(--sage); }
.nav-pill {
  background: var(--white);
  border: 1px solid var(--warm);
  border-radius: 100px;
  padding: 8px 20px;
  font-family: 'DM Mono', monospace;
  font-size: 10px; letter-spacing: 1.5px;
  color: var(--dust);
  text-transform: uppercase;
}
.nav-badge {
  display: flex; align-items: center; gap: 8px;
  font-size: 12px; font-weight: 500; color: var(--sage);
}
.nav-dot {
  width: 7px; height: 7px;
  background: var(--sage); border-radius: 50%;
  animation: breathe 3s ease-in-out infinite;
}
@keyframes breathe {
  0%,100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.4; transform: scale(0.8); }
}

/* ── HERO ── */
.hero {
  display: grid;
  grid-template-columns: 1fr 420px;
  gap: 0;
  min-height: calc(100vh - 92px);
  padding: 0 60px 0 60px;
  align-items: center;
  animation: fadeUp 0.8s ease 0.1s both;
}
.hero-left { padding-right: 80px; }
.hero-label {
  display: inline-flex; align-items: center; gap: 10px;
  font-family: 'DM Mono', monospace;
  font-size: 10px; letter-spacing: 2px; color: var(--clay);
  text-transform: uppercase; margin-bottom: 32px;
}
.hero-label::before {
  content: '';
  width: 28px; height: 1px;
  background: var(--clay);
}
.hero-h1 {
  font-family: 'Playfair Display', serif;
  font-size: clamp(52px, 5.5vw, 82px);
  font-weight: 700; line-height: 1.05;
  letter-spacing: -2px; color: var(--ink);
  margin-bottom: 28px;
}
.hero-h1 em {
  font-style: italic; color: var(--sage);
}
.hero-desc {
  font-size: 16px; font-weight: 300; line-height: 1.8;
  color: var(--ink2); max-width: 420px;
  margin-bottom: 52px;
}
.hero-stats {
  display: flex; gap: 48px;
  padding-top: 36px;
  border-top: 1px solid var(--warm);
}
.stat-num {
  font-family: 'Playfair Display', serif;
  font-size: 36px; font-weight: 700;
  color: var(--ink); letter-spacing: -1px; line-height: 1;
}
.stat-num sup {
  font-size: 16px; color: var(--sage); vertical-align: top; margin-top: 6px; display: inline-block;
}
.stat-lbl {
  font-size: 12px; font-weight: 400; color: var(--dust);
  margin-top: 4px; letter-spacing: 0.3px;
}

/* ── CARD PANEL ── */
.panel {
  background: var(--white);
  border-radius: 28px;
  border: 1px solid rgba(196,133,106,0.18);
  padding: 40px 36px;
  box-shadow: 0 20px 60px rgba(28,25,23,0.08), 0 4px 16px rgba(28,25,23,0.04);
  position: relative; overflow: hidden;
}
.panel::before {
  content: '';
  position: absolute; top: 0; left: 0; right: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--sage) 0%, var(--clay) 100%);
}
.panel-eyebrow {
  font-family: 'DM Mono', monospace;
  font-size: 9px; letter-spacing: 2.5px;
  text-transform: uppercase; color: var(--dust);
  margin-bottom: 24px;
}
.panel-title {
  font-family: 'Playfair Display', serif;
  font-size: 22px; font-weight: 700;
  color: var(--ink); margin-bottom: 6px; letter-spacing: -0.3px;
}
.panel-sub {
  font-size: 13px; font-weight: 300; color: var(--dust);
  line-height: 1.6; margin-bottom: 28px;
}
.metric-row {
  display: flex; flex-direction: column; gap: 14px;
  margin-bottom: 32px;
}
.metric-item {
  display: flex; align-items: center; justify-content: space-between;
  padding: 14px 16px;
  background: var(--cream);
  border-radius: 12px;
}
.metric-name {
  font-family: 'DM Mono', monospace;
  font-size: 10px; letter-spacing: 1px; color: var(--dust); text-transform: uppercase;
}
.metric-val {
  font-family: 'Playfair Display', serif;
  font-size: 18px; font-weight: 700; color: var(--ink);
}
.metric-val.good { color: var(--sage); }
.metric-bar-wrap { height: 3px; background: var(--warm); border-radius: 2px; margin-top: 6px; overflow: hidden; }
.metric-bar { height: 100%; background: var(--sage); border-radius: 2px; animation: barIn 1.5s ease both; }
@keyframes barIn { from { width: 0; } }

/* ── FEATURES ── */
.features {
  padding: 80px 60px;
  animation: fadeUp 0.8s ease 0.2s both;
}
.features-label {
  font-family: 'DM Mono', monospace;
  font-size: 10px; letter-spacing: 2px;
  text-transform: uppercase; color: var(--clay);
  margin-bottom: 52px; display: flex; align-items: center; gap: 14px;
}
.features-label::after {
  content: ''; flex: 1; height: 1px; background: var(--warm);
}
.feat-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2px;
  background: var(--warm);
  border-radius: 20px;
  overflow: hidden;
}
.feat-item {
  background: var(--white);
  padding: 44px 36px;
  position: relative;
  transition: background 0.25s;
}
.feat-item:hover { background: var(--cream); }
.feat-num {
  font-family: 'Playfair Display', serif;
  font-size: 11px; font-style: italic; color: var(--clay);
  margin-bottom: 20px; display: block;
}
.feat-name {
  font-family: 'Playfair Display', serif;
  font-size: 20px; font-weight: 700;
  color: var(--ink); margin-bottom: 12px; letter-spacing: -0.3px;
}
.feat-desc {
  font-size: 13px; font-weight: 300; line-height: 1.8; color: var(--ink2);
}
.feat-glyph {
  position: absolute; bottom: 28px; right: 32px;
  font-family: 'Playfair Display', serif;
  font-size: 52px; font-style: italic; font-weight: 700;
  color: rgba(28,25,23,0.04); line-height: 1; user-select: none;
}

/* ── CTA ── */
.cta-section {
  padding: 0 60px 80px;
  animation: fadeUp 0.8s ease 0.3s both;
}
.cta-inner {
  background: var(--ink);
  border-radius: 24px;
  padding: 64px;
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 60px; align-items: center;
  position: relative; overflow: hidden;
}
.cta-inner::before {
  content: '';
  position: absolute; top: -80px; right: -80px;
  width: 350px; height: 350px; border-radius: 50%;
  background: radial-gradient(circle, rgba(123,158,135,0.2), transparent 65%);
}
.cta-inner::after {
  content: '';
  position: absolute; bottom: -60px; left: 30%;
  width: 250px; height: 250px; border-radius: 50%;
  background: radial-gradient(circle, rgba(196,133,106,0.15), transparent 65%);
}
.cta-text { position: relative; z-index: 1; }
.cta-eyebrow {
  font-family: 'DM Mono', monospace;
  font-size: 10px; letter-spacing: 2px;
  text-transform: uppercase; color: var(--sage);
  margin-bottom: 16px;
}
.cta-title {
  font-family: 'Playfair Display', serif;
  font-size: 38px; font-weight: 700;
  color: var(--white); letter-spacing: -1px; line-height: 1.1; margin-bottom: 10px;
}
.cta-sub { font-size: 14px; font-weight: 300; color: rgba(255,255,255,0.5); }
.cta-btn-wrap { position: relative; z-index: 1; }

/* ── BUTTON ── */
div[data-testid="stButton"] > button {
  background: var(--sage) !important;
  color: white !important;
  font-family: 'DM Sans', sans-serif !important;
  font-weight: 500 !important;
  font-size: 14px !important;
  letter-spacing: 0.2px !important;
  border: none !important;
  border-radius: 100px !important;
  padding: 16px 40px !important;
  transition: all 0.25s ease !important;
  white-space: nowrap !important;
  box-shadow: 0 4px 20px rgba(123,158,135,0.4) !important;
}
div[data-testid="stButton"] > button:hover {
  background: #6a8f76 !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 28px rgba(123,158,135,0.5) !important;
}

/* ── FOOTER ── */
.mz-foot {
  padding: 24px 60px;
  border-top: 1px solid var(--warm);
  display: flex; justify-content: space-between; align-items: center;
  animation: fadeUp 0.8s ease 0.4s both;
}
.foot-l {
  font-family: 'DM Mono', monospace;
  font-size: 10px; letter-spacing: 1px;
  text-transform: uppercase; color: var(--dust);
}
.foot-r {
  font-size: 12px; color: var(--dust);
  max-width: 380px; text-align: right; line-height: 1.5;
}

@keyframes fadeUp { from { opacity: 0; transform: translateY(24px); } to { opacity: 1; transform: translateY(0); } }
@keyframes fadeDown { from { opacity: 0; transform: translateY(-16px); } to { opacity: 1; transform: translateY(0); } }

hr { display: none !important; }
</style>

<div class="mz">
<div class="mz-blob1"></div>
<div class="mz-blob2"></div>
<div class="mz-noise"></div>

<nav class="nav">
  <div class="nav-logo">
    <div class="nav-mark">🫀</div>
    <div class="nav-name">Med<em>Zentic</em></div>
  </div>
  <div class="nav-pill">Clinical AI · v2.0</div>
  <div class="nav-badge"><div class="nav-dot"></div>Systems Ready</div>
</nav>

<section class="hero">
  <div class="hero-left">
    <div class="hero-label">Clinical Intelligence</div>
    <h1 class="hero-h1">Know your<br>health with<br><em>clarity.</em></h1>
    <p class="hero-desc">Upload a medical report and receive an AI-powered risk assessment across diabetes, cardiac health, and neurological markers — in seconds.</p>
    <div class="hero-stats">
      <div><div class="stat-num">98<sup>%</sup></div><div class="stat-lbl">Model Accuracy</div></div>
      <div><div class="stat-num">~5<sup>s</sup></div><div class="stat-lbl">Analysis Time</div></div>
      <div><div class="stat-num">3<sup>×</sup></div><div class="stat-lbl">Disease Models</div></div>
    </div>
  </div>
  <div class="panel">
    <div class="panel-eyebrow">// System Status</div>
    <div class="panel-title">Live Intelligence</div>
    <div class="panel-sub">Clinical models standing by, ready for your report.</div>
    <div class="metric-row">
      <div class="metric-item">
        <div>
          <div class="metric-name">AI Model</div>
          <div class="metric-bar-wrap"><div class="metric-bar" style="width:98%"></div></div>
        </div>
        <div class="metric-val good">Online</div>
      </div>
      <div class="metric-item">
        <div>
          <div class="metric-name">Analysis Speed</div>
          <div class="metric-bar-wrap"><div class="metric-bar" style="width:92%;animation-delay:0.3s"></div></div>
        </div>
        <div class="metric-val">&#60; 5s</div>
      </div>
      <div class="metric-item">
        <div>
          <div class="metric-name">Risk Markers</div>
          <div class="metric-bar-wrap"><div class="metric-bar" style="width:80%;animation-delay:0.6s"></div></div>
        </div>
        <div class="metric-val">12+</div>
      </div>
      <div class="metric-item">
        <div>
          <div class="metric-name">Accuracy</div>
          <div class="metric-bar-wrap"><div class="metric-bar" style="width:98%;animation-delay:0.9s"></div></div>
        </div>
        <div class="metric-val good">98.4%</div>
      </div>
    </div>
  </div>
</section>

<section class="features">
  <div class="features-label">Capabilities</div>
  <div class="feat-grid">
    <div class="feat-item">
      <span class="feat-num">one</span>
      <div class="feat-name">Smart Risk Detection</div>
      <div class="feat-desc">ML models analyze clinical values and estimate health risk across multiple conditions simultaneously.</div>
      <div class="feat-glyph">Rx</div>
    </div>
    <div class="feat-item">
      <span class="feat-num">two</span>
      <div class="feat-name">Clear Health Insights</div>
      <div class="feat-desc">Complex medical numbers translated into plain language — no background required to understand your results.</div>
      <div class="feat-glyph">Dx</div>
    </div>
    <div class="feat-item">
      <span class="feat-num">three</span>
      <div class="feat-name">AI Medical Assistant</div>
      <div class="feat-desc">Discuss your results with a clinical AI assistant. Ask questions, understand implications, get context.</div>
      <div class="feat-glyph">Ai</div>
    </div>
  </div>
</section>

<section class="cta-section">
  <div class="cta-inner">
    <div class="cta-text">
      <div class="cta-eyebrow">Begin Analysis</div>
      <div class="cta-title">Start your health<br>assessment today.</div>
      <div class="cta-sub">Upload a report. Get results in under five seconds.</div>
    </div>
    <div class="cta-btn-wrap">
""", unsafe_allow_html=True)

if st.button("Open Health Dashboard →"):
    st.switch_page("pages/1_Dashboard.py")

st.markdown("""
    </div>
  </div>
</section>

<footer class="mz-foot">
  <div class="foot-l">MedZentic AI · 2025 · All Rights Reserved</div>
  <div class="foot-r">For educational and risk assessment purposes only. Not a substitute for professional medical diagnosis or advice.</div>
</footer>

</div>
""", unsafe_allow_html=True)