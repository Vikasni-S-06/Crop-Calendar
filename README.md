🌾 SmartCrop Advisor

Real-time Crop Recommendation System using Machine Learning & Streamlit

📌 Project Overview

SmartCrop Advisor is an intelligent web-based application that recommends suitable crops based on soil parameters and real-time weather conditions.
The system uses machine learning, map-based location selection, and live weather data to assist farmers, students, and agricultural planners in making informed crop decisions.

The application is developed using Streamlit and deployed on Streamlit Cloud for easy accessibility.

🚀 Live Application

🔗 Streamlit App Link:
👉 https://smartcrop-project.streamlit.app/

🎯 Key Features
🌍 Map-based location selection
🌡 Automatic real-time weather fetching (OpenWeather API)
🌱 Soil parameter input (N, P, K, pH)
🤖 Machine Learning-based crop recommendation
📊 Top-3 crop predictions with confidence scores
🧪 Soil type classification
☁️ Cloud-deployed using Streamlit
🧠 Machine Learning Model

Model Type: Supervised Classification
Training Dataset: Crop Recommendation Dataset
Features Used:
Nitrogen (N)
Phosphorus (P)
Potassium (K)
Soil pH
Temperature
Humidity
Rainfall
Model Serialization: Joblib
Output: Top 3 recommended crops with confidence probabilities
🏗️ System Architecture
User
 ↓
Streamlit UI
 ↓
Map Selection (Latitude & Longitude)
 ↓
OpenWeather API (Live Weather)
 ↓
ML Model Prediction
 ↓
Crop Recommendation Output
🧰 Technology Stack
Component	Technology
Frontend	Streamlit
Mapping	Folium
Machine Learning	Scikit-learn
Model Storage	Joblib
Weather API	OpenWeather
Deployment	Streamlit Cloud
Programming Language	Python
📂 Project Structure
SmartCrop-Advisor/
│
├── app.py                  # Main Streamlit application
├── crop_model.pkl          # Trained ML model
├── requirements.txt        # Dependencies
├── README.md               # Project documentation
└── data/                   # Dataset (if applicable)
⚙️ Installation & Local Setup
1️⃣ Clone the Repository
git clone (https://github.com/Vikasni-S-06/Crop-Calendar).git
cd smartcrop-advisor
2️⃣ Install Dependencies
pip install -r requirements.txt
3️⃣ Run the Streamlit App
streamlit run app.py
🔐 API Key Configuration (Important)

This project uses OpenWeather API.

For Local Use:

Add your API key directly in the code (for testing only).

For Streamlit Cloud:

Store the API key securely using Streamlit Secrets:

This ensures secure deployment without exposing credentials.

☁️ Deployment

The application is deployed using Streamlit Cloud, providing:

Browser-based access
No local setup for end users
Secure environment variable handling
🧪 Error Handling

The application gracefully handles:

Missing location selection
API failures
Invalid inputs
Model loading errors

User-friendly warnings are displayed instead of application crashes.

📈 Future Enhancements
Historical weather-based crop analysis
Pest and disease prediction
Crop yield estimation
Market price forecasting
Multilingual farmer support
Mobile-optimized UI
🏁 Conclusion

SmartCrop Advisor demonstrates the effective integration of:

Machine Learning
Real-time APIs
Geospatial inputs
Cloud-based deployment

to solve real-world agricultural decision-making challenges.
