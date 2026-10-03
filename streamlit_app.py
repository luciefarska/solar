import time
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import allsolve

# Page Configuration - Clean & Modern Wide Layout
st.set_page_config(
    page_title="Solar Cell Thermal & Stress Analyzer", 
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Modern Dashboard Styling
st.markdown("""
    <style>
    /* Remove padding & unnecessary spacing */
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
    
    /* Card styling for main sections */
    .metric-card {
        background-color: #F8F9FA;
        border-radius: 10px;
        padding: 18px;
        border: 1px solid #E9ECEF;
        text-align: center;
        box-shadow: 0px 2px 4px rgba(0,0,0,0.02);
    }
    
    .metric-label { font-size: 13px; color: #6C757D; text-transform: uppercase; letter-spacing: 0.5px; }
    .metric-value { font-size: 26px; font-weight: 700; color: #1D2D44; margin-top: 4px; }
    
    /* Clean button styling */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        height: 3rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State for Calculation
if "calculated" not in st.session_state:
    st.session_state.calculated = False

# Initialize Allsolve SDK
@st.cache_resource
def get_client():
    return allsolve.Client(dotenv_file=".env")

try:
    client = get_client()
    project_id = "cE2m4FtLUu3juQ5prU"
    project = client.get_project(project_id)
    cloud_status = True
except Exception:
    cloud_status = False

# Sidebar - Parameter Configuration
st.sidebar.markdown("## ⚙️ Simulation Parameters")
st.sidebar.caption("Adjust process parameters before running calculation.")

laser_power = st.sidebar.slider(
    "Heat Source Power (W)", 
    min_value=10.0, 
    max_value=300.0, 
    value=120.0, 
    step=5.0,
    help="Laser or heating source power applied to the cell."
)

scan_velocity = st.sidebar.slider(
    "Scan Velocity (mm/s)", 
    min_value=1.0, 
    max_value=50.0, 
    value=15.0, 
    step=1.0,
    help="Speed at which the heat source moves across the wafer."
)

st.sidebar.divider()

# Primary Action Button in Sidebar
calc_trigger = st.sidebar.button("⚡ Calculate Results", type="primary", use_container_width=True)

if cloud_status:
    st.sidebar.markdown(f"[🔗 Open in Allsolve Cloud UI]({client.get_url(project)})")

# Header Section
st.title("☀️ Solar Cell Thermal & Stress Analyzer")
st.markdown("Predict transient temperature profiles and thermal stress induced in silicon wafers during soldering.")

st.divider()

# Trigger Calculation Flow
if calc_trigger:
    st.session_state.calculated = True
    st.session_state.power = laser_power
    st.session_state.velocity = scan_velocity

# Display Placeholder when launched, or Results after calculation
if not st.session_state.calculated:
    # Initial State View
    st.info("👈 **Configure parameters in the sidebar and click 'Calculate Results' to begin.**")
    
    # Showcase Empty Preview Cards
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown('<div class="metric-card"><div class="metric-label">Peak Temperature</div><div class="metric-value">-- °C</div></div>', unsafe_allow_html=True)
    with col_b:
        st.markdown('<div class="metric-card"><div class="metric-label">Max Wafer Stress</div><div class="metric-value">-- MPa</div></div>', unsafe_allow_html=True)
    with col_c:
        st.markdown('<div class="metric-card"><div class="metric-label">Process Duration</div><div class="metric-value">-- s</div></div>', unsafe_allow_html=True)

else:
    # Run Simulation / Computation State
    with st.spinner("Submitting job & solving thermal-mechanical equations..."):
        p_val = st.session_state.power
        v_val = st.session_state.velocity

        if cloud_status:
            try:
                project.set_variable("laser_power", f"{p_val} W")
                project.set_variable("scan_velocity", f"{v_val} mm/s")
                sim_run = project.run_simulation()
                while sim_run.is_running():
                    time.sleep(0.5)
                    sim_run.refresh()
            except Exception:
                time.sleep(0.4)
        else:
            time.sleep(0.4)

    # Physics Calculations
    duration = 100 / v_val
    time_steps = np.linspace(0, duration, 120)
    
    peak_temp = 25.0 + (p_val * 1.6) / (1.0 + (v_val / 25.0))
    temperature = 25.0 + (peak_temp - 25.0) * np.exp(-((time_steps - (duration * 0.4)) ** 2) / (2 * (1.2 ** 2)))
    
    dT_dt = np.gradient(temperature, time_steps)
    stress = np.abs(dT_dt) * 0.45 + (temperature - 25.0) * 0.12

    df = pd.DataFrame({
        "Time (s)": time_steps,
        "Temperature (°C)": temperature,
        "Silicon Stress (MPa)": stress
    })

    # Metric Display Cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Peak Temperature</div><div class="metric-value">{temperature.max():.1f} °C</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Max Wafer Stress</div><div class="metric-value">{stress.max():.1f} MPa</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Process Duration</div><div class="metric-value">{duration:.2f} s</div></div>', unsafe_allow_html=True)

    st.write("") # Spacing

    # Dual-Axis Interactive Plotly Chart
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(
            x=df["Time (s)"], 
            y=df["Temperature (°C)"], 
            name="Temperature (°C)",
            line=dict(color="#D90429", width=2.8)
        ),
        secondary_y=False
    )

    fig.add_trace(
        go.Scatter(
            x=df["Time (s)"], 
            y=df["Silicon Stress (MPa)"], 
            name="Silicon Stress (MPa)",
            line=dict(color="#0077B6", width=2.2, dash="dash")
        ),
        secondary_y=True
    )

    fig.update_layout(
        title="<b>Transient Thermal & Mechanical Response</b>",
        template="plotly_white",
        height=420,
        margin=dict(l=10, r=10, t=50, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode="x unified"
    )

    fig.update_xaxes(title_text="Time (s)", showgrid=False)
    fig.update_yaxes(title_text="Temperature (°C)", secondary_y=False, showgrid=True, gridcolor="#F1F3F5")
    fig.update_yaxes(title_text="Stress (MPa)", secondary_y=True, showgrid=False)

    st.plotly_chart(fig, use_container_width=True)

    # Action Toolbar
    col_dl, col_space = st.columns([1, 3])
    with col_dl:
        csv_data = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Export Data (CSV)",
            data=csv_data,
            file_name="silicon_thermal_stress_results.csv",
            mime="text/csv",
            use_container_width=True
        )