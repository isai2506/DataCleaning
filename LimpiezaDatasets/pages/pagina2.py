import streamlit as st
import login
import pandas as pd 

login.generarLogin()
if 'usuario' in st.session_state:
    st.title('Limpieza AES')

def LimpiezaAes(file):
  # Leer archivo en formato csv y saltar las primeras 13 filas
  df = pd.read_excel(file, skiprows=15)

  # Eliminar columnas 'BAJA' y 'FECHA DE BAJA'
  df = df.drop(columns=['BAJA','FECHA DE BAJA'])

  # Eliminar filas que tengan todos los valores vacías
  df = df.dropna(axis=0, how='all')

  # FUNCION PARA ELIMINAR LAS FILAS QUE TENGAN LOS MISMOS DATOS QUE LOS NOMBRES DE LAS COLUMNAS
  # Función para verificar si una fila coincide con los nombres de las columnas
  def fila_coincide_con_columnas(fila, columnas):
      return all(fila[col] == col for col in columnas)

  # Obtenemos los nombres de las columnas
  columnas = df.columns

  # Eliminamos las filas que coinciden con los nombres de las columnas
  df = df[~df.apply(lambda fila: fila_coincide_con_columnas(fila, columnas), axis=1)]
  # Crear una columna nueva llamada 'COMPAÑIA' y llenar toda la fila con el valor

  # FUNCION PARA ELIMINAR LAS FULAS QUE TENGAN AL MENOS EL 30% DE CELDAS VACIAS
  umbral = int((1 - 0.30) * df.shape[1])

  # Eliminamos las filas que tienen al menos el 30% de las celdas vacías
  df = df.dropna(thresh=umbral)

  for col in ['FECHA INICIO CREDITO', 'FECHA ULTIMO PAGO']:
    df['FECHA INICIO CREDITO'] = pd.to_datetime(df['FECHA INICIO CREDITO']).dt.date
    df['FECHA ULTIMO PAGO'] = pd.to_datetime(df['FECHA ULTIMO PAGO']).dt.date

  return df


def main():
    st.write('Sube un archivo .xls para limpiarlo')

    uploaded_file = st.file_uploader("Elige un archivo", type=['xls'])

    if uploaded_file is not None:
        # Limpieza del dataset
        cleaned_df = LimpiezaAes(uploaded_file)

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