# Análisis de Reportes de Violencia Familiar en Palmira

Este proyecto tiene como objetivo analizar una base de datos de reportes de violencia familiar en el municipio de Palmira, Valle del Cauca, utilizando Python y las librerías Pandas, Plotly Express y Streamlit.

## Estado Actual del Proyecto

Actualmente, el proyecto ha avanzado en las siguientes etapas:

1. **Carga de Datos:**
    * Se ha implementado una clase `DataLoader` en el archivo `data_loader.py` para cargar datos desde un archivo CSV.
    * Se ha integrado una opción en la aplicación Streamlit (a través de la clase `APIConnector` en `api_connector.py`) para cargar datos directamente desde la API de Datos Abiertos de Colombia (enlace a la API: [https://www.datos.gov.co/api/odata/v4/x783-krje](https://www.datos.gov.co/api/odata/v4/x783-krje)). Los datos descargados de la API se guardan localmente como un archivo CSV.

2. **Exploración Inicial de los Datos:**
    * En la página principal de la aplicación Streamlit (`main.py`), se muestra información básica del DataFrame cargado, incluyendo las primeras filas, información general, estadísticas descriptivas y la cantidad de valores únicos por columna.
    * Se incluye la visualización de información sobre el conjunto de datos desde un archivo `data_description.md`.

3. **Limpieza y Preprocesamiento de Datos:**
    * Se han añadido funciones a la clase `DataLoader` para realizar tareas de limpieza y preprocesamiento:
        * Conversión de columnas a tipo datetime.
        * Extracción de características de fecha (año, mes, día de la semana) para la columna 'fecha\_de\_apertura'.
        * Conversión de la columna 'hora\_militar\_ocurrencia\_hechos' a tipo numérico.
        * Verificación y manejo de valores faltantes (se muestra la cantidad por columna y se incluye un ejemplo de cómo llenarlos o eliminarlos).
        * Verificación y eliminación de filas duplicadas.
        * Eliminación de columnas con una alta cantidad de valores faltantes ('hora\_militar\_ocurrencia\_hechos', 'fecha\_ocurrencia\_hechos\_año', 'fecha\_ocurrencia\_hechos\_mes', 'fecha\_ocurrencia\_hechos\_dia\_semana'). Se mantiene la columna 'fecha\_ocurrencia\_hechos' a pesar de tener faltantes.

## Estructura del Proyecto

```Text
El proyecto se organiza en los siguientes archivos y carpetas:

violencia_familiar_analisis/
├── main.py           # Archivo principal para ejecutar la aplicación Streamlit
├── data_loader.py    # Contiene la clase DataLoader para cargar y preprocesar datos
├── api_connector.py  # Contiene la clase APIConnector para obtener datos de la API
├── visualizations.py # (En desarrollo) Contendrá funciones para crear visualizaciones con Plotly Express
├── utils.py          # (Opcional) Podría contener funciones utilitarias
├── data/             # Carpeta para almacenar el archivo de datos (dataFrame.csv o el descargado de la API)
└── README.md         # Este archivo
```

## Próximos Pasos

Los siguientes pasos planeados para el proyecto son:

* Crear el archivo `visualizations.py` y desarrollar visualizaciones exploratorias utilizando Plotly Express para entender patrones en los datos (por ejemplo, distribución de tipos de violencia, tendencias temporales, características de las víctimas y agresores).
* Integrar estas visualizaciones en la aplicación Streamlit para hacerla interactiva.
* Continuar con el preprocesamiento de datos según sea necesario para el análisis.
* Potencialmente, explorar la creación de dashboards o análisis más profundos basados en las visualizaciones.

## Cómo Ejecutar la Aplicación

1. Asegúrate de tener Python instalado en tu sistema.
2. Instala las librerías necesarias:

    ```bash
    pip install pandas streamlit requests plotly-express
    ```

3. Navega al directorio raíz del proyecto (`violencia_familiar_analisis/`) en tu terminal.
4. Ejecuta la aplicación Streamlit:

    ```bash
    streamlit run main.py
    ```
