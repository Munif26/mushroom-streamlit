
import streamlit as st
import joblib

model = joblib.load('mushroom_rf_model.pkl')

st.title("🍄 Prediksi Jamur: Beracun atau Tidak?")

odor = st.selectbox("Bau Jamur", ['almond', 'creosote', 'foul', 'none', 'pungent', 'spicy', 'fishy', 'musty'])
gill_color = st.selectbox("Warna Insang", ['black', 'brown', 'buff', 'chocolate', 'gray', 'orange', 'pink', 'purple', 'red', 'white', 'yellow'])
spore_print_color = st.selectbox("Warna Cetakan Spora", ['black', 'brown', 'buff', 'chocolate', 'green', 'orange', 'purple', 'white', 'yellow'])

encoder_maps = {
    'odor': {'almond': 0, 'creosote': 1, 'foul': 2, 'none': 3, 'pungent': 4, 'spicy': 5, 'fishy': 6, 'musty': 7},
    'gill-color': {'black': 0, 'brown': 1, 'buff': 2, 'chocolate': 3, 'gray': 4, 'orange': 5, 'pink': 6, 'purple': 7, 'red': 8, 'white': 9, 'yellow': 10},
    'spore-print-color': {'black': 0, 'brown': 1, 'buff': 2, 'chocolate': 3, 'green': 4, 'orange': 5, 'purple': 6, 'white': 7, 'yellow': 8}
}

if st.button("Prediksi"):
    input_data = [
        encoder_maps['odor'][odor],
        encoder_maps['gill-color'][gill_color],
        encoder_maps['spore-print-color'][spore_print_color]
    ]
    result = model.predict([input_data])[0]
    st.success("☠️ Beracun" if result == 1 else "🍽️ Dapat Dimakan")
