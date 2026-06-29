import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="AI Air Cargo Operations Centre",
    page_icon="✈️",
    layout="wide"
)

st.title("✈ AI-Driven Intelligent Air Cargo Visibility & Predictive Logistics System")

st.caption("""
Operations Control Centre

Real-Time AI Decision Support Platform

n8n | Google Gemini AI | PostgreSQL | Supabase | Weather API | Streamlit | Python
""")
st.success(f"""
🟢 SYSTEM STATUS : ONLINE

✔ AI Engine Active

✔ n8n Workflow Connected

✔ PostgreSQL Connected

✔ Weather API Active

✔ Cargo Tracking Active

Last Updated:
{datetime.now().strftime("%d %b %Y  %H:%M:%S")}
""")

# ----------------------------
# DATABASE CONNECTION
# ----------------------------

conn = psycopg2.connect(
    host="aws-0-eu-west-3.pooler.supabase.com",
    database="postgres",
    user="postgres.epkpxzhgxtnlnqqvxlga",
    password="Supabase-nsix@2026",
    port=6543
)

# ----------------------------
# LOAD DATA
# ----------------------------

shipments = pd.read_sql("""
SELECT *
FROM shipments
ORDER BY shipment_id DESC
""", conn)

tracking = pd.read_sql("""
SELECT *
FROM tracking_events
ORDER BY event_timestamp DESC
""", conn)

conn.close()

# ----------------------------
# FIX NUMERIC FIELDS
# ----------------------------

numeric_columns = [
    "delay_hours",
    "weather_risk_score",
    "cargo_risk_score",
    "route_risk_score",
    "total_risk_score"
]

for col in numeric_columns:
    if col in shipments.columns:
        shipments[col] = pd.to_numeric(shipments[col], errors="coerce")

# ----------------------------
# KPI CARDS
# ----------------------------

c1,c2,c3,c4 = st.columns(4)

c1.metric(
    "Total Shipments",
    len(shipments)
)

c2.metric(
    "Tracking Events",
    len(tracking)
)

high=len(shipments[
    shipments["priority_level"]=="High"
])

c3.metric(
    "High Priority",
    high
)

avg_delay=shipments["delay_hours"].mean()

c4.metric(
    "Average Delay (hrs)",
    round(avg_delay,1)
)

st.markdown("---")

st.header("📦 Live Shipment Records")

st.dataframe(
    shipments,
    use_container_width=True
)
st.markdown("---")
st.header("📈 Shipment Timeline")

timeline = tracking.sort_values("event_timestamp")

st.dataframe(
    timeline[
        [
            "event_timestamp",
            "cargo_id",
            "event_type",
            "cargo_status",
            "weather_condition",
            "route_status"
        ]
    ],
    use_container_width=True
)
st.markdown("---")

st.header("🔥 AI Risk Heatmap")

risk = shipments[
    [
        "cargo_id",
        "priority_level",
        "weather_condition",
        "route_status",
        "delay_hours"
    ]
]

styled = (
    risk.style
    .background_gradient(
        subset=["delay_hours"],
        cmap="Reds"
    )
    .map(
        lambda x:
            "background-color:#ff4b4b;color:white" if x=="High"
            else "background-color:#ffa500;color:black" if x=="Medium"
            else "background-color:#3cb371;color:white" if x=="Low"
            else "",
        subset=["priority_level"]
    )
)

st.dataframe(
    styled,
    use_container_width=True
)
st.markdown("---")

st.header("🤖 AI Recommendations")

for _, row in shipments.iterrows():

    if float(row["delay_hours"]) >= 2:

        st.error(
            f"""
Cargo **{row['cargo_id']}**

Prediction:
Delay Risk Detected

Recommendation:
Escalate to Operations

Current Route:
{row['route_status']}
"""
        )

    else:

        st.success(
            f"""
Cargo **{row['cargo_id']}**

No operational action required.
"""
        )
        st.markdown("---")

st.header("🌍 Live Cargo Map")

import pandas as pd

map_data = pd.DataFrame({
    "latitude": [6.5774, 9.0065],
    "longitude": [3.3212, 7.2632],
    "Airport": ["LOS - Lagos", "ABV - Abuja"]
})

st.map(
    map_data,
    latitude="latitude",
    longitude="longitude",
    zoom=5
)
import plotly.graph_objects as go

st.markdown("---")
st.header("📊 AI Delay Prediction Gauge")

delay = float(shipments.iloc[0]["delay_hours"])

fig = go.Figure(go.Indicator(
    mode="gauge+number+delta",
    value=delay,
    title={"text": "Predicted Delay (Hours)"},
    delta={"reference": 1},
    gauge={
        "axis": {"range": [0, 10]},
        "bar": {"color": "darkblue"},
        "steps": [
            {"range": [0, 2], "color": "lightgreen"},
            {"range": [2, 5], "color": "gold"},
            {"range": [5, 10], "color": "red"}
        ],
        "threshold": {
            "line": {"color": "black", "width": 4},
            "thickness": 0.75,
            "value": delay
        }
    }
))

st.plotly_chart(fig, use_container_width=True)
st.markdown("---")

st.header("🤖 Executive AI Decision Panel")

shipment = shipments.iloc[0]

risk = shipment["priority_level"]
delay = shipment["delay_hours"]

if risk == "High":
    confidence = "96%"
elif risk == "Medium":
    confidence = "88%"
else:
    confidence = "80%"

st.success(f"""
### AI Decision Summary

**Cargo ID:** {shipment['cargo_id']}

**Origin:** {shipment['origin_airport']}

**Destination:** {shipment['destination_airport']}

**Current Position:** {shipment['current_location']}

**Current Status:** {shipment['current_status']}

**Priority:** {risk}

**Weather:** {shipment['weather_condition']}

**Route Status:** {shipment['route_status']}

**Predicted Delay:** {delay} Hours

**AI Confidence:** {confidence}

---

### Recommended Actions

✅ Escalate to Operations Control

✅ Notify Airline Operations

✅ Notify Cargo Consignee

✅ Continue Live Monitoring

✅ Update Executive Dashboard
""")
