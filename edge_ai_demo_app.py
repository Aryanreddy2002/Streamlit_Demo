import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

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
    st.title("🎞️ Fault Playback - Air Compressor Sensors")
    st.write("Simulated temperature with anomaly markers")

    time_series = pd.date_range(start="2025-06-20", periods=100, freq="T")
    temp = np.random.normal(30, 1, size=100)
    temp[70:75] += 5  # Simulated fault spike
    anomaly_score = np.random.rand(100)
    anomaly_score[70:75] = 0.95  # Highlight fault region

    fig, ax = plt.subplots()
    ax.plot(time_series, temp, label="Temperature (°C)")
    ax.scatter(time_series[anomaly_score > 0.9], temp[anomaly_score > 0.9], color="red", label="Anomaly")
    plt.xticks(rotation=45)
    ax.legend()
    st.pyplot(fig)

