import streamlit as st
import login
import pandas as pd

login.generarLogin()
if 'usuario' in st.session_state:
    st.title('Limpieza FTV')

def LimpiezaFTV(file):
  # Leer archivo
  dff = pd.read_excel(file, skiprows=16)

  # Nombre de columnas
  columns = ['# CLT', 'CREDITO', 'FECHA INICIO CREDITO',
        'PERIODICIDAD', 'CAPITAL OTORGADO', 'TASA INTERES', 'PLAZO',
        'MONTO TABLA CAPITAL', 'MONTO TABLA INTERES', 'FECHA ULTIMO PAGO',
        'PAGO CAPITAL', 'PAGO INTERES', 'VENCIDO CAPITAL', 'VENCIDO INTERES',
        'DIAS ATRASO', 'PAGOS REALIZADOS', 'PAGOS RESTANTES',
        'MONTO TABLA CAPITAL FINAL', 'MONTO TABLA INTERES FINAL', 'x', 'NOMBRE CLIENTE']

  # Asignar nombre de columnas
  dff.columns = columns

  # Eliminar filas que contengan todos los datos de fila vacíos
  dff = dff.dropna(axis=0, how='all')

  # Eliminar columnas 'NOMBRE CLIENTE' y 'X'
  dff = dff.drop(columns=['NOMBRE CLIENTE', 'x'])

  # Eliminar datos que contengan al menos un dato vacío
  dff = dff.dropna(axis=0, how='any')

  # Añadir nombres
  dff2 = pd.read_excel(file, skiprows=16)

  # Nombre de columnas
  columns = ['# CLT', 'CREDITO', 'FECHA INICIO CREDITO',
        'PERIODICIDAD', 'CAPITAL OTORGADO', 'TASA INTERES', 'PLAZO',
        'MONTO TABLA CAPITAL', 'MONTO TABLA INTERES', 'FECHA ULTIMO PAGO',
        'PAGO CAPITAL', 'PAGO INTERES', 'VENCIDO CAPITAL', 'VENCIDO INTERES',
        'DIAS ATRASO', 'PAGOS REALIZADOS', 'PAGOS RESTANTES',
        'MONTO TABLA CAPITAL FINAL', 'MONTO TABLA INTERES FINAL', 'x', 'NOMBRE CLIENTE']

  # Asignar nombre de columnas
  dff2.columns = columns

  # Extraer los nombres de clientes y # CLT del df original
  df_prueba = dff2[['FECHA INICIO CREDITO', 'PERIODICIDAD']]

  # Nombre de columnas a asignar
  columnas = ['# CLT', 'NOMBRE CLIENTE']

  # Asignar nombre de las columnas
  df_prueba.columns = columnas

  # Eliminar todas las filas que contengan al menos un dato vacío
  df_prueba = df_prueba.dropna(axis=0, how='any')

  # Eliminar datos que tenga la palabra 'MENSUAL' o 'PERIODICIDAD'
  df_prueba = df_prueba[~df_prueba['NOMBRE CLIENTE'].isin(['PERIODICIDAD', 'MENSUAL'])]

  # Eliminar los datos repetidos baasado en nombre
  df_prueba = df_prueba.drop_duplicates(subset='NOMBRE CLIENTE')

  dff_final = pd.merge(dff, df_prueba, how='inner', on='# CLT')

      # Eliminar los datos de hora de las columnas de fecha
  for col in ['FECHA INICIO CREDITO', 'FECHA ULTIMO PAGO']:
    dff_final['FECHA INICIO CREDITO'] = pd.to_datetime(dff_final['FECHA INICIO CREDITO']).dt.date
    dff_final['FECHA ULTIMO PAGO'] = pd.to_datetime(dff_final['FECHA ULTIMO PAGO']).dt.date

  return dff_final


def main():
    st.write('Sube un archivo .xls para limpiarlo')

    uploaded_file = st.file_uploader("Elige un archivo", type=['xls'])

    if uploaded_file is not None:
        # Limpieza del dataset
        cleaned_df = LimpiezaFTV(uploaded_file)

        # Mostrar el dataframe limpio
        st.write('Dataset Limpio:')
        st.dataframe(cleaned_df)

        # Descargar el archivo limpio
        st.download_button(label="Descargar Dataset Limpio",
                          data=cleaned_df.to_csv(index=False).encode('utf-8'),
                          file_name="dataset_limpio_aes.csv",
                          mime='text/csv')

if __name__ == "__main__":
    main()