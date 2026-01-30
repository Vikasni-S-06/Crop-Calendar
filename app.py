import streamlit as st
import folium
import requests
import numpy as np
import joblib
import random

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="SmartCrop Advisor", layout="centered")
st.title("🌾 SmartCrop Advisor")

# ---------------- API KEY ----------------
OPENWEATHER_API_KEY = "97a7e1271940a389ebb19099dcd9fe9c"

# ---------------- LOAD MODEL ----------------
MODEL_PATH = "crop_model.pkl"
ENCODER_PATH = "label_encoder.pkl"

clf = joblib.load(MODEL_PATH)
le = joblib.load(ENCODER_PATH)

# ---------------- SESSION STATE ----------------
if "lat" not in st.session_state:
    st.session_state.lat = None
    st.session_state.lon = None

# ---------------- WEATHER FUNCTION ----------------
def get_weather_from_coords(lat, lon):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }
    res = requests.get(url, params=params)
    if res.status_code == 200:
        data = res.json()
        temp = data["main"]["temp"]
        hum = data["main"]["humidity"]
        rain = data.get("rain", {}).get("1h", 0.0)
        place = data.get("name", "Pinned Location")
        return temp, hum, rain, place
    return None, None, None, None

# ---------------- ML FUNCTIONS ----------------
def recommend_crop(N, P, K, temp, hum, ph, rain):
    X = np.array([[N, P, K, temp, hum, ph, rain]])
    probs = clf.predict_proba(X)[0]
    top_idx = np.argsort(probs)[::-1][:3]
    return [(le.inverse_transform([i])[0], probs[i]) for i in top_idx]

def soil_type(ph):
    if ph < 5.5:
        return "Acidic"
    if ph <= 7.5:
        return "Neutral"
    return "Alkaline"

def pest_alert(crop):
    pests = {
        "rice": ["Rice blast", "Stem borer"],
        "maize": ["Fall armyworm"],
        "wheat": ["Rust", "Aphids"],
        "cotton": ["Bollworm"],
        "tomato": ["Fruit borer"]
    }
    return pests.get(crop.lower(), ["No major pests detected"])

# ---------------- MAP UI ----------------
st.subheader("📍 Select Location on Map")

# Default map location
map_center = [20.5937, 78.9629]

m = folium.Map(location=map_center, zoom_start=5)
m.add_child(folium.LatLngPopup())

# Add marker if location already selected
if st.session_state.lat and st.session_state.lon:
    folium.Marker(
        [st.session_state.lat, st.session_state.lon],
        tooltip="Selected Location",
        icon=folium.Icon(color="red", icon="map-marker")
    ).add_to(m)

map_data = st_folium(m, height=420, width=700)

temp = hum = rain = None

# Capture clicked location
if map_data and map_data.get("last_clicked"):
    st.session_state.lat = map_data["last_clicked"]["lat"]
    st.session_state.lon = map_data["last_clicked"]["lng"]

# Fetch weather if location exists
if st.session_state.lat and st.session_state.lon:
    lat = st.session_state.lat
    lon = st.session_state.lon

    st.success(f"📌 Latitude: {lat:.4f}, Longitude: {lon:.4f}")

    temp, hum, rain, location_name = get_weather_from_coords(lat, lon)

    if temp is not None:
        c1, c2, c3 = st.columns(3)
        c1.metric("🌡 Temperature (°C)", temp)
        c2.metric("💧 Humidity (%)", hum)
        c3.metric("🌧 Rainfall (mm)", rain)
        st.caption(f"Detected location: {location_name}")

# ---------------- SOIL INPUT FORM ----------------
st.subheader("🌱 Soil Parameters")

with st.form("soil_form"):
    N = st.number_input("Nitrogen (N)", 0, 200, 50)
    P = st.number_input("Phosphorus (P)", 0, 200, 30)
    K = st.number_input("Potassium (K)", 0, 300, 20)
    ph = st.number_input("Soil pH", 0.0, 14.0, 6.5)

    submit = st.form_submit_button("Get Crop Recommendation")

# ---------------- OUTPUT ----------------
if submit:
    if temp is None:
        st.error("⚠️ Please pin a location on the map to fetch weather data.")
    else:
        results = recommend_crop(N, P, K, temp, hum, ph, rain)

        st.subheader("🌾 Recommended Crops")
        for crop, prob in results:
            st.write(f"• **{crop}** (confidence {prob:.2f})")

        main_crop = results[0][0]

        st.subheader("🧪 Soil Type")
        st.write(soil_type(ph))

        st.subheader("🐛 Pest Alerts")
        for p in pest_alert(main_crop):
            st.write("• " + p)

        st.subheader("💰 Market Price (Estimated)")
        base = random.randint(1500, 5000)
        st.metric("Current Price (₹/quintal)", base)
        st.metric("Expected Price at Harvest (₹/quintal)", int(base * 1.15))

st.caption("Phase-2 Enhancement: Map-based automatic weather input using OpenWeather API")
