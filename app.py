"""
AI Multi-Agent Data Analysis System
Main Streamlit Application
"""
import streamlit as st
import pandas as pd
import numpy as np
# ── agents setup ────────────────────────────────────────────────────────────
from agents.manager_agent import DataMindManager
from agents.visualization_agent import CHART_TYPES
from ui.styles import CUSTOM_CSS
from utils.helpers import df_to_csv_bytes, format_number

# ── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DataMind AI · Multi-Agent Analysis",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ── Session state init ───────────────────────────────────────────────────────
if "pipeline_state" not in st.session_state:
    st.session_state.pipeline_state = None

# Initialize manager directly
manager = DataMindManager()


# ════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 10px 0 24px;'>
      <div style='font-size:2.4rem;'>🧠</div>
      <div style='font-size:1.15rem; font-weight:700; color:#a78bfa;'>DataMind AI</div>
      <div style='font-size:0.75rem; color:#94a3b8; margin-top:2px;'>Multi-Agent Analysis System</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📂 Upload Dataset")
    uploaded_file = st.file_uploader(
        "Drag & drop or browse",
        type=["csv", "xlsx", "xls", "json", "pdf", "docx", "txt"],
        label_visibility="collapsed",
    )

    st.markdown("### 🎛️ Output Options")
    output_options = st.multiselect(
        "Select outputs to display",
        ["Dataset Overview", "AI Insights", "Statistics", "Visualizations", "Trend Analysis", "Raw Data"],
        default=["Dataset Overview", "AI Insights", "Visualizations"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    run_btn = st.button("🚀 Run Analysis", use_container_width=True)

    # Pipeline status
    if st.session_state.pipeline_state:
        state = st.session_state.pipeline_state
        st.markdown("---")
        st.markdown("### 🔄 Agent Pipeline")
        for log in state.get("agent_log", []):
            st.markdown(
                f"<div class='log-entry'>{log}</div>",
                unsafe_allow_html=True,
            )


# ════════════════════════════════════════════════════════════════════════════
# HERO BANNER
# ════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class='hero-banner'>
  <h1>🧠 DataMind AI</h1>
  <p>Upload any dataset · 8 Specialized Agents · Instant Insights & Interactive Charts</p>
</div>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# RUN PIPELINE
# ════════════════════════════════════════════════════════════════════════════

# Map agent names → human-readable step labels
_AGENT_LABELS = {
    "FileDetectionAgent":  ("🔍", "Detecting file type"),
    "ExtractionAgent":     ("📄", "Extracting data from document"),
    "LoadingAgent":        ("📥", "Loading dataset into memory"),
    "UnderstandingAgent":  ("🧐", "Analysing dataset structure"),
    "CleaningAgent":       ("🧹", "Cleaning & standardising data"),
    "AnalysisAgent":       ("📊", "Running statistical analysis"),
    "InsightAgent":        ("💡", "Generating AI insights"),
    "VisualizationAgent":  ("🎨", "Building visualizations"),
}

if run_btn:
    if uploaded_file is None:
        st.error("⚠️ Please upload a file first using the sidebar.")
    else:
        # manager is already initialized at top level
        state_result = {}

        with st.status("🤖 Agent Pipeline Running…", expanded=True) as status:
            completed_steps = []

            def _on_step(agent_name: str):
                icon, label = _AGENT_LABELS.get(agent_name, ("⚙️", agent_name))
                # Mark previous steps done
                steps_html = "".join(
                    f"<div class='progress-step done'>"
                    f"<span class='step-icon'>{e}</span>{l} &nbsp;<strong style='color:#86efac;'>✓</strong></div>"
                    for e, l in completed_steps
                )
                steps_html += (
                    f"<div class='progress-step'>"
                    f"<span class='step-icon'>{icon}</span>"
                    f"<span style='color:#a78bfa;font-weight:600;'>{label}…</span></div>"
                )
                st.markdown(
                    f"<div class='progress-panel'>{steps_html}</div>",
                    unsafe_allow_html=True,
                )
                completed_steps.append((icon, label))

            result = manager.execute_pipeline(uploaded_file, on_step=_on_step)

            if result.get("error"):
                status.update(
                    label=f"❌ Pipeline failed: {result['error']}",
                    state="error",
                    expanded=True,
                )
                st.error(f"❌ {result['error']}")
            else:
                # Show all steps complete
                done_html = "".join(
                    f"<div class='progress-step done'>"
                    f"<span class='step-icon'>{e}</span>{l} &nbsp;<strong style='color:#86efac;'>✓</strong></div>"
                    for e, l in completed_steps
                )
                st.markdown(
                    f"<div class='progress-panel'>{done_html}</div>",
                    unsafe_allow_html=True,
                )
                status.update(
                    label="✅ Analysis complete! Scroll down to explore results.",
                    state="complete",
                    expanded=False,
                )
                st.session_state.pipeline_state = result
                st.rerun()


# ════════════════════════════════════════════════════════════════════════════
# RESULTS DASHBOARD
# ════════════════════════════════════════════════════════════════════════════
state = st.session_state.pipeline_state

if state and state.get("pipeline_complete"):
    df: pd.DataFrame = state.get("clean_df")
    raw_df: pd.DataFrame = state.get("raw_df")
    numeric_cols: list = state.get("numeric_cols", [])
    cat_cols: list = state.get("cat_cols", [])
    dt_cols: list = state.get("dt_cols", [])
    all_cols: list = df.columns.tolist() if df is not None else []

    # ── Top KPI strip ──────────────────────────────────────────────────────
    st.markdown("<div class='section-header'>📊 Dataset at a Glance</div>", unsafe_allow_html=True)
    k1, k2, k3, k4, k5 = st.columns(5)
    shape = state.get("shape", (0, 0))
    k1.metric("Rows", f"{shape[0]:,}")
    k2.metric("Columns", f"{shape[1]:,}")
    k3.metric("Numeric", len(numeric_cols))
    k4.metric("Categorical", len(cat_cols))
    k5.metric("File Type", state.get("file_type", "—").upper())

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Tabs ───────────────────────────────────────────────────────────────
    tab_labels = []
    if "Dataset Overview" in output_options:
        tab_labels.append("📋 Overview")
    if "AI Insights" in output_options:
        tab_labels.append("💡 Insights")
    if "Statistics" in output_options:
        tab_labels.append("📈 Statistics")
    if "Visualizations" in output_options:
        tab_labels.append("🎨 Visualizations")
    if "Trend Analysis" in output_options:
        tab_labels.append("📅 Trends")
    if "Raw Data" in output_options:
        tab_labels.append("🗃️ Raw Data")

    if not tab_labels:
        tab_labels = ["📋 Overview"]

    tabs = st.tabs(tab_labels)
    tab_index = 0

    # ── TAB: Overview ────────────────────────────────────────────────────
    if "📋 Overview" in tab_labels:
        with tabs[tab_index]:
            tab_index += 1

            col_l, col_r = st.columns([1, 1], gap="large")

            with col_l:
                st.markdown("<div class='section-header'>🔍 Dataset Summary</div>", unsafe_allow_html=True)
                summary = state.get("dataset_summary", "No summary available.")
                st.markdown(
                    f"<div class='insight-card'>{summary}</div>",
                    unsafe_allow_html=True,
                )

                # Cleaning report
                cleaning_report = state.get("cleaning_report", [])
                if cleaning_report:
                    st.markdown("<div class='section-header' style='margin-top:24px;'>🧹 Cleaning Report</div>", unsafe_allow_html=True)
                    for item in cleaning_report:
                        st.markdown(
                            f"<div class='clean-item'>{item}</div>",
                            unsafe_allow_html=True,
                        )

            with col_r:
                st.markdown("<div class='section-header'>👁️ Data Preview (first 50 rows)</div>", unsafe_allow_html=True)
                if df is not None:
                    st.dataframe(df.head(50), use_container_width=True, height=400)

            # Column type breakdown
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<div class='section-header'>🗂️ Column Classification</div>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown("**🔢 Numeric Columns**")
                for c in numeric_cols:
                    st.markdown(f"<span class='step-badge'>{c}</span>", unsafe_allow_html=True)
                if not numeric_cols:
                    st.caption("None detected")
            with c2:
                st.markdown("**🏷️ Categorical Columns**")
                for c in cat_cols:
                    st.markdown(f"<span class='step-badge'>{c}</span>", unsafe_allow_html=True)
                if not cat_cols:
                    st.caption("None detected")
            with c3:
                st.markdown("**📅 Date/Time Columns**")
                for c in dt_cols:
                    st.markdown(f"<span class='step-badge'>{c}</span>", unsafe_allow_html=True)
                if not dt_cols:
                    st.caption("None detected")

    # ── TAB: Insights ────────────────────────────────────────────────────
    if "💡 Insights" in tab_labels:
        with tabs[tab_index]:
            tab_index += 1
            insights: list = state.get("insights", [])
            st.markdown("<div class='section-header'>💡 AI-Generated Insights</div>", unsafe_allow_html=True)

            if insights:
                # Summary strip
                st.markdown(
                    f"<div style='color:#94a3b8;font-size:0.82rem;margin-bottom:14px;'>"
                    f"🧠 <strong style='color:#a78bfa;'>{len(insights)}</strong> insights generated from your dataset"
                    f"</div>",
                    unsafe_allow_html=True,
                )
                for i, insight in enumerate(insights, 1):
                    st.markdown(
                        f"<div class='insight-card'>"
                        f"<span class='insight-number'>{i}</span>"
                        f"{insight}"
                        f"</div>",
                        unsafe_allow_html=True,
                    )
            else:
                st.info("No insights generated. Ensure the dataset has numeric or categorical columns.")

    # ── TAB: Statistics ──────────────────────────────────────────────────
    if "📈 Statistics" in tab_labels:
        with tabs[tab_index]:
            tab_index += 1
            stats: dict = state.get("stats", {})
            correlations = state.get("correlations")
            category_counts: dict = state.get("category_counts", {})

            row1, row2 = st.columns([3, 2], gap="large")

            with row1:
                st.markdown("<div class='section-header'>📐 Descriptive Statistics</div>", unsafe_allow_html=True)
                if stats:
                    stats_df = pd.DataFrame(stats).T.reset_index()
                    stats_df = stats_df.rename(columns={"index": "Column"})
                    numeric_stat_cols = [c for c in stats_df.columns if c != "Column"]
                    for c in numeric_stat_cols:
                        stats_df[c] = stats_df[c].apply(lambda x: round(float(x), 2) if x == x else x)
                    st.dataframe(stats_df, use_container_width=True, height=300)
                else:
                    st.info("No numeric columns for statistical analysis.")

            with row2:
                st.markdown("<div class='section-header'>🏷️ Category Frequencies</div>", unsafe_allow_html=True)
                if category_counts:
                    selected_cat = st.selectbox(
                        "Select categorical column",
                        list(category_counts.keys()),
                        key="cat_sel",
                    )
                    if selected_cat:
                        cat_df = pd.DataFrame(
                            list(category_counts[selected_cat].items()),
                            columns=["Category", "Count"],
                        )
                        st.dataframe(cat_df, use_container_width=True, height=260)
                else:
                    st.info("No categorical columns detected.")

            # Correlation heatmap
            if correlations is not None and not correlations.empty:
                st.markdown("<div class='section-header' style='margin-top:24px;'>🔗 Correlation Matrix</div>", unsafe_allow_html=True)
                viz_agent = manager.visualization
                fig = viz_agent.make_heatmap(correlations)
                st.plotly_chart(fig, use_container_width=True, key="stats_corr_heatmap")

    # ── TAB: Visualizations ──────────────────────────────────────────────
    if "🎨 Visualizations" in tab_labels:
        with tabs[tab_index]:
            tab_index += 1

            # ── Auto-generated charts ──
            auto_charts = state.get("auto_charts", [])
            if auto_charts:
                st.markdown("<div class='section-header'>🤖 Auto-Generated Charts</div>", unsafe_allow_html=True)
                # Show 2 per row
                for i in range(0, len(auto_charts), 2):
                    cols = st.columns(2, gap="medium")
                    for j, col in enumerate(cols):
                        if i + j < len(auto_charts):
                            chart = auto_charts[i + j]
                            with col:
                                st.plotly_chart(chart["fig"], use_container_width=True, key=f"auto_chart_{i+j}")

            # ── Custom chart builder ──
            st.markdown("<div class='section-header' style='margin-top:32px;'>🛠️ Custom Chart Builder</div>", unsafe_allow_html=True)
            cb1, cb2, cb3, cb4 = st.columns([2, 2, 2, 1])

            with cb1:
                chart_type = st.selectbox("Chart Type", CHART_TYPES, key="custom_chart_type")
            with cb2:
                x_col = st.selectbox("X-Axis / Category", all_cols, key="custom_x")
            with cb3:
                y_options = ["(none)"] + numeric_cols
                y_col_raw = st.selectbox("Y-Axis / Value", y_options, key="custom_y")
                y_col = None if y_col_raw == "(none)" else y_col_raw
            with cb4:
                color_options = ["(none)"] + cat_cols
                color_raw = st.selectbox("Color By", color_options, key="custom_color")
                color_col = None if color_raw == "(none)" else color_raw

            if st.button("📊 Generate Chart", key="gen_chart_btn"):
                # manager is already initialized at top level
                fig = manager.make_custom_chart(state, chart_type, x_col, y_col, color_col)
                if fig:
                    st.plotly_chart(fig, use_container_width=True, key="custom_chart_render")
                else:
                    st.warning("Could not generate chart. Check column selections.")

    # ── TAB: Trends ──────────────────────────────────────────────────────
    if "📅 Trends" in tab_labels:
        with tabs[tab_index]:
            tab_index += 1
            trends: dict = state.get("trends", {})
            st.markdown("<div class='section-header'>📅 Trend Analysis</div>", unsafe_allow_html=True)

            if trends:
                viz_agent = manager.visualization
                for col, trend_df in trends.items():
                    if trend_df is not None and len(trend_df) >= 2:
                        dt_col = trend_df.columns[0]
                        st.markdown(f"**📈 {col.replace('_', ' ').title()} over Time**")
                        # Line and area side by side
                        tc1, tc2 = st.columns(2, gap="medium")
                        with tc1:
                            fig_line = viz_agent.make_line(
                                trend_df, dt_col, col,
                                title=f"{col.replace('_',' ').title()} — Line"
                            )
                            st.plotly_chart(fig_line, use_container_width=True, key=f"trend_line_{col}")
                        with tc2:
                            fig_area = viz_agent.make_area(
                                trend_df, dt_col, col,
                                title=f"{col.replace('_',' ').title()} — Area"
                            )
                            st.plotly_chart(fig_area, use_container_width=True, key=f"trend_area_{col}")
            else:
                st.info(
                    "No time-series columns detected. "
                    "To see trends, include a date/time column in your dataset."
                )

    # ── TAB: Raw Data ────────────────────────────────────────────────────
    if "🗃️ Raw Data" in tab_labels:
        with tabs[tab_index]:
            tab_index += 1
            st.markdown("<div class='section-header'>🗃️ Full Cleaned Dataset</div>", unsafe_allow_html=True)

            # Search/filter
            search_term = st.text_input(
                "🔎 Filter rows (searches all columns)",
                placeholder="Type to filter…",
                key="raw_search",
            )
            display_df = df.copy() if df is not None else pd.DataFrame()
            if search_term and not display_df.empty:
                mask = display_df.apply(
                    lambda col: col.astype(str).str.contains(search_term, case=False, na=False)
                ).any(axis=1)
                display_df = display_df[mask]

            st.dataframe(display_df, use_container_width=True, height=500)

            # Download button
            if df is not None:
                st.download_button(
                    label="⬇️ Download Cleaned CSV",
                    data=df_to_csv_bytes(df),
                    file_name=f"cleaned_{state.get('filename', 'dataset')}.csv",
                    mime="text/csv",
                    use_container_width=True,
                )

# ════════════════════════════════════════════════════════════════════════════
# EMPTY STATE (no file processed yet)
# ════════════════════════════════════════════════════════════════════════════
elif not state:
    col_a, col_b, col_c = st.columns(3, gap="large")

    cards = [
        ("📂", "Upload Any Format",
         "CSV, Excel, JSON, PDF, Word, or plain text — the system handles it all automatically."),
        ("🤖", "8 Specialized Agents",
         "Detection → Extraction → Loading → Understanding → Cleaning → Analysis → Insights → Visualization."),
        ("📊", "Interactive Charts",
         "Bar, Line, Pie, Scatter, Histogram, Area, Box, and Correlation Heatmap — fully custom."),
    ]
    for col, (icon, title, desc) in zip([col_a, col_b, col_c], cards):
        with col:
            st.markdown(
                f"""<div class='insight-card' style='text-align:center; padding:32px 20px;'>
                  <div style='font-size:2.5rem;'>{icon}</div>
                  <div style='font-size:1.05rem; font-weight:700; color:#a78bfa; margin:10px 0 6px;'>{title}</div>
                  <div style='color:#94a3b8; font-size:0.88rem; line-height:1.6;'>{desc}</div>
                </div>""",
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align:center; color:#64748b; font-size:0.85rem;'>
      Upload a dataset in the sidebar and click <strong style='color:#a78bfa;'>🚀 Run Analysis</strong> to begin.
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# FOOTER
# ════════════════════════════════════════════════════════════════════════════
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center; color:#374151; font-size:0.78rem; padding:16px 0; border-top:1px solid rgba(255,255,255,0.06);'>
  🧠 DataMind AI · Multi-Agent Data Analysis System ·
  Built with Streamlit, Plotly, Pandas, scikit-learn
</div>
""", unsafe_allow_html=True)
