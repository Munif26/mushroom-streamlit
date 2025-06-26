
import streamlit as st
import pandas as pd
import joblib

# Load model dan label encoder
model = joblib.load('mushroom_rf_model.pkl')
encoders = joblib.load('label_encoders.pkl')

features = list(encoders.keys())
features.remove('class')

st.title("🍄 Prediksi Jamur: Apakah Beracun atau Dapat Dimakan?")
st.markdown("Masukkan ciri-ciri jamur di bawah ini untuk memprediksi klasifikasinya:")

user_input = {}
for feature in features:
    categories = encoders[feature].classes_
    user_input[feature] = st.selectbox(feature, categories)

# Buat dataframe
input_df = pd.DataFrame([user_input])

# Encode input sesuai label encoder
for col in input_df.columns:
    input_df[col] = encoders[col].transform(input_df[col])

# Prediksi
if st.button("Prediksi"):
    pred = model.predict(input_df)[0]
    label = encoders['class'].inverse_transform([pred])[0]
    if label == 'e':
        st.success("🍽️ Jamur ini **AMAN dimakan (edible)**.")
    else:
        st.error("☠️ Jamur ini **BERACUN (poisonous)**!")
