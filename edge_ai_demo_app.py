# edge_ai_demo_app.py

import streamlit as st
import serial
import threading
import time
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import os
import json

# Configuration
SERIAL_PORT = '/dev/ttyUSB0'  # Change as per your system
BAUD_RATE = 115200
DATA_FILE = 'sensor_data.csv'
IMAGE_UPLOAD_DIR = 'uploads/'
HEATMAP_DIR = 'heatmaps/'

os.makedirs(IMAGE_UPLOAD_DIR, exist_ok=True)
os.makedirs(HEATMAP_DIR, exist_ok=True)

# Shared data
sensor_data = []

# Serial reading thread
def read_serial():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        while True:
            line = ser.readline().decode('utf-8').strip()
            if line:
                try:
                    data = json.loads(line)
                    sensor_data.append(data)
                    with open(DATA_FILE, 'a') as f:
                        f.write(json.dumps(data) + '\n')
                except Exception as e:
                    print("Serial parse error:", e)
    except Exception as e:
        print("Serial connection error:", e)

threading.Thread(target=read_serial, daemon=True).start()

# Streamlit UI
st.set_page_config(page_title="Edge AI Demo", layout="wide")
st.sidebar.title("Demo Mode")
demo_mode = st.sidebar.selectbox("Choose a use case", ["DR Eye Camp", "Doctor vs AI", "Live Sensor Room", "Fault Playback"])

if demo_mode == "DR Eye Camp":
    st.title("🩺 AI-Powered DR Screening")
    uploaded_file = st.file_uploader("Upload fundus image", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        file_path = os.path.join(IMAGE_UPLOAD_DIR, uploaded_file.name)
        with open(file_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        st.image(file_path, caption="Uploaded Image", width=300)

        # Simulate prediction
        st.success("Prediction: Moderate DR")
        st.info("Confidence: 82%")

        # Simulated heatmap
        heatmap_path = os.path.join(HEATMAP_DIR, 'heatmap_example.jpg')
        if os.path.exists(heatmap_path):
            st.image(heatmap_path, caption="Attention Heatmap", width=300)

        if st.button("Export PDF Report"):
            st.success("PDF Report generated at /reports/report_01.pdf")

elif demo_mode == "Doctor vs AI":
    st.title("🧠 Doctor vs AI")
    st.write("Compare AI prediction with expert opinion")
    st.image("uploads/sample_dr.jpg", width=300)
    st.columns(2)[0].markdown("**AI Prediction:** Moderate DR\n\nConfidence: 82%")
    st.columns(2)[1].markdown("**Doctor Label:** Mild DR")

elif demo_mode == "Live Sensor Room":
    st.title("⚙️ Live Sensor Dashboard")
    df = pd.DataFrame(sensor_data[-50:])
    if not df.empty:
        st.line_chart(df[['temp', 'vibration', 'pressure']])
        st.dataframe(df)
    else:
        st.info("Waiting for sensor data over serial...")

elif demo_mode == "Fault Playback":
    st.title("🎞️ Fault Playback")
    try:
        with open(DATA_FILE, 'r') as f:
            logs = [json.loads(line) for line in f.readlines()[-200:]]
        df = pd.DataFrame(logs)
        fig, ax = plt.subplots()
        df['anomaly'] = df['anomaly_score'].apply(lambda x: x > 0.5)
        ax.plot(df['timestamp'], df['temp'], label='Temp')
        ax.plot(df['timestamp'], df['pressure'], label='Pressure')
        ax.plot(df['timestamp'], df['vibration'], label='Vibration')
        ax.scatter(df[df['anomaly']]['timestamp'], df[df['anomaly']]['temp'], color='red', label='Anomaly')
        plt.xticks(rotation=45)
        st.pyplot(fig)
    except Exception as e:
        st.error("No log data found or format error: " + str(e))
