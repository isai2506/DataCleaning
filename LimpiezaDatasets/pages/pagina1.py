import streamlit as st
import login
import pandas as pd

login.generarLogin()
if 'usuario' in st.session_state:
    st.title('Limpieza KELQ')

def clean_dataset_kelq(file_path, skiprows=14):
    # Leer el archivo
    df = pd.read_excel(file_path, skiprows=skiprows, dtype={'# CLT': str})

    # Eliminar filas y columnas con datos vacíos. Eliminar las columnas 'FECHA DE BAJA' y 'BAJA'
    df = df.drop(columns=['FECHA DE BAJA', 'BAJA'])
    df = df.dropna(axis=1, how='all')
    df = df.dropna(axis=0, how='all')
    
    # Eliminar filas con más del 50% de datos vacíos
    threshold = 0.5 * len(df.columns)
    df = df.dropna(thresh=threshold, axis=0)
    
    # Eliminar columnas con más del 50% de datos vacíos
    threshold = 0.5 * len(df)
    df = df.dropna(thresh=threshold, axis=1)
    
    # Eliminar filas con al menos un dato vacío 
    df = df.dropna(axis=0, how='any')
    
    # Eliminar filas con los mismos datos del nombre de las columnas
    header = df.columns.tolist()
    rows_to_drop = df.index[df.apply(lambda x: all(x == header), axis=1)]
    df = df.drop(rows_to_drop)
    
    # Asignación de tipo de variable
    df = df.astype({
            '# CLT': 'string',
            'NOMBRE CLIENTE': 'string',
            'CREDITO': 'int',
            'PERIODICIDAD': 'string',
            'CAPITAL OTORGADO': 'float',
            'TASA INTERES': 'float',
            'PLAZO': 'int',
            'MONTO TABLA CAPITAL': 'float',
            'MONTO TABLA INTERES': 'float',
            'PAGO CAPITAL': 'float',
            'PAGO INTERES': 'float',
            'VENCIDO CAPITAL': 'float',
            'VENCIDO INTERES': 'float',
            'DIAS ATRASO': 'int',
            'PAGOS REALIZADOS': 'int',
            'PAGOS RESTANTES': 'int',
            'MONTO TABLA CAPITAL FINAL': 'float',
            'MONTO TABLA INTERES FINAL': 'float'
        })
    
    # Eliminar los datos de hora de las columnas de fecha
    for col in ['FECHA INICIO CREDITO', 'FECHA ULTIMO PAGO']:
        df['FECHA INICIO CREDITO'] = pd.to_datetime(df['FECHA INICIO CREDITO']).dt.date
        df['FECHA ULTIMO PAGO'] = pd.to_datetime(df['FECHA ULTIMO PAGO']).dt.date

    # Acomodar los datos de forma descendente
    df = df.sort_values(by='# CLT', ascending=True)

    return df


def main():
    st.write('Sube un archivo .xls para limpiarlo')

    uploaded_file = st.file_uploader("Elige un archivo", type=['xls'])

    if uploaded_file is not None:
        # Limpieza del dataset
        cleaned_df = clean_dataset_kelq(uploaded_file)

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
