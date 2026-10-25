from pathlib import Path
from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="RehabSense", layout="wide")

st.markdown(
    """
    <style>
    .metric-row {
        display: flex;
        justify-content: space-between;
        margin-bottom: 2rem;
        margin-top: 1rem;
    }
    .metric-box {
        flex: 1;
        padding: 0 1.5rem;
        border-left: 4px solid #2c3e50;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #6c757d;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.3rem;
        font-weight: 500;
    }
    .metric-value {
        font-size: 2.8rem;
        font-weight: 600;
        color: #1e1e1e;
        margin: 0;
        line-height: 1;
    }
    .header-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 0.2rem;
    }
    .header-subtitle {
        font-size: 1.1rem;
        color: #6c757d;
        margin-bottom: 1rem;
    }
    .footer {
        text-align: center;
        color: #adb5bd;
        font-size: 0.8rem;
        margin-top: 3rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

DATA_PATH = Path(__file__).parent / "data" / "sessions.csv"

if not DATA_PATH.exists():
    st.markdown('<div class="header-title">RehabSense</div>', unsafe_allow_html=True)
    st.info("No session data found. Complete a workout to generate metrics.")
    st.stop()

all_sessions = pd.read_csv(DATA_PATH, parse_dates=["timestamp"]).sort_values("timestamp")

if all_sessions.empty:
    st.markdown('<div class="header-title">RehabSense</div>', unsafe_allow_html=True)
    st.info("The session log is empty. Complete a workout to generate metrics.")
    st.stop()

with st.sidebar:
    st.header("System Overview")
    st.write("Camera-based physiotherapy exercise monitoring prototype.")
    st.warning(
        "Engineering prototype only. Not a diagnostic device or a substitute for professional medical care."
    )
    st.divider()
    
    exercise_options = all_sessions["exercise"].unique()
    selected_exercise = st.selectbox("Select Exercise", exercise_options)
    
    filtered_sessions = all_sessions[all_sessions["exercise"] == selected_exercise]
    
    if not filtered_sessions.empty:
        total_reps = filtered_sessions["reps"].sum()
        st.metric("All-Time Repetitions", int(total_reps))
        
    st.divider()
    if st.button("Refresh Data"):
        st.rerun()

st.markdown('<div class="header-title">RehabSense</div>', unsafe_allow_html=True)
st.markdown(f'<div class="header-subtitle">Clinical Monitoring Dashboard - {selected_exercise.replace("_", " ").title()}</div>', unsafe_allow_html=True)

latest_session = filtered_sessions.iloc[-1]

st.divider()

st.subheader("Latest Session Metrics")
st.markdown(
    f"""
    <div class="metric-row">
        <div class="metric-box">
            <div class="metric-label">Repetitions</div>
            <div class="metric-value">{int(latest_session['reps'])}</div>
        </div>
        <div class="metric-box">
            <div class="metric-label">Min Angle</div>
            <div class="metric-value">{latest_session['min_angle']:.1f}&deg;</div>
        </div>
        <div class="metric-box">
            <div class="metric-label">Angular Excursion</div>
            <div class="metric-value">{latest_session['angular_excursion']:.1f}&deg;</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

st.subheader("Recovery Trend")

if len(filtered_sessions) < 2:
    st.info("Complete at least two sessions to view a longitudinal progress trend.")
else:
    excursion_figure = px.line(
        filtered_sessions,
        x="timestamp",
        y="angular_excursion",
        markers=True
    )
    excursion_figure.update_layout(
        template="simple_white",
        margin=dict(l=0, r=0, t=10, b=0),
    )
    excursion_figure.update_traces(
        line_color="#2c3e50", 
        line_width=2,
        marker=dict(size=8, color="#2c3e50")
    )
    excursion_figure.update_xaxes(showgrid=False, title="Date")
    excursion_figure.update_yaxes(showgrid=True, gridcolor="#f0f0f0", title="Excursion (deg)")
    st.plotly_chart(excursion_figure, use_container_width=True)

st.divider()

with st.expander("Session History"):
    st.dataframe(filtered_sessions, use_container_width=True, hide_index=True)

st.markdown(
    f'<div class="footer">Data stored locally | Last updated: {datetime.now().strftime("%Y-%m-%d %H:%M")}</div>', 
    unsafe_allow_html=True
)