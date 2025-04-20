# main.py (modificado para usar APIConnector)
import streamlit as st
import pandas as pd
from data_loader import DataLoader
from api_connector import APIConnector  # Importa la clase APIConnector

MARKDOWN_PATH = 'data/data_description.md'

# Configuración de la página de Streamlit
st.set_page_config(page_title="Análisis de Violencia Familiar", layout="wide")
st.title("Análisis de Reportes de Violencia Familiar")

# --- Sección para cargar datos ---
st.subheader("Carga de Datos")

# Opción para cargar desde CSV local o desde la API
data_source = st.radio("Seleccionar fuente de datos:", ("Archivo CSV Local", "API de Datos Abiertos"))

if data_source == "Archivo CSV Local":
    DATA_PATH = 'data/dataFrame_violencia.csv'  # Ajusta la ruta
    data_loader = DataLoader(DATA_PATH)
    df = data_loader.load_data()
elif data_source == "API de Datos Abiertos":
    API_URL = "https://www.datos.gov.co/api/odata/v4/x783-krje"
    api_connector = APIConnector(API_URL)
    json_data = api_connector.fetch_data()
    if json_data:
        records = api_connector.process_json_data(json_data)
        if records:
            df = api_connector.create_dataframe(records)
            if df is not None:
                # Ahora guardamos el DataFrame localmente y luego lo cargamos con DataLoader
                FILE_PATH_API_DATA = 'data/violencia_familiar_api.csv'
                api_connector.save_to_csv(df, FILE_PATH_API_DATA)
                data_loader = DataLoader(FILE_PATH_API_DATA)
                df = data_loader.load_data()
            else:
                df = None
        else:
            df = None
    else:
        df = None

# # --- Resto del código para exploración y preprocesamiento ---
# if df is not None:
#     st.subheader("Exploración Inicial de los Datos")
#     # ... (el resto de tu código para mostrar información inicial, preprocesamiento, etc.) ...

# # Configuración de la página de Streamlit
# st.set_page_config(page_title="Análisis de Violencia Familiar", layout="wide")
# st.title("Análisis de Reportes de Violencia Familiar")

# # Ruta al archivo de datos y al archivo Markdown
# DATA_PATH = 'add/dataFrame.csv' 
# #           
# #           From https://www.datos.gov.co/api/odata/v4/x783-krje -> add/dataFrame.csv
# #           https://www.datos.gov.co/resource/x783-krje.csv
# MARKDOWN_PATH = 'data/data_description.md'

# # Crear una instancia de la clase DataLoader
# data_loader = DataLoader(DATA_PATH)

# # Cargar los datos
# df = data_loader.load_data()

# Mostrar información básica y el Markdown (como antes)
if df is not None:
    st.subheader("Exploración Inicial de los Datos")
    st.write("Primeras 5 filas del DataFrame:")
    st.dataframe(df.head())

    st.write("\nInformación general del DataFrame:")
    st.write(f"Número de filas: {df.shape[0]}")
    st.write(f"Número de columnas: {df.shape[1]}")
    st.write("\nTipos de datos por columna:")
    st.write(df.dtypes)
    st.write("\nCantidad de valores no nulos por columna:")
    st.write(df.notna().sum())

    st.write("\nEstadísticas descriptivas de las columnas numéricas:")
    st.dataframe(df.describe())

    st.write("\nCantidad de valores únicos por columna:")
    for col in df.columns:
        st.write(f"- **{col}:** {df[col].nunique()} valores únicos")

    st.subheader("Información del Conjunto de Datos")
    try:
        with open(MARKDOWN_PATH, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        st.markdown(markdown_content)
    except FileNotFoundError:
        st.error(f"No se encontró el archivo: {MARKDOWN_PATH}")
    except Exception as e:
        st.error(f"Error al leer el archivo Markdown: {e}")

    # --- Inicio del Preprocesamiento ---
    st.subheader("Preprocesamiento de Datos")

    # Convertir columnas a datetime
    date_columns = ['fecha_de_apertura', 'fecha_ocurrencia_hechos']
    for col in date_columns:
        df = data_loader.convert_to_datetime(col)
        if df is not None and col in df.columns and pd.api.types.is_datetime64_any_dtype(df[col]):
            st.success(f"Columna '{col}' convertida a datetime.")

    # Extraer características de las fechas
    for col in date_columns:
        if df is not None and col in df.columns and pd.api.types.is_datetime64_any_dtype(df[col]):
            df = data_loader.extract_date_features(col)
            if df is not None:
                st.success(f"Características de fecha extraídas de '{col}'.")

    # Convertir 'hora_militar_ocurrencia_hechos' a numérico (manejar errores si hay no numéricos)
    df = data_loader.convert_to_numeric('hora_militar_ocurrencia_hechos', errors='coerce')
    if df is not None and 'hora_militar_ocurrencia_hechos' in df.columns:
        st.success("Columna 'hora_militar_ocurrencia_hechos' convertida a numérica (posibles NaN introducidos).")

    # Verificar valores faltantes
    missing_values = data_loader.check_missing_values()
    st.write("\nValores faltantes por columna:")
    st.write(missing_values)

    # Ejemplo de cómo manejar valores faltantes en una columna (ajústalo según tus necesidades)
    if 'edad_victima' in df.columns:
        df = data_loader.handle_missing_values('edad_victima', strategy='fill_mean')
        if df is not None:
            st.success("Valores faltantes en 'edad_victima' manejados (llenados con la media).")

    # Verificar duplicados
    duplicates = data_loader.check_duplicates()
    st.write(f"\nCantidad de filas duplicadas: {duplicates}")

    # Ejemplo de cómo manejar duplicados
    df = data_loader.handle_duplicates()
    if df is not None:
        st.success("Filas duplicadas eliminadas.")

    # Mostrar el DataFrame después del preprocesamiento (opcional)
    st.subheader("DataFrame después del Preprocesamiento (Primeras 5 filas)")
    st.dataframe(df.head())
    
    st.write("\nTipos de datos por columna después del Procesamiento:")
    st.write(df.dtypes)
    
    st.subheader("Análisis de Valores Faltantes y Eliminación de Columnas")
    st.write("\nCantidad de valores faltantes por columna:")
    st.write(missing_values)

    # Decidir qué columnas eliminar
    columns_to_drop = ['hora_militar_ocurrencia_hechos',
                       'fecha_ocurrencia_hechos_año',
                       'fecha_ocurrencia_hechos_mes',
                       'fecha_ocurrencia_hechos_dia_semana'] # Añade aquí las columnas que decidas eliminar

    # Eliminar las columnas
    if df is not None:
        df = data_loader.drop_columns(columns_to_drop)
        st.success(f"Columnas eliminadas: {columns_to_drop}")

        # Volver a verificar los valores faltantes después de la eliminación
        st.write("\nCantidad de valores faltantes por columna después de la eliminación:")
        st.write(df.isnull().sum())

        # Mostrar el DataFrame después de la eliminación (opcional)
        st.subheader("DataFrame después de la Eliminación de Columnas (Primeras 5 filas)")
        st.dataframe(df.head())
        
        st.write("\nTipos de datos por columna:")
        st.write(df.dtypes)
        st.write("\nCantidad de valores no nulos por columna:")
        st.write(df.notna().sum())