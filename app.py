

import streamlit as st
import joblib
import numpy as np

st.set_page_config(page_title="Prediksi Jamur", page_icon="🍄", layout="centered")

# Load model
model = joblib.load('mushroom_rf_model1.pkl')

st.title("🍄 Prediksi Jamur: Apakah Beracun atau Dapat Dimakan?")
st.markdown("Masukkan ciri-ciri jamur di bawah ini untuk memprediksi klasifikasinya:")

# ===========================
# Dictionary pilihan fitur
# ===========================

cap_shape_options = {
    'b': 'Bell (b) - Lonceng',
    'c': 'Conical (c) - Kerucut',
    'x': 'Convex (x) - Cembung',
    'f': 'Flat (f) - Datar',
    'k': 'Knobbed (k) - Bertonjolan',
    's': 'Sunken (s) - Cekung'
}

cap_surface_options = {
    'f': 'Fibrous (f) - Berserat',
    'g': 'Grooves (g) - Beralur',
    'y': 'Scaly (y) - Bersisik',
    's': 'Smooth (s) - Halus'
}

cap_color_options = {
    'n': 'Brown (n) - Cokelat',
    'b': 'Buff (b) - Krem',
    'c': 'Cinnamon (c) - Kayu manis',
    'g': 'Gray (g) - Abu-abu',
    'r': 'Green (r) - Hijau',
    'p': 'Pink (p) - Merah muda',
    'u': 'Purple (u) - Ungu',
    'e': 'Red (e) - Merah',
    'w': 'White (w) - Putih',
    'y': 'Yellow (y) - Kuning'
}

bruises_options = {
    't': 'Yes (t) - Memar',
    'f': 'No (f) - Tidak memar'
}

odor_options = {
    'a': 'Almond (a) - Almond',
    'l': 'Anise (l) - Adas manis',
    'c': 'Creosote (c) - Bau tar',
    'y': 'Fishy (y) - Amis',
    'f': 'Foul (f) - Busuk',
    'm': 'Musty (m) - Apak',
    'n': 'None (n) - Tidak ada',
    'p': 'Pungent (p) - Menyengat',
    's': 'Spicy (s) - Pedas'
}

# ===========================
# Input dari user
# ===========================

cap_shape = st.selectbox("Bentuk Topi Jamur (cap-shape)", list(cap_shape_options.values()))
cap_surface = st.selectbox("Permukaan Topi Jamur (cap-surface)", list(cap_surface_options.values()))
cap_color = st.selectbox("Warna Topi Jamur (cap-color)", list(cap_color_options.values()))
bruises = st.selectbox("Apakah Jamur Memar? (bruises)", list(bruises_options.values()))
odor = st.selectbox("Bau Jamur (odor)", list(odor_options.values()))

# ===========================
# Konversi ke kode
# ===========================

def get_key(d, value):
    return [k for k, v in d.items() if v == value][0]

data_input = [
    get_key(cap_shape_options, cap_shape),
    get_key(cap_surface_options, cap_surface),
    get_key(cap_color_options, cap_color),
    get_key(bruises_options, bruises),
    get_key(odor_options, odor)
]

# Buat array lengkap (22 kolom) - kita isi dummy untuk yang tidak digunakan
# Posisi kolom berdasarkan urutan asli dataset (drop class)
# 0: cap-shape, 1: cap-surface, 2: cap-color, 3: bruises, 4: odor
# isi lainnya default 'x' (nanti akan di-labelencode ke nilai tetap saat training)

dummy_input = ['x'] * 22
dummy_input[0] = data_input[0]
dummy_input[1] = data_input[1]
dummy_input[2] = data_input[2]
dummy_input[3] = data_input[3]
dummy_input[4] = data_input[4]

# Gunakan LabelEncoder yang sudah dilatih
le = joblib.load('label_encoder.pkl')
encoded_input = le.transform(dummy_input).reshape(1, -1)

# ===========================
# Prediksi
# ===========================

if st.button("🔍 Prediksi Jamur"):
    pred = model.predict(encoded_input)[0]

    if pred == 0:
        st.success("✅ Hasil: **Jamur ini dapat dimakan (Edible)**")
    else:
        st.error("⚠️ Hasil: **Jamur ini beracun (Poisonous)**")
