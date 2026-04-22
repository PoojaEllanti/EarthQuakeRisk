import streamlit as st
import pandas as pd
import requests

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Earthquake Info Dashboard", layout="wide")

# ---------------- TITLE ----------------
st.title("🌍 Earthquake Information Dashboard")
st.write("Live earthquake updates and awareness system")

# ---------------- FETCH DATA ----------------
url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"

st.subheader("📡 Recent Significant Earthquakes (Last 24 Hours)")

earthquakes = []

try:
    response = requests.get(url)
    data = response.json()

    for quake in data['features']:
        mag = quake['properties']['mag']
        place = quake['properties']['place']

        if mag is None or mag < 4.5:
            continue

        coords = quake['geometry']['coordinates']
        lon, lat = coords[0], coords[1]

        earthquakes.append({
            "Place": place,
            "Magnitude": mag,
            "Latitude": lat,
            "Longitude": lon
        })

    earthquakes = earthquakes[:10]

    df = pd.DataFrame(earthquakes)
    st.dataframe(df)

except:
    st.error("⚠️ Unable to fetch live earthquake data")

# ---------------- ALERT SECTION ----------------
st.subheader("🚨 Active Alerts")

if len(earthquakes) == 0:
    st.success("No significant earthquakes detected recently")

for q in earthquakes:
    if q["Magnitude"] >= 6:
        st.error(f"🔴 HIGH ALERT: {q['Place']} (Mag {q['Magnitude']})")
    elif q["Magnitude"] >= 5:
        st.warning(f"🟡 Moderate Activity: {q['Place']} (Mag {q['Magnitude']})")

# ---------------- EDUCATION ----------------
st.subheader("📘 What does magnitude mean?")

st.info("""
🟢 Below 4.0 → Usually not felt  
🟡 4.0 - 5.9 → Noticeable shaking  
🔴 6.0+ → Can cause serious damage  
""")

# ---------------- SAFETY ----------------
st.subheader("🚨 General Safety Guidelines")

st.write("""
- Drop, Cover, and Hold  
- Stay away from windows  
- Move to open area if outside  
- Do not use elevators  
- Follow official emergency alerts  
""")

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("🌍 Real-time Earthquake Awareness System")