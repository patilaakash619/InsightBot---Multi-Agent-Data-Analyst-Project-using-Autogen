"""InsightBot UI  ->  uv run streamlit run app.py"""
import streamlit as st
from insightbot.workflows.analysis_flow import run_analysis
from insightbot.config.settings import UPLOADS_DIR, OUTPUTS_DIR

st.set_page_config(page_title="InsightBot", page_icon="📊")
st.title("📊 InsightBot — Multi-Agent Data Analyst")

# 1. Upload a CSV (or use existing ones)
uploaded = st.file_uploader("Upload a CSV", type="csv")
if uploaded:
    (UPLOADS_DIR / uploaded.name).write_bytes(uploaded.getvalue())
    st.success(f"Saved {uploaded.name}")

csv_files = sorted(p.name for p in UPLOADS_DIR.glob("*.csv"))
csv_name = st.selectbox("Dataset", csv_files)

# 2. Ask a question
question = st.text_input("Your question",
                         "Which region has the highest revenue? Plot revenue by region.")

# 3. Run the agent team
if st.button("Analyze", type="primary") and csv_name:
    import time
    start = time.time()
    with st.spinner("Agent team working... (watch the terminal for the full conversation)"):
        answer = run_analysis(question, csv_name)
    st.subheader("Answer")
    st.write(answer)

    charts = [p for p in OUTPUTS_DIR.glob("*.png") if p.stat().st_mtime >= start]
    if charts:
        st.subheader("Charts")
        for chart in sorted(charts):
            st.image(str(chart), caption=chart.name)
    else:
        st.info("No charts were generated for this question.")