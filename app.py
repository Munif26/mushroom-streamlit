

import streamlit as st
import pandas as pd
import joblib

# Load model dan label encoder
model = joblib.load('mushroom_rf_model.pkl')
label_encoders = joblib.load('label_encoders.pkl')

st.set_page_config(page_title="Prediksi Jamur 🍄", layout="centered", initial_sidebar_state="auto")

# Judul aplikasi
st.title("🍄 Prediksi Jamur: Apakah Beracun atau Dapat Dimakan?")
st.markdown("Masukkan ciri-ciri jamur di bawah ini untuk memprediksi klasifikasinya:")

# Keterangan fitur (tooltip)
keterangan_fitur = {
    'cap-shape': "f: datar (flat), x: cembung (convex), b: lonceng (bell), k: menonjol, s: cekung, c: kerucut",
    'cap-surface': "f: berserat, g: beralur, y: bersisik, s: halus",
    'cap-color': "b: buff, c: cinnamon, e: merah, g: abu-abu, n: coklat, p: pink, r: hijau, u: ungu, w: putih, y: kuning",
    'bruises': "t: ada memar (bruises), f: tidak ada",
    'odor': "a: almond, l: anise, c: creosote, y: amis, f: busuk, m: apek, n: tidak berbau, p: menyengat, s: pedas",
    'gill-attachment': "a: menempel ke batang, f: bebas (tidak menempel)",
    'gill-spacing': "c: rapat, w: padat",
    'gill-size': "b: besar, n: kecil",
    'gill-color': "b: buff, e: merah, g: abu-abu, h: coklat tua, k: hitam, n: coklat, o: oranye, p: pink, r: hijau, u: ungu, w: putih, y: kuning",
    'stalk-shape': "e: membesar di bawah, t: meruncing",
    'stalk-root': "b: berbonggol, c: tongkat, e: sama besar, r: berakar",
    'stalk-surface-above-ring': "f: berserat, k: sutra, s: halus, y: bersisik",
    'stalk-surface-below-ring': "f: berserat, k: sutra, s: halus, y: bersisik",
    'stalk-color-above-ring': "b: buff, c: cinnamon, e: merah, g: abu-abu, n: coklat, o: oranye, p: pink, w: putih, y: kuning",
    'stalk-color-below-ring': "sama seperti atas",
    'veil-color': "n: coklat, o: oranye, w: putih, y: kuning",
    'ring-number': "n: tidak ada, o: satu, t: dua",
    'ring-type': "e: mudah hilang, f: melebar, l: besar, n: tidak ada, p: menggantung",
    'spore-print-color': "k: hitam, n: coklat, b: buff, h: coklat tua, r: hijau, o: oranye, u: ungu, w: putih, y: kuning",
    'population': "a: banyak, c: berkerumun, n: sangat banyak, s: tersebar, v: beberapa, y: sendirian",
    'habitat': "g: rumput, l: daun, m: padang rumput, p: jalan, u: kota, w: sampah, d: hutan"
}

# Urutan fitur
fitur_input = [
    'cap-shape', 'cap-surface', 'cap-color', 'bruises', 'odor',
    'gill-attachment', 'gill-spacing', 'gill-size', 'gill-color',
    'stalk-shape', 'stalk-root', 'stalk-surface-above-ring', 'stalk-surface-below-ring',
    'stalk-color-above-ring', 'stalk-color-below-ring', 'veil-color',
    'ring-number', 'ring-type', 'spore-print-color', 'population', 'habitat'
]

# Input user
input_data = {}
for fitur in fitur_input:
    opsi = label_encoders[fitur].classes_
    input_data[fitur] = st.selectbox(
        f"{fitur.replace('-', ' ').capitalize()}",
        options=opsi,
        help=keterangan_fitur.get(fitur, "Pilih nilai fitur")
    )

# Prediksi
if st.button("🔍 Prediksi Jamur"):
    # Convert input ke DataFrame dan encode
    input_df = pd.DataFrame([input_data])
    for kolom in input_df.columns:
        le = label_encoders[kolom]
        input_df[kolom] = le.transform(input_df[kolom])
    
    hasil = model.predict(input_df)[0]
    hasil_label = label_encoders['class'].inverse_transform([hasil])[0]

    # Tampilkan hasil
    if hasil_label == 'e':
        st.success("✅🍽️ Jamur ini **Dapat Dimakan (Edible)**.")
    else:
        st.error("⚠️☠️ Jamur ini **Beracun (Poisonous)**. Jangan dimakan!")
