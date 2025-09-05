import streamlit as st
from calc_app.pot_calc import run_calculation

st.set_page_config(
    page_title="Cálculo UNI",
    page_icon="📟",
    initial_sidebar_state="expanded",
)

maxNsd = st.number_input('Maximum vertical load ULS kN?', 0.00) * 1000
Vxd = st.number_input('Non-Seismic Longitudinal movement mm?', 0.00)

if st.button('Calcular'):
    run_calculation(maxNsd, Vxd)
