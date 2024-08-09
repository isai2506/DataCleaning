import streamlit as st
import pandas as pd

# Validación simple de usuario y clave con un archivo csv

def validarUsuario(usuario,clave):    
    """Permite la validación de usuario y clave

    Args:
        usuario (str): usuario a validar
        clave (str): clave del usuario

    Returns:
        bool: True usuario valido, False usuario invalido
    """    
    dfusuarios = pd.read_csv('usuarios.csv')
    if len(dfusuarios[(dfusuarios['usuario']==usuario) & (dfusuarios['clave']==clave)])>0:
        return True
    else:
        return False

def generarMenu(usuario):
    with st.sidebar:
        dfusuarios = pd.read_csv('usuarios.csv')
        nombre = dfusuarios[dfusuarios['usuario'] == usuario]['nombre'].values[0]
        st.write(f"Hola **:blue-background[{nombre}]**")
        st.page_link("inicio.py", label="Inicio", icon=":material/home:")
        st.subheader("Tableros")
        st.page_link("pages/pagina1.py", label="Ventas", icon=":material/sell:")
        st.page_link("pages/pagina2.py", label="Compras", icon=":material/shopping_cart:")
        st.page_link("pages/pagina3.py", label="Personal", icon=":material/group:")
        
        btnSalir = st.button("Salir")
        if btnSalir:
            st.session_state.clear()
            st.experimental_js("window.location.reload()")  # Redirige al usuario después de cerrar sesión

def generarLogin():
    if 'usuario' in st.session_state:
        generarMenu(st.session_state['usuario'])
    else:
        with st.form('frmLogin'):
            parUsuario = st.text_input('Usuario')
            parPassword = st.text_input('Password', type='password')
            btnLogin = st.form_submit_button('Ingresar', type='primary')
            if btnLogin:
                if validarUsuario(parUsuario, parPassword):
                    st.session_state['usuario'] = parUsuario
                    st.experimental_js("window.location.reload()")  # Redirige después del login exitoso
                else:
                    st.error("Usuario o clave inválidos", icon=":material/gpp_maybe:")
                       