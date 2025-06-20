import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

st.set_page_config(page_title="Edge AI Demo", layout="wide")

st.sidebar.title("Demo Mode")
demo_mode = st.sidebar.selectbox("Choose a use case", ["DR Eye Camp", "Doctor vs AI", "Fault Playback"])

if demo_mode == "DR Eye Camp":
    st.title("🩺 AI-Powered DR Screening")
    uploaded_file = st.file_uploader("Upload fundus image", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Fundus Image", width=300)
        st.success("Prediction: **Moderate DR**")
        st.info("Confidence: **82%**")
        st.image("https://i.imgur.com/zJ22rfS.png", caption="Attention Heatmap (simulated)", width=300)
        if st.button("Export PDF Report"):
            st.success("PDF Report would be generated (mock)")

elif demo_mode == "Doctor vs AI":
    st.title("🧠 Doctor vs AI")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("AI Prediction")
        st.image("https://i.imgur.com/B5qz9Hd.jpg", width=250)
        st.write("**Prediction:** Moderate DR")
        st.write("**Confidence:** 82%")
    with col2:
        st.subheader("Doctor Label")
        st.image("https://i.imgur.com/B5qz9Hd.jpg", width=250)
        st.write("**Label:** Mild DR")

elif demo_mode == "Fault Playback":
    st.set_page_config(page_title="Edge AI: Sensor Anomaly Dashboard", layout="wide")

    # --- HEADER ---
    st.markdown("<h1 style='text-align: center; color: #4E8CD9;'>🧠 Edge AI: Live Anomaly Monitoring</h1>", unsafe_allow_html=True)
    st.markdown("### 🔧 Monitoring Air Compressor System | ⏱️ Real-Time Simulation")

    # --- SIDEBAR ---
    st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/STM32_microcontroller_logo.svg/512px-STM32_microcontroller_logo.svg.png", width=150)
    st.sidebar.markdown("## Usecase")
    st.sidebar.info("Anomaly Detection on sensor data from STM32 deployed AI using CNN Autoencoder.")

    # --- SIMULATED DATA ---
    np.random.seed(42)
    time_index = pd.date_range(start="2025-06-20 10:00", periods=100, freq="T")
    temp = np.random.normal(32, 0.5, 100)
    pressure = np.random.normal(1.2, 0.05, 100)
    vibration = np.random.normal(0.03, 0.01, 100)

    # Inject anomaly
    temp[60:65] += 5
    pressure[60:65] += 0.3
    vibration[60:65] += 0.05

    df = pd.DataFrame({
        "Time": time_index,
        "Temperature (°C)": temp,
        "Pressure (bar)": pressure,
        "Vibration (g)": vibration
    }).set_index("Time")

    # --- METRIC CARDS ---
    st.markdown("### 🔍 Current Sensor Status")

    col1, col2, col3 = st.columns(3)
    col1.metric("🌡️ Temperature", f"{temp[-1]:.2f} °C", f"{temp[-1]-temp[-2]:.2f}")
    col2.metric("🔵 Pressure", f"{pressure[-1]:.2f} bar", f"{pressure[-1]-pressure[-2]:.2f}")
    col3.metric("🟣 Vibration", f"{vibration[-1]:.4f} g", f"{vibration[-1]-vibration[-2]:.4f}")

    # --- TABS FOR GRAPHS ---
    tab1, tab2 = st.tabs(["📈 Sensor Trends", "🚨 Detected Anomalies"])

    with tab1:
        st.line_chart(df)

    with tab2:
        st.markdown("### 🚨 Anomaly Region Detected")
        st.dataframe(df.iloc[60:65].style.highlight_max(axis=0, color="salmon"))

    # --- FOOTER ---
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: gray;'>Demo powered by STM32 + Advantech Linux + Edge AI | UI built with ❤️ using Streamlit</p>",
        unsafe_allow_html=True
    )
