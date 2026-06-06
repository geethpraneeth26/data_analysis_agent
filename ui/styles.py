"""
Custom CSS styles for the Streamlit dashboard.
"""

CUSTOM_CSS = """
<style>
/* ── Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── Background ── */
.stApp {
    background: linear-gradient(135deg, #0f0c29 0%, #1a1040 40%, #0d1117 100%);
    min-height: 100vh;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(16px);
    border-right: 1px solid rgba(167,139,250,0.15);
}
section[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}

/* ── Metric cards ── */
[data-testid="metric-container"] {
    background: rgba(124,58,237,0.12);
    border: 1px solid rgba(124,58,237,0.3);
    border-radius: 14px;
    padding: 16px 20px;
    backdrop-filter: blur(12px);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
[data-testid="metric-container"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(124,58,237,0.25);
}
[data-testid="metric-container"] label {
    color: #a78bfa !important;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-size: 1.8rem;
    font-weight: 700;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.04);
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
    border: 1px solid rgba(167,139,250,0.1);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    color: #94a3b8;
    font-weight: 500;
    padding: 8px 20px;
    transition: all 0.2s;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
    color: #ffffff !important;
    box-shadow: 0 4px 12px rgba(124,58,237,0.4);
}

/* ── Cards / containers ── */
.insight-card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(167,139,250,0.25);
    border-radius: 14px;
    padding: 18px 22px;
    margin-bottom: 12px;
    backdrop-filter: blur(10px);
    transition: transform 0.2s, border-color 0.2s, box-shadow 0.2s;
    line-height: 1.8;
    color: #e2e8f0 !important;
    font-size: 0.96rem;
    font-weight: 500;
}
.insight-card:hover {
    transform: translateX(4px);
    border-color: rgba(167,139,250,0.5);
    box-shadow: 0 4px 20px rgba(124,58,237,0.15);
}
.insight-card strong, .insight-card b {
    color: #c4b5fd;
    font-weight: 700;
}
.insight-card em {
    color: #94a3b8;
}
/* Numbered insight badge */
.insight-number {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 24px;
    height: 24px;
    background: linear-gradient(135deg, #7c3aed, #4f46e5);
    color: #ffffff;
    border-radius: 50%;
    font-size: 0.7rem;
    font-weight: 700;
    margin-right: 10px;
    flex-shrink: 0;
    vertical-align: middle;
}

/* ── Section headers ── */
.section-header {
    font-size: 1.3rem;
    font-weight: 700;
    color: #a78bfa;
    padding-bottom: 6px;
    border-bottom: 2px solid rgba(124,58,237,0.3);
    margin-bottom: 18px;
    letter-spacing: -0.01em;
}

/* ── Hero banner ── */
.hero-banner {
    background: linear-gradient(135deg, #7c3aed22 0%, #4f46e522 100%);
    border: 1px solid rgba(124,58,237,0.3);
    border-radius: 20px;
    padding: 32px 36px;
    margin-bottom: 28px;
    text-align: center;
}
.hero-banner h1 {
    font-size: 2.4rem;
    font-weight: 800;
    background: linear-gradient(135deg, #a78bfa, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 8px;
}
.hero-banner p {
    color: #94a3b8;
    font-size: 1.05rem;
    margin: 0;
}

/* ── Step badge (agent pipeline) ── */
.step-badge {
    display: inline-block;
    background: rgba(124,58,237,0.2);
    border: 1px solid rgba(124,58,237,0.4);
    border-radius: 8px;
    padding: 4px 12px;
    font-size: 0.78rem;
    font-weight: 600;
    color: #a78bfa;
    margin: 2px;
}

/* ── DataFrames ── */
.stDataFrame {
    border: 1px solid rgba(167,139,250,0.15) !important;
    border-radius: 12px !important;
    overflow: hidden;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #4f46e5);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px 24px;
    font-weight: 600;
    font-family: 'Inter', sans-serif;
    transition: all 0.2s;
    box-shadow: 0 4px 12px rgba(124,58,237,0.3);
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(124,58,237,0.5);
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    border: 2px dashed rgba(124,58,237,0.4) !important;
    border-radius: 14px !important;
    background: rgba(124,58,237,0.05) !important;
    padding: 20px !important;
    transition: border-color 0.2s;
}
[data-testid="stFileUploader"]:hover {
    border-color: rgba(124,58,237,0.7) !important;
}

/* ── Selectbox / multiselect ── */
[data-testid="stSelectbox"], [data-testid="stMultiselect"] {
    background: rgba(255,255,255,0.05) !important;
    border-radius: 10px !important;
}

/* ── Spinner ── */
.stSpinner > div {
    border-top-color: #7c3aed !important;
}

/* ── Text area / text input (Optional Query) ── */
section[data-testid="stSidebar"] textarea {
    background: rgba(255,255,255,0.93) !important;
    color: #1e1b4b !important;
    border: 1.5px solid rgba(124,58,237,0.45) !important;
    border-radius: 10px !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    padding: 10px 12px !important;
    caret-color: #7c3aed;
    transition: border-color 0.2s, box-shadow 0.2s;
}
section[data-testid="stSidebar"] textarea:focus {
    border-color: #7c3aed !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.25) !important;
    outline: none !important;
}
section[data-testid="stSidebar"] textarea::placeholder {
    color: #7c6aaa !important;
    font-style: italic;
    font-weight: 400 !important;
}

/* ── Progress step (pipeline loading) ── */
.progress-panel {
    background: rgba(124,58,237,0.08);
    border: 1px solid rgba(124,58,237,0.25);
    border-radius: 14px;
    padding: 20px 24px;
    margin: 16px 0;
}
.progress-step {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 8px 0;
    color: #cbd5e1;
    font-size: 0.9rem;
    font-weight: 500;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    animation: fadeIn 0.3s ease;
}
.progress-step:last-child {
    border-bottom: none;
}
.progress-step .step-icon {
    font-size: 1.1rem;
    width: 28px;
    text-align: center;
    flex-shrink: 0;
}
.progress-step.done {
    color: #86efac;
}
.progress-step.done .step-icon::after {
    content: ' ✓';
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateX(-8px); }
    to   { opacity: 1; transform: translateX(0); }
}

/* ── Query card (blue accent) ── */
.query-card {
    background: rgba(96,165,250,0.08);
    border: 1px solid rgba(96,165,250,0.3);
    border-radius: 14px;
    padding: 16px 20px;
    margin-bottom: 16px;
    color: #bfdbfe;
    font-size: 0.94rem;
    font-weight: 500;
    line-height: 1.7;
}

/* ── Cleaning report ── */
.clean-item {
    display: flex;
    align-items: flex-start;
    gap: 8px;
    padding: 10px 0;
    border-bottom: 1px solid rgba(167,139,250,0.1);
    color: #e2e8f0;
    font-size: 0.9rem;
    font-weight: 500;
}

/* ── Agent log ── */
.log-entry {
    font-size: 0.82rem;
    color: #94a3b8;
    padding: 4px 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
}

/* ── Success / Error alerts ── */
.stSuccess {
    background: rgba(16,185,129,0.1) !important;
    border: 1px solid rgba(16,185,129,0.3) !important;
    border-radius: 10px !important;
}
.stError {
    background: rgba(239,68,68,0.1) !important;
    border: 1px solid rgba(239,68,68,0.3) !important;
    border-radius: 10px !important;
}
</style>
"""
