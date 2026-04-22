import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from model import train_model
from geopy.geocoders import Nominatim

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Earthquake Risk Predictor", layout="wide")

# ---------------- CSS ----------------
st.markdown("""
<style>
.title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    color: #0b3d91;
}
.card {
    padding: 18px;
    border-radius: 12px;
    margin-top: 15px;
}
.low {background-color: #d4edda;}
.medium {background-color: #fff3cd;}
.high {background-color: #f8d7da;}
.metric-box {
    background: #ffffff;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ---------------- MODEL ----------------
model, best_acc, best_name, all_results = train_model()

# ---------------- TITLE ----------------
st.markdown('<div class="title">🌍 Earthquake Risk Prediction System</div>', unsafe_allow_html=True)
st.write("### Enter any place name (works globally)")

# ---------------- INPUT ----------------
location_name = st.text_input("📍 Enter Location (e.g., Japan, Chennai, Delhi)")

intensity = st.selectbox("Shaking Intensity", ["Mild", "Moderate", "Strong"])

# Map intensity → magnitude
mag_map = {
    "Mild": 3.5,
    "Moderate": 5.0,
    "Strong": 6.5
}

mag = mag_map[intensity]

# Map intensity → realistic depth
depth_map = {
    "Mild": 70,
    "Moderate": 30,
    "Strong": 10
}

depth = depth_map[intensity]

geolocator = Nominatim(user_agent="quake_app")

# ---------------- PREDICTION ----------------
if st.button("Predict Risk"):

    if location_name.strip() == "":
        st.warning("Please enter a location")
    else:
        try:
            location = geolocator.geocode(location_name)

            lat = location.latitude
            lon = location.longitude

            prediction = model.predict([[mag, depth, lat, lon]])[0]

            # ✅ PROPER RISK PROBABILITY
            proba = model.predict_proba([[mag, depth, lat, lon]])[0]

            low_p = round(proba[0] * 100, 1)
            med_p = round(proba[1] * 100, 1)
            high_p = round(proba[2] * 100, 1)

            # Main risk score = High probability
            risk_score = high_p

            st.subheader(f"📍 Location: {location_name}")

            col1, col2 = st.columns(2)

            with col1:
                st.metric("🔴 High Risk Probability", f"{risk_score}%")

            with col2:
                st.metric("🏆 Best Model", best_name)

            # ---------------- RESULT ----------------
            if prediction == 0:
                st.markdown('<div class="card low"><h3>🟢 Low Risk</h3></div>', unsafe_allow_html=True)
            elif prediction == 1:
                st.markdown('<div class="card medium"><h3>🟡 Medium Risk</h3></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="card high"><h3>🔴 High Risk 🚨</h3></div>', unsafe_allow_html=True)

            # ---------------- BREAKDOWN ----------------
            st.subheader("📊 Risk Breakdown")

            st.write(f"🟢 Low: {low_p}%")
            st.write(f"🟡 Medium: {med_p}%")
            st.write(f"🔴 High: {high_p}%")

            # ---------------- EXPLANATION ----------------
            st.subheader("💡 Why this result?")

            if prediction == 2:
                st.write("👉 Strong earthquake detected, which can cause serious damage.")
                st.write("👉 Shallow depth increases impact on surface.")
            elif prediction == 1:
                st.write("👉 Moderate earthquake strength.")
                st.write("👉 Some structural damage may occur.")
            else:
                st.write("👉 Weak earthquake, minimal impact expected.")

            # ---------------- SAFETY GUIDELINES ----------------
            st.subheader("🚨 Safety Guidelines")

            if prediction == 0:
                st.info("""
                ✅ Stay calm and do not panic  
                ✅ Monitor news and updates  
                ✅ Ensure emergency contacts are accessible  
                """)

            elif prediction == 1:
                st.warning("""
                ⚠️ Stay alert and prepared  
                ⚠️ Keep emergency kit ready (water, torch, first aid)  
                ⚠️ Avoid staying near weak structures  
                ⚠️ Identify safe spots (under table, open area)  
                """)

            else:
                st.error("""
                🚨 DROP, COVER, HOLD immediately  
                🚨 Move to open area away from buildings  
                🚨 Avoid glass, windows, and heavy objects  
                🚨 Do NOT use elevators  
                🚨 Follow official emergency instructions  
                🚨 Help others if safe to do so  
                """)

        except:
            st.error("Location not found. Try another name.")

# ---------------- MODEL PERFORMANCE ----------------
st.subheader("🤖 Model Performance")

df_models = pd.DataFrame({
    "Model": list(all_results.keys()),
    "Accuracy (%)": [round(v*100, 2) for v in all_results.values()]
})

st.dataframe(df_models)

st.success(f"Best Model: {best_name} ({round(best_acc*100,2)}%)")

# ---------------- CHART ----------------
st.subheader("📊 Earthquake Intensity Pattern")

data = pd.read_csv("earthquake.csv")

fig, ax = plt.subplots()
data['mag'].plot(kind='kde', ax=ax)

st.pyplot(fig)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("🚀 Final Clean ML System | Balanced Predictions")