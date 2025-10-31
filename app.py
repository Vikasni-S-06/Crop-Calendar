import streamlit as st
import joblib, os, random, math
import pandas as pd, numpy as np
from datetime import date

st.set_page_config(page_title="SmartCrop Advisor", layout="centered")
st.title("🌾 SmartCrop Advisor — Demo")

# load model & encoder
MODEL = "/content/smartcrop/crop_model.pkl"
ENC = "/content/smartcrop/label_encoder.pkl"
clf = joblib.load(MODEL)
le = joblib.load(ENC)

# helpers (lighter versions)
def recommend_topk_ui(N,P,K,temperature,humidity,ph,rainfall):
    X = np.array([[N,P,K,temperature,humidity,ph,rainfall]])
    if hasattr(clf, "predict_proba"):
        probs = clf.predict_proba(X)[0]
        top_idx = np.argsort(probs)[::-1][:3]
        return [(le.inverse_transform([i])[0], float(probs[i])) for i in top_idx]
    else:
        p = clf.predict(X)[0]
        return [(le.inverse_transform([p])[0], None)]

def soil_from_ph(ph):
    try: phv=float(ph)
    except: return "Unknown"
    if phv<5.5: return "Acidic"
    if phv<=7.5: return "Neutral"
    return "Alkaline"

def get_pests_ui(crop, temp=None, hum=None):
    pest_map = {'rice':['rice blast','stem borer'],'maize':['fall armyworm'],'wheat':['rust','aphids'],'cotton':['bollworm']}
    res = pest_map.get(str(crop).lower(), [])
    try:
        if hum and temp and hum>80 and temp>20:
            res = res + ['High fungal risk (humid & warm)']
    except:
        pass
    return res if res else ['No major pests detected.']

def get_price_ui(crop, market_keyword=None):
    file = "/content/smartcrop/market_standardized.csv"
    if os.path.exists(file):
        try:
            mdf = pd.read_csv(file, low_memory=False)
            mdf.columns = [c.strip().lower().replace(" ","_") for c in mdf.columns]
            comm = next((c for c in mdf.columns if 'commodity' in c or 'crop' in c), None)
            price_col = next((c for c in mdf.columns if 'modal' in c or 'price' in c), None)
            if comm and price_col:
                mdf[comm] = mdf[comm].astype(str).str.lower()
                sel = mdf[mdf[comm].str.contains(str(crop).lower(), na=False)]
                if not sel.empty:
                    vals = pd.to_numeric(sel[price_col], errors='coerce').dropna()
                    if not vals.empty:
                        return float(vals.median())
        except:
            pass
    return None

with st.form("input"):
    c1,c2 = st.columns(2)
    with c1:
        city = st.text_input("Nearest city/market (optional)", "")
        N = st.number_input("Nitrogen (N)", 0, 200, 50)
        P = st.number_input("Phosphorus (P)", 0, 200, 30)
        K = st.number_input("Potassium (K)", 0, 300, 20)
        ph = st.number_input("Soil pH", 0.0, 14.0, 6.5, step=0.1)
    with c2:
        temp = st.number_input("Temperature (°C)", -10.0, 60.0, 25.0, step=0.5)
        hum = st.number_input("Humidity (%)", 0.0, 100.0, 70.0, step=1.0)
        rainfall = st.number_input("Recent Rainfall (mm)", 0, 500, 100)
        days = st.number_input("Days until harvest (approx)", 30, 365, 90)
    submitted = st.form_submit_button("Get Recommendation")

if submitted:
    top = recommend_topk_ui(N,P,K,temp,hum,ph,rainfall)
    st.subheader("Top crop recommendations")
    for crop,prob in top:
        if prob is not None:
            st.write(f"- **{crop}** (confidence {prob:.2f})")
        else:
            st.write(f"- **{crop}**")
    st.subheader("Soil type")
    st.write(soil_from_ph(ph))
    st.subheader("Pest alerts")
    pests = get_pests_ui(top[0][0], temp=temp, hum=hum)
    for pe in pests:
        st.write("- " + str(pe))
    st.subheader("Market price (approx)")
    price = get_price_ui(top[0][0], market_keyword=city)
    if price is not None:
        st.metric("Current price (₹/quintal)", f"₹{int(price)}")
        st.metric("Expected price at harvest (approx)", f"₹{int(price * (1 + 0.05 + random.random()*0.15))}")
    else:
        base = random.randint(1500,5000)
        st.write("No exact market record found — showing simulated price.")
        st.metric("Current price (simulated ₹/quintal)", f"₹{base}")
        st.metric("Expected price at harvest (simulated ₹/quintal)", f"₹{int(base * (1 + 0.05 + random.random()*0.15))}")

st.caption("Demo app: model trained on uploaded Crop_recommendation.csv. Replace market file for live prices.")
