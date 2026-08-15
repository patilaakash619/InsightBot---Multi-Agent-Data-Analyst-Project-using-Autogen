"""InsightBot Terminal  ->  uv run streamlit run app.py"""
import time
import pandas as pd
import streamlit as st
from insightbot.workflows.analysis_flow import run_analysis
from insightbot.config.settings import UPLOADS_DIR, OUTPUTS_DIR

st.set_page_config(page_title="InsightBot Terminal", page_icon="📊",
                   layout="wide", initial_sidebar_state="expanded")

# ---------- styling ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=JetBrains+Mono:wght@400;600&display=swap');
h1, h2, h3 { font-family: 'Space Grotesk', sans-serif !important; letter-spacing: -0.02em; }
[data-testid="stMetricValue"] { font-family: 'JetBrains Mono', monospace; color: #E8B44C; }
[data-testid="stMetricLabel"] { color: #8B94A7; text-transform: uppercase; font-size: 0.7rem; letter-spacing: 0.08em; }
.pipeline { font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; color: #8B94A7;
  border: 1px solid #223050; border-radius: 6px; padding: 6px 14px; display: inline-block; }
.pipeline b { color: #3FBF8F; }
div.stButton > button { background: #E8B44C; color: #0B1220; font-weight: 700; border: none; width: 100%; }
div.stButton > button:hover { background: #F2C766; color: #0B1220; }
[data-testid="stSidebar"] { border-right: 1px solid #223050; }
[data-testid="stImage"] img { max-height: 34vh; object-fit: contain;
  border: 1px solid #223050; border-radius: 6px; background: #0E1526; }
</style>
""", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []

# ---------- sidebar: all controls ----------
with st.sidebar:
    st.markdown("### ⚙️ Controls")
    uploaded = st.file_uploader("Upload CSV", type="csv")
    if uploaded:
        (UPLOADS_DIR / uploaded.name).write_bytes(uploaded.getvalue())
        st.success(f"Saved {uploaded.name}")

    csv_files = sorted(p.name for p in UPLOADS_DIR.glob("*.csv"))
    csv_name = st.selectbox("Dataset", csv_files)

    # question = st.text_area("Question", height=100,
    #     value="Which region has the highest revenue? Plot revenue by region.")
    # run = st.button("▶ Run analysis")
    # st.caption("Agent conversation streams in the terminal.")
    
    question = st.text_area(
        "Question", height=100, value="",
        placeholder="e.g. Which category has the highest total? Plot it.",
    )
    run = st.button("▶ Run analysis", disabled=not question.strip())

# ---------- header ----------
st.title("InsightBot Terminal")
st.markdown('<div class="pipeline">PIPELINE&nbsp;&nbsp; PLANNER ▸ TOOLS ▸ <b>CODER</b> ▸ '
            '<b>EXECUTOR</b> ▸ REVIEWER</div>', unsafe_allow_html=True)
st.write("")

# ---------- KPI row (dataset stats) ----------
# if csv_name:
#     df = pd.read_csv(UPLOADS_DIR / csv_name)
#     num_cols = df.select_dtypes("number").columns
#     k1, k2, k3, k4 = st.columns(4)
#     k1.metric("Dataset", csv_name)
#     k2.metric("Rows", f"{len(df):,}")
#     k3.metric("Columns", f"{df.shape[1]}")
#     if len(num_cols):
#         main = num_cols[-1]
#         k4.metric(f"Total {main}", f"{df[main].sum():,.0f}")

# ---------- KPI row (dataset facts, schema-agnostic) ----------
# ---------- KPI row (dataset facts, schema-agnostic) ----------
if csv_name:
    df = pd.read_csv(UPLOADS_DIR / csv_name)
    k1, k2, k3 = st.columns(3)
    k1.metric("Dataset", csv_name)
    k2.metric("Rows", f"{len(df):,}")
    k3.metric("Numeric / Text cols",
              f"{df.select_dtypes('number').shape[1]} / {df.select_dtypes(exclude='number').shape[1]}")

st.divider()

# ---------- run ----------
if run and csv_name:
    start = time.time()
    with st.spinner("Agent team working..."):
        answer = run_analysis(question, csv_name)
    charts = [p for p in OUTPUTS_DIR.glob("*.png") if p.stat().st_mtime >= start]
    # st.session_state.history.insert(0, {
    #     "question": question, "answer": answer,
    #     "charts": [str(c) for c in sorted(charts)],
    #     "duration": f"{time.time() - start:.0f}s",
    # })
    
    st.session_state.history.insert(0, {
        "dataset": csv_name,
        "question": question, "answer": answer,
        "charts": [str(c) for c in sorted(charts)],
        "duration": f"{time.time() - start:.0f}s",
    })

# ---------- tabs ----------
tab_result, tab_data, tab_history = st.tabs(["📈 Analysis", "🗂 Data preview", "🕘 History"])

with tab_result:
    if st.session_state.history:
        latest = st.session_state.history[0]

        # compact answer strip on top
        st.caption(f"“{latest['question']}”  ·  {latest['duration']}")
        st.markdown(f"**{latest['answer']}**")
        st.write("")

        # charts in a 2-up grid, all visible at once
        charts = latest["charts"]
        if charts:
            for i in range(0, len(charts), 2):
                cols = st.columns(2, gap="medium")
                for col, chart in zip(cols, charts[i:i+2]):
                    col.image(chart, use_container_width=True)
        else:
            st.info("No chart was generated for this question.")
    else:
        st.info("Pick a dataset, type a question in the sidebar, and press Run analysis.")

with tab_data:
    if csv_name:
        st.dataframe(df, use_container_width=True, height=380)

# with tab_history:
#     for i, h in enumerate(st.session_state.history):
#         with st.expander(f"{h['question']}  ·  {h['duration']}"):
#             st.write(h["answer"])
#             for c in h["charts"]:
#                 st.image(c, width=520)

with tab_history:
    if not st.session_state.history:
        st.info("No runs yet.")
    else:
        # preserve first-seen order of datasets (most recent dataset used appears first
        # naturally, since history is newest-first)
        seen = []
        for h in st.session_state.history:
            ds = h.get("dataset", "unknown")
            if ds not in seen:
                seen.append(ds)

        ds_tabs = st.tabs([f"🗂 {ds}" for ds in seen])

        for ds, ds_tab in zip(seen, ds_tabs):
            with ds_tab:
                entries = [h for h in st.session_state.history if h.get("dataset", "unknown") == ds]
                st.caption(f"{len(entries)} question{'s' if len(entries) != 1 else ''} asked on this dataset")
                for h in entries:
                    with st.expander(f"{h['question']}  ·  {h['duration']}"):
                        st.write(h["answer"])
                        for c in h["charts"]:
                            st.image(c, width=520)