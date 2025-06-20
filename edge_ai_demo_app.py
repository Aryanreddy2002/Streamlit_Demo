import streamlit as st
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

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
    st.image("https://i.imgur.com/B5qz9Hd.jpg", width=300)  # Example image
    st.columns(2)[0].markdown("**AI Prediction:** Moderate DR  \nConfidence: 82%")
    st.columns(2)[1].markdown("**Doctor Label:** Mild DR")

elif demo_mode == "Fault Playback":
    st.title("🎞️ Fault Playback Demo")
    st.write("Simulated sensor anomaly over time")
    time_series = pd.date_range(start="2023-01-01", periods=100, freq="T")
    temp = np.random.normal(30, 1, size=100)
    temp[70:75] += 6  # Simulated fault
    anomaly_score = np.random.rand(100)
    anomaly_score[70:75] = 0.95  # Fault peak
    df = pd.DataFrame({"Time": time_series, "Temp": temp, "Anomaly": anomaly_score})

    fig, ax = plt.subplots()
    ax.plot(df["Time"], df["Temp"], label="Temp")
    ax.scatter(df[df["Anomaly"] > 0.9]["Time"], df[df["Anomaly"] > 0.9]["Temp"], color="red", label="Anomaly")
    plt.xticks(rotation=45)
    st.pyplot(fig)

