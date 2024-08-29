import streamlit as st
import login
import pandas as pd

login.generarLogin()
if 'usuario' not in st.session_state:
    st.error("Por favor, inicia sesión para acceder a esta página.")
    st.stop()

st.title('Limpieza KELQ por Patron')

def clean_dataset_kelq_patron(file_path, skiprows=17):
  # Leer el archivo
  x = pd.read_excel(file_path)

  columns = ['# PAT', 'x', '# CLT',
          'NOMBRE CLIENTE', 'CREDITO', 'FECHA INICIO CREDITO', 'PERIODICIDAD',
          'CAPITAL OTORGADO', 'TASA INTERES', 'PLAZO', ' MONTO TABLA CAPITAL', 'MONTO TABLA INTERES',
          'FECHA ULTIMO PAGO', 'PAGO CAPITAL', 'PAGO INTERES', 'VENCIDO CAPITAL', 'VENCIDO INTERES', 
          'DIAS ATRASO', 'PAGOS REALIZADOS', 'PAGOS RESTANTES',
          'MONTO TABLA CAPITAL FINAL', 'MONTO TABLA INTERES FINAL']

  x.columns = columns

  threshold = 0.8 * x.shape[1]

  # Eliminar filas que tienen el 80% o más de sus valores vacíos
  df_cleaned = x.dropna(thresh=threshold)

  return df_cleaned


def main():
    st.write('Sube un archivo .xls para limpiarlo')

    uploaded_file = st.file_uploader("Elige un archivo", type=['xls'])

    if uploaded_file is not None:
        # Limpieza del dataset
        cleaned_df = clean_dataset_kelq_patron(uploaded_file)

        # Mostrar el dataframe limpio
        st.write('Dataset Limpio:')
        st.dataframe(cleaned_df)

        # Descargar el archivo limpio
        st.download_button(label="Descargar Dataset Limpio",
                          data=cleaned_df.to_csv(index=False).encode('utf-8'),
                          file_name="dataset_limpio_kelq.csv",
                          mime='text/csv')

if __name__ == "__main__":
    main()
