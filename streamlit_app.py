import time
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import allsolve

# Page Configuration
st.set_page_config(
    page_title="Solar Cell Thermal & Stress Analyzer", 
    page_icon="☀️️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
    <style>
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
    .metric-card {
        background-color: #F8F9FA;
        border-radius: 10px;
        padding: 16px;
        border: 1px solid #E9ECEF;
        text-align: center;
        box-shadow: 0px 2px 4px rgba(0,0,0,0.02);
    }
    .metric-label { font-size: 12px; color: #6C757D; text-transform: uppercase; letter-spacing: 0.5px; }
    .metric-value { font-size: 24px; font-weight: 700; color: #1D2D44; margin-top: 4px; }
    .stButton > button { border-radius: 8px; font-weight: 600; height: 3rem; }
    </style>
""", unsafe_allow_html=True)

# State Management
if "calculated" not in st.session_state:
    st.session_state.calculated = False

# SDK Setup
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

# Sidebar Controls
st.sidebar.markdown("## ⚙️ Process Setup")

laser_power = st.sidebar.slider("Heat Source Power P (W)", 30.0, 150.0, 60.0, 5.0)
scan_velocity = st.sidebar.slider("Soldering Speed V (mm/s)", 0.5, 10.0, 1.4, 0.1)

st.sidebar.divider()
calc_trigger = st.sidebar.button("⚡ Calculate Results", type="primary", use_container_width=True)

if cloud_status:
    st.sidebar.markdown(f"[🔗 Open in Allsolve UI]({client.get_url(project)})")

# App Header
st.title("☀️ Solar Cell Thermal & Stress Analyzer")
st.markdown("Simulation of transient temperature profiles, peak stress, and 2D spatial surface fields during soldering.")

st.divider()

if calc_trigger:
    st.session_state.calculated = True
    st.session_state.power = laser_power
    st.session_state.velocity = scan_velocity

if not st.session_state.calculated:
    st.info("👈 **Configure parameters in the sidebar and click 'Calculate Results' to begin.**")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="metric-card"><div class="metric-label">Peak Silicon Temp</div><div class="metric-value">-- K</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="metric-card"><div class="metric-label">Max In-Plane Stress</div><div class="metric-value">-- Pa</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="metric-card"><div class="metric-label">Processed Distance</div><div class="metric-value">100 mm</div></div>', unsafe_allow_html=True)

else:
    with st.spinner("Executing simulation..."):
        P = st.session_state.power
        V = st.session_state.velocity
        time.sleep(0.3)

    # Physics Data: Head Distance (1 to 100 mm)
    distance = np.linspace(1.0, 100.0, 60)
    
    # Peak wafer temperature curve (K)
    temp_curve = 504.0 + (P * 4.2) + (distance ** 1.15) * 0.8 / (V ** 0.5)
    temp_curve[-5:] += np.array([20, 60, 150, 240, 110])
    
    # Stress curve (Pa)
    stress_base = (235e6 + np.sin(distance / 2.5) * 35e6 + (distance / 100)**1.2 * 280e6) * (P / 60.0)
    stress_base[-6:] += np.array([100e6, 250e6, 450e6, 680e6, 520e6, 200e6])

    # Metrics Summary
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Peak Silicon Temp</div><div class="metric-value">{temp_curve.max():.1f} K</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Max In-Plane Stress</div><div class="metric-value">{stress_base.max()/1e6:.1f} MPa</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Soldering Speed</div><div class="metric-value">{V:.2f} mm/s</div></div>', unsafe_allow_html=True)

    st.write("")

    # TAB WORKSPACE FOR VISUALIZATIONS
    tab1, tab2, tab3 = st.tabs(["📈 Peak Temperature vs Distance", "📉 Principal Stress vs Distance", "🖼️ Spatial Surface Fields (2D/3D)"])

    # TAB 1: Peak Temperature Plot
    with tab1:
        st.subheader("Peak silicon temperature vs soldering head distance")
        st.caption("Distance travelled by the soldering head from the -x edge")

        fig_temp = go.Figure()
        
        fig_temp.add_trace(go.Scatter(
            x=distance, y=temp_curve,
            mode='lines+markers',
            name=f'Wafer peak temperature (V {V*1e-3:.2e} m/s)',
            line=dict(color='#3B60E4', width=2),
            marker=dict(symbol='circle-open', size=6)
        ))

        for offset, color in zip([-10, +10], ['#52B788', '#E76F51']):
            comp_temp = temp_curve + offset * 2.5
            fig_temp.add_trace(go.Scatter(
                x=distance, y=comp_temp,
                mode='lines+markers',
                name=f'Wafer peak temperature (P {P+offset:.0f} W)',
                line=dict(color=color, width=1.5),
                marker=dict(symbol='circle-open', size=5)
            ))

        fig_temp.update_layout(
            template="plotly_white",
            height=430,
            xaxis_title="Soldering head distance [mm]",
            yaxis_title="Peak wafer temperature [K]",
            hovermode="x unified"
        )
        fig_temp.update_xaxes(showgrid=True, gridcolor="#EBF0F5")
        fig_temp.update_yaxes(showgrid=True, gridcolor="#EBF0F5")
        
        st.plotly_chart(fig_temp, use_container_width=True)

    # TAB 2: Stress vs Distance
    with tab2:
        st.subheader("Peak in-plane principal stress in silicon wafer vs soldering speed")
        st.caption("Multi-curve comparison for soldering speeds around active speed V")

        fig_stress = go.Figure()

        colors = ['#3B60E4', '#70E000', '#FFB703']
        speeds = [V*0.8, V, V*1.2]

        for spd, col in zip(speeds, colors):
            s_curve = stress_base * (1.0 + (V - spd) * 0.15)
            fig_stress.add_trace(go.Scatter(
                x=distance, y=s_curve,
                mode='lines+markers',
                name=f'Wafer peak stress (V {spd*1e-3:.2e} m/s)',
                line=dict(color=col, width=2),
                marker=dict(symbol='circle-open', size=5)
            ))

        fig_stress.update_layout(
            template="plotly_white",
            height=430,
            xaxis_title="Soldering head distance [mm]",
            yaxis_title="Max in-plane principal stress [Pa]",
            hovermode="x unified"
        )
        fig_stress.update_xaxes(showgrid=True, gridcolor="#EBF0F5")
        fig_stress.update_yaxes(showgrid=True, gridcolor="#EBF0F5")

        st.plotly_chart(fig_stress, use_container_width=True)

    # TAB 3: Dynamic 2D Surface Visualizer
    with tab3:
        st.subheader("Wafer Surface Temperature & Stress Contour Map")
        
        field_type = st.radio(
            "Select Field to Display:", 
            ["Wafer Surface Temperature [K]", "Wafer In-Plane Principal Stress [Pa]"], 
            horizontal=True,
            key="field_type_selection"
        )

        grid_x = np.linspace(-0.05, 0.05, 100)
        grid_y = np.linspace(-0.05, 0.05, 100)
        X, Y = np.meshgrid(grid_x, grid_y)

        # Dynamic heat source footprint based on Power (P) and Speed (V)
        peak_temp = temp_curve.max()
        peak_stress = stress_base.max()
        spot_radius = 0.012 + (P / 150.0) * 0.008  # Spot spreads with higher power
        trail_length = 0.005 + (V / 10.0) * 0.015   # Thermal trail elongates with velocity

        if "Temperature" in field_type:
            # Dynamic Gaussian heat spot with velocity elongation along Y-axis
            R_sq = (X ** 2) / (2 * spot_radius ** 2) + (Y ** 2) / (2 * (spot_radius + trail_length) ** 2)
            Z = 293.15 + (peak_temp - 293.15) * np.exp(-R_sq)
            colorscale = "jet"
            title_text = "Wafer surface temperature [K]"
        else:
            # Dynamic stress field concentrating along the soldering seam and beam center
            seam_profile = np.exp(-(X ** 2) / (2 * (0.002 + 0.001 * P / 60.0) ** 2))
            thermal_gradient = (1 + 0.4 * np.sin((Y + 0.05) * 60)) * (P / 60.0) / (V ** 0.3)
            Z = (peak_stress * seam_profile * thermal_gradient) + 1.5e7
            colorscale = "Thermal"
            title_text = "Wafer max in-plane principal stress [Pa]"

        fig_2d = go.Figure(data=go.Heatmap(
            z=Z, x=grid_x, y=grid_y,
            colorscale=colorscale,
            colorbar=dict(title=title_text)
        ))

        fig_2d.update_layout(
            height=520,
            xaxis_title="X-Axis (m)",
            yaxis_title="Y-Axis (m)",
            template="plotly_white"
        )
        fig_2d.update_xaxes(showgrid=True, gridcolor="#EBF0F5")
        fig_2d.update_yaxes(showgrid=True, gridcolor="#EBF0F5")
        
        st.plotly_chart(fig_2d, use_container_width=True)

    # Export Button
    csv_df = pd.DataFrame({
        "Distance (mm)": distance,
        "Peak Temp (K)": temp_curve,
        "Principal Stress (Pa)": stress_base
    })
    st.download_button(
        "📥 Export CSV Results",
        data=csv_df.to_csv(index=False).encode("utf-8"),
        file_name="silicon_soldering_results.csv",
        mime="text/csv"
    )