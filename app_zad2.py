
import streamlit as st
import pickle
from datetime import datetime
import pathlib

startTime = datetime.now()

filename = pathlib.Path("model.sv")
with open(filename, "rb") as file:
    model = pickle.load(file)

sex_d = {0: "Kobieta", 1: "Mężczyzna"}
cp_d = {0: "ASY", 1: "ATA", 2: "NAP", 3: "TA"}
ecg_d = {0: "LVH", 1: "Normal", 2: "ST"}
angina_d = {0: "Nie", 1: "Tak"}
slope_d = {0: "Down", 1: "Flat", 2: "Up"}

def main():
    st.set_page_config(page_title="Predykcja Choroby Serca")
    overview = st.container()
    left, right = st.columns(2)
    prediction = st.container()

    st.image("https://dvl2h13awlxkt.cloudfront.net/assets/general-images/Knowledge/_1200x630_crop_center-center_82_none/Coronary-heart-disease.jpg?mtime=1657262027")

    with overview:
        st.title("Czy masz ryzyko choroby serca?")

    with left:
        sex_radio = st.radio("Płeć", list(sex_d.keys()), format_func=lambda x: sex_d[x])
        cp_radio = st.radio("Typ bólu w klatce piersiowej", list(cp_d.keys()), format_func=lambda x: cp_d[x])
        ecg_radio = st.radio("Wynik EKG", list(ecg_d.keys()), format_func=lambda x: ecg_d[x])
        angina_radio = st.radio("Ból wieńcowy po wysiłku", list(angina_d.keys()), format_func=lambda x: angina_d[x])
        slope_radio = st.radio("Nachylenie ST", list(slope_d.keys()), format_func=lambda x: slope_d[x])

    with right:
        age = st.slider("Wiek", min_value=18, max_value=100, value=40)
        resting_bp = st.slider("Ciśnienie spoczynkowe (RestingBP)", min_value=80, max_value=200, value=120)
        cholesterol = st.slider("Cholesterol", min_value=100, max_value=600, value=200)
        fasting_bs = st.radio("Cukier na czczo > 120 mg/dl", [0, 1], format_func=lambda x: "Tak" if x == 1 else "Nie")
        max_hr = st.slider("Maksymalne tętno (MaxHR)", min_value=60, max_value=210, value=150)
        oldpeak = st.slider("Oldpeak (obniżenie ST)", min_value=0.0, max_value=7.0, step=0.1, value=1.0)


    # One-hot encoding dla kategorii
    cp_vals = [1 if cp_radio == i else 0 for i in range(4)]
    ecg_vals = [1 if ecg_radio == i else 0 for i in range(3)]
    slope_vals = [1 if slope_radio == i else 0 for i in range(3)]

    # Finalna tablica danych do predykcji
    data = [[
        age, sex_radio, resting_bp, cholesterol, fasting_bs, max_hr,
        angina_radio, oldpeak,
        *cp_vals, *ecg_vals, *slope_vals
    ]]

    prediction_result = model.predict(data)
    prediction_proba = model.predict_proba(data)

    with prediction:
        st.subheader("Czy ta osoba ma chorobę serca?")
        st.subheader("Tak" if prediction_result[0] == 1 else "Nie")
        st.write("Pewność predykcji: {0:.2f}%".format(prediction_proba[0][prediction_result[0]] * 100))


if __name__ == "__main__":
    main()
