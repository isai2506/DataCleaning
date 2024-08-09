import streamlit as st
import login as login

st.header('Limpieza de históricos GRUPO DINERCAP')
login.generarLogin()

if 'usuario' in st.session_state:
    st.subheader('Información página principal')
