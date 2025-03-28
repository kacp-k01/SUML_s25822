
import streamlit as st
import pickle
from datetime import datetime
import pathlib

startTime = datetime.now()

# Wczytanie modelu
filename = pathlib.Path("model.sv")
with open(filename, "rb") as file:
    model = pickle.load(file)

# Słowniki pomocnicze do wyświetlania opcji
sex_d = {0: "Kobieta", 1: "Mężczyzna"}
angina_d = {0: "Nie", 1: "Tak"}

def main():
    st.set_page_config(page_title="Predykcja Choroby Serca")
    overview = st.container()
    left, right = st.columns(2)
    prediction = st.container()

    st.image("https://upload.wikimedia.org/wikipedia/commons/6/6a/Coronary_artery_disease.png")

    with overview:
        st.title("Czy masz ryzyko choroby serca?")

    with left:
        age = st.slider("Wiek", min_value=18, max_value=100, value=40)
        sex = st.radio("Płeć", list(sex_d.keys()), format_func=lambda x: sex_d[x])
        resting_bp = st.slider("Ciśnienie krwi (RestingBP)", min_value=80, max_value=200, value=120)
        cholesterol = st.slider("Cholesterol", min_value=100, max_value=600, value=200)
        fasting_bs = st.radio("Cukier na czczo > 120 mg/dl", [0, 1], format_func=lambda x: "Tak" if x == 1 else "Nie")

    with right:
        max_hr = st.slider("Maksymalne tętno", min_value=60, max_value=210, value=150)
        oldpeak = st.slider("Oldpeak (ST depression)", min_value=0.0, max_value=7.0, step=0.1, value=1.0)
        exercise_angina = st.radio("Ból wieńcowy po wysiłku", list(angina_d.keys()), format_func=lambda x: angina_d[x])

        # Kategorie zakodowane jako one-hot: ChestPainType, RestingECG, ST_Slope
        chest_pain = st.selectbox("Typ bólu w klatce", ["ASY", "ATA", "NAP", "TA"])
        ecg = st.selectbox("Wynik EKG", ["Normal", "ST", "LVH"])
        st_slope = st.selectbox("Nachylenie ST", ["Up", "Flat", "Down"])

    # One-hot encoding dla kategorii
    chest_pain_vals = [0, 0, 0, 0]
    if chest_pain == "ASY":
        chest_pain_vals[0] = 1
    elif chest_pain == "ATA":
        chest_pain_vals[1] = 1
    elif chest_pain == "NAP":
        chest_pain_vals[2] = 1
    elif chest_pain == "TA":
        chest_pain_vals[3] = 1

    ecg_vals = [0, 0, 0]
    if ecg == "LVH":
        ecg_vals[0] = 1
    elif ecg == "Normal":
        ecg_vals[1] = 1
    elif ecg == "ST":
        ecg_vals[2] = 1

    st_vals = [0, 0, 0]
    if st_slope == "Down":
        st_vals[0] = 1
    elif st_slope == "Flat":
        st_vals[1] = 1
    elif st_slope == "Up":
        st_vals[2] = 1

    # Finalna tablica danych do predykcji
    data = [[
        age, sex, resting_bp, cholesterol, fasting_bs, max_hr,
        exercise_angina, oldpeak,
        *chest_pain_vals, *ecg_vals, *st_vals
    ]]

    prediction_result = model.predict(data)
    prediction_proba = model.predict_proba(data)

    with prediction:
        st.subheader("Czy ta osoba ma chorobę serca?")
        st.subheader("Tak" if prediction_result[0] == 1 else "Nie")
        st.write("Pewność predykcji: {0:.2f}%".format(prediction_proba[0][prediction_result[0]] * 100))


if __name__ == "__main__":
    main()
