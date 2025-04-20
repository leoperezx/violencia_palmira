# api_connector.py
import requests
import pandas as pd
import json

class APIConnector:
    """
    Clase para conectar a una API y cargar datos en un DataFrame de Pandas.
    """
    def __init__(self, url):
        """
        Constructor de la clase APIConnector.

        Args:
            url (str): La URL de la API.
        """
        self.url = url

    def fetch_data(self):
        """
        Realiza la petición a la API y devuelve la respuesta en formato JSON.

        Returns:
            dict: El diccionario JSON de la respuesta de la API, o None si hay un error.
        """
        try:
            response = requests.get(self.url)
            response.raise_for_status()  # Lanza una excepción para códigos de error HTTP
            data = response.json()
            print(f"Datos obtenidos exitosamente de: {self.url}")
            return data
        except requests.exceptions.RequestException as e:
            print(f"Error al conectar o obtener datos de la API: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error al decodificar la respuesta JSON: {e}")
            return None

    def process_json_data(self, json_data, key_for_records="value"):
        """
        Procesa los datos JSON para extraer la lista de registros.

        Args:
            json_data (dict): El diccionario JSON obtenido de la API.
            key_for_records (str, optional): La clave que contiene la lista de registros.
                                             Por defecto es "value".

        Returns:
            list: La lista de registros, o None si la clave no se encuentra.
        """
        if json_data and key_for_records in json_data:
            records = json_data[key_for_records]
            print(f"Se encontraron {len(records)} registros.")
            return records
        else:
            print(f"Error: La clave '{key_for_records}' no se encontró en los datos JSON.")
            return None

    def create_dataframe(self, records):
        """
        Crea un DataFrame de Pandas a partir de una lista de registros.

        Args:
            records (list): La lista de registros (diccionarios).

        Returns:
            pandas.DataFrame: El DataFrame creado, o None si no hay registros.
        """
        if records:
            df = pd.DataFrame(records)
            print("DataFrame creado exitosamente.")
            print("Información del DataFrame:")
            df.info()
            return df
        else:
            print("No se proporcionaron registros para crear el DataFrame.")
            return None

    def save_to_csv(self, dataframe, file_path='dataFrame.csv', index=False):
        """
        Guarda el DataFrame a un archivo CSV.

        Args:
            dataframe (pandas.DataFrame): El DataFrame a guardar.
            file_path (str, optional): La ruta del archivo CSV. Por defecto es 'dataFrame.csv'.
            index (bool, optional): Indica si se debe escribir el índice del DataFrame. Por defecto es False.
        """
        if dataframe is not None:
            try:
                dataframe.to_csv(file_path, index=index, encoding='utf-8')
                print(f"DataFrame guardado exitosamente en: {file_path}")
            except Exception as e:
                print(f"Error al guardar el DataFrame a CSV: {e}")
        else:
            print("No hay DataFrame para guardar.")

# # Ejemplo de cómo usar la clase (esto se puede probar aquí o en otro script)
# if __name__ == "__main__":
#     api_url = "https://www.datos.gov.co/api/odata/v4/x783-krje"
#     connector = APIConnector(api_url)
#     json_data = connector.fetch_data()
#     if json_data:
#         records = connector.process_json_data(json_data)
#         if records:
#             df = connector.create_dataframe(records)
#             if df is not None:
#                 connector.save_to_csv(df, 'data/violencia_familiar_palmira.csv') # Guarda en la carpeta data