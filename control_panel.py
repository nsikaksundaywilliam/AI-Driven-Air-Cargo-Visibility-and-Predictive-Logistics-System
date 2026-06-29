import streamlit as st
import requests

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="SMART Technologies",
    page_icon="✈",
    layout="centered"
)

st.title("✈ SMART Technologies")
st.subheader("Cargo Operations Console")

st.write("Click a button below to simulate a cargo event.")

# ==========================================
# WEBHOOK
# ==========================================

WEBHOOK = "https://vaguely-gumball-powdery.ngrok-free.dev/webhook/cargo-delay-alert"

# ==========================================
# SEND FUNCTION
# ==========================================

def send(payload):

    st.write("Sending payload...")
    st.json(payload)

    headers = {
        "ngrok-skip-browser-warning": "true"
    }

    try:

        st.info("Calling n8n webhook...")

        response = requests.post(
            WEBHOOK,
            json=payload,
            headers=headers,
            timeout=60
        )

        st.success("Webhook responded")

        st.write("Status Code:", response.status_code)

        st.code(response.text)

        if response.status_code == 200:
            st.success("✅ Cargo Event Sent Successfully!")
        else:
            st.error(f"Webhook returned {response.status_code}")

    except Exception as e:
        st.error(f"Connection Error:\n{e}")

# ==========================================
# NORMAL SHIPMENT
# ==========================================

if st.button("✈ Simulate Normal Shipment", use_container_width=True):

    payload = {
        "cargo_id":"CG001",
        "awb_number":"AWB123456",
        "origin_airport":"LOS",
        "destination_airport":"ABV",
        "current_status":"In Transit",
        "shipment_stage":"Air Transit",
        "current_location":"Lagos",
        "weather_condition":"Clear",
        "route_status":"Normal",
        "delay_hours":0
    }

    send(payload)

# ==========================================
# WEATHER DELAY
# ==========================================

if st.button("⚠ Simulate Weather Delay", use_container_width=True):

    payload = {
        "cargo_id":"CG001",
        "awb_number":"AWB123456",
        "origin_airport":"LOS",
        "destination_airport":"ABV",
        "current_status":"In Transit",
        "shipment_stage":"Air Transit",
        "current_location":"Lagos",
        "weather_condition":"Thunderstorm",
        "route_status":"Congested",
        "delay_hours":2
    }

    send(payload)

# ==========================================
# HIGH RISK
# ==========================================

if st.button("🚨 Simulate High Risk Cargo", use_container_width=True):

    payload = {
        "cargo_id":"CG001",
        "awb_number":"AWB123456",
        "origin_airport":"LOS",
        "destination_airport":"ABV",
        "current_status":"Delayed",
        "shipment_stage":"Air Transit",
        "current_location":"Lagos",
        "weather_condition":"Thunderstorm",
        "route_status":"Congested",
        "delay_hours":6
    }

    send(payload)
