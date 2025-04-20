# data_loader.py
import pandas as pd

class DataLoader:
    """
    Clase para cargar y preprocesar datos.
    """
    def __init__(self, file_path):
        """
        Constructor de la clase DataLoader.

        Args:
            file_path (str): La ruta al archivo de datos.
        """
        self.file_path = file_path
        self.df = None

    def load_data(self):
        """
        Carga los datos desde el archivo especificado.

        Returns:
            pandas.DataFrame: El DataFrame con los datos cargados, o None si falla la carga.
        """
        try:
            self.df = pd.read_csv(self.file_path)  # Por ahora asumimos que es un CSV
            print(f"Datos cargados exitosamente desde: {self.file_path}")
            return self.df
        except FileNotFoundError:
            print(f"Error: El archivo '{self.file_path}' no fue encontrado.")
            return None
        except Exception as e:
            print(f"Error al cargar el archivo: {e}")
            return None

    def get_dataframe(self):
        """
        Devuelve el DataFrame cargado.

        Returns:
            pandas.DataFrame: El DataFrame cargado.
        """
        return self.df

    def convert_to_datetime(self, column):
        """
        Convierte una columna al tipo de dato datetime.

        Args:
            column (str): El nombre de la columna a convertir.

        Returns:
            pandas.DataFrame: El DataFrame con la columna convertida, o None si la columna no existe.
        """
        if column in self.df.columns:
            try:
                self.df[column] = pd.to_datetime(self.df[column], errors='coerce')
                print(f"Columna '{column}' convertida a datetime.")
                return self.df
            except Exception as e:
                print(f"Error al convertir la columna '{column}' a datetime: {e}")
                return None
        else:
            print(f"Error: La columna '{column}' no existe en el DataFrame.")
            return None

    def extract_date_features(self, date_column):
        """
        Extrae características útiles de una columna de fecha (mes, año, día de la semana).

        Args:
            date_column (str): El nombre de la columna de fecha.

        Returns:
            pandas.DataFrame: El DataFrame con las nuevas columnas añadidas, o None si la columna no existe.
        """
        if date_column in self.df.columns and pd.api.types.is_datetime64_any_dtype(self.df[date_column]):
            self.df[f'{date_column}_año'] = self.df[date_column].dt.year
            self.df[f'{date_column}_mes'] = self.df[date_column].dt.month
            self.df[f'{date_column}_dia_semana'] = self.df[date_column].dt.day_name()
            print(f"Características de fecha extraídas de la columna '{date_column}'.")
            return self.df
        else:
            print(f"Error: La columna '{date_column}' no es de tipo datetime o no existe.")
            return None

    def convert_to_numeric(self, column, errors='coerce'):
        """
        Convierte una columna a tipo numérico.

        Args:
            column (str): El nombre de la columna a convertir.
            errors (str, default='coerce'): Cómo manejar los errores de conversión ('raise', 'coerce', 'ignore').

        Returns:
            pandas.DataFrame: El DataFrame con la columna convertida, o None si la columna no existe.
        """
        if column in self.df.columns:
            try:
                self.df[column] = pd.to_numeric(self.df[column], errors=errors)
                print(f"Columna '{column}' convertida a numérica.")
                return self.df
            except Exception as e:
                print(f"Error al convertir la columna '{column}' a numérica: {e}")
                return None
        else:
            print(f"Error: La columna '{column}' no existe en el DataFrame.")
            return None

    def check_missing_values(self):
        """
        Verifica y muestra la cantidad de valores faltantes por columna.

        Returns:
            pandas.Series: Una Serie con la cantidad de valores faltantes por columna.
        """
        missing_values = self.df.isnull().sum()
        print("\nCantidad de valores faltantes por columna:")
        print(missing_values)
        return missing_values

    def handle_missing_values(self, column, strategy='drop'):
        """
        Maneja los valores faltantes en una columna específica.

        Args:
            column (str): El nombre de la columna donde manejar los valores faltantes.
            strategy (str, default='drop'): La estrategia para manejar los valores faltantes.
                                           Opciones: 'drop' (eliminar filas con NaN),
                                                    'fill_mean' (llenar con la media),
                                                    'fill_median' (llenar con la mediana),
                                                    'fill_value' (llenar con un valor específico).
            value (any, optional): El valor para llenar si strategy='fill_value'. Defaults to None.

        Returns:
            pandas.DataFrame: El DataFrame con los valores faltantes manejados, o None si la columna no existe.
        """
        if column in self.df.columns:
            if self.df[column].isnull().any():
                print(f"\nManejando valores faltantes en la columna '{column}' con estrategia '{strategy}'.")
                if strategy == 'drop':
                    self.df.dropna(subset=[column], inplace=True)
                    print(f"Filas con valores faltantes en '{column}' eliminadas.")
                elif strategy == 'fill_mean' and pd.api.types.is_numeric_dtype(self.df[column]):
                    mean_value = self.df[column].mean()
                    self.df[column].fillna(mean_value, inplace=True)
                    print(f"Valores faltantes en '{column}' llenados con la media ({mean_value:.2f}).")
                elif strategy == 'fill_median' and pd.api.types.is_numeric_dtype(self.df[column]):
                    median_value = self.df[column].median()
                    self.df[column].fillna(median_value, inplace=True)
                    print(f"Valores faltantes en '{column}' llenados con la mediana ({median_value:.2f}).")
                elif strategy == 'fill_value' and 'value' in locals():
                    self.df[column].fillna(value, inplace=True)
                    print(f"Valores faltantes en '{column}' llenados con el valor: {value}.")
                else:
                    print(f"Estrategia '{strategy}' no válida o no aplicable a la columna '{column}'.")
                return self.df
            else:
                print(f"No hay valores faltantes en la columna '{column}'.")
                return self.df
        else:
            print(f"Error: La columna '{column}' no existe en el DataFrame.")
            return None

    def check_duplicates(self):
        """
        Verifica y muestra la cantidad de filas duplicadas.

        Returns:
            int: La cantidad de filas duplicadas.
        """
        duplicates = self.df.duplicated().sum()
        print(f"\nCantidad de filas duplicadas: {duplicates}")
        return duplicates

    def handle_duplicates(self, strategy='drop'):
        """
        Maneja las filas duplicadas.

        Args:
            strategy (str, default='drop'): La estrategia para manejar los duplicados.
                                           Opciones: 'drop' (eliminar filas duplicadas).
        Returns:
            pandas.DataFrame: El DataFrame con los duplicados manejados.
        """
        if strategy == 'drop':
            initial_rows = len(self.df)
            self.df.drop_duplicates(inplace=True)
            print(f"Filas duplicadas eliminadas. Inicialmente {initial_rows}, ahora {len(self.df)} filas.")
            return self.df
        else:
            print(f"Estrategia '{strategy}' no válida para manejar duplicados.")
            return self.df
    
    def drop_columns(self, columns_to_drop):
        """
        Elimina una lista de columnas del DataFrame.

        Args:
            columns_to_drop (list): Una lista de nombres de las columnas a eliminar.

        Returns:
            pandas.DataFrame: El DataFrame con las columnas especificadas eliminadas,
                              o el DataFrame original si alguna columna no existe.
        """
        initial_columns = self.df.columns.tolist()
        self.df.drop(columns=[col for col in columns_to_drop if col in initial_columns], inplace=True, errors='ignore')
        dropped_columns = [col for col in columns_to_drop if col in initial_columns]
        if dropped_columns:
            print(f"Columnas eliminadas: {dropped_columns}")
        else:
            print("No se eliminó ninguna columna porque no se encontraron en el DataFrame.")
        return self.df
    # Podemos añadir más funciones de limpieza y preprocesamiento aquí