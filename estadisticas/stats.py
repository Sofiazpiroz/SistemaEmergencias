# Importamos las librerias necesarias como pandas para manejar estructuras de datos y os para trabajar con rutas de archivos y carpetas
import pandas as pd
import os #Para meter el archivo donde yo quiero

# La clase estadisticas se encarga de almacenar y guardar informacion de incidentes
class Estadisticas:
    def __init__(self):
        #Inicializamos la lista vacia donde se iran almacenando los accidentes
        self.datos = []
        self.directorio = "estadisticas"  
        self.archivo_csv = os.path.join(self.directorio, "incidentes.csv")  

# Este metodo lo utilzamos para agregar informacion de un nuevo incidente
    def agregar_datos(self, id_incidente: int, tipo: str, prioridad: int, 
                      ubicacion: str, tiempo_espera: float, tiempo_resolucion: float, 
                      recurso_asignado: str) -> None:
        """
        Agrega información sobre un incidente.

        Args:
            id_incidente (int): ID del incidente.
            tipo (str): Tipo de incidente.
            prioridad (int): Prioridad (1 = máxima).
            ubicacion (str): Ubicación del incidente.
            tiempo_espera (float): Tiempo desde la creación hasta la asignación del recurso.
            tiempo_resolucion (float): Tiempo desde la asignación hasta la resolución.
            recurso_asignado (str): Recurso asignado al incidente.
        """
    # Diccionario con la informacion de los incidentes 
        datos_incidente = {
            'ID Incidente': id_incidente,
            'Tipo': tipo,
            'Prioridad': prioridad,
            'Ubicación': ubicacion,
            'Tiempo Espera': tiempo_espera,
            'Tiempo Resolución': tiempo_resolucion,
            'Recurso Asignado': recurso_asignado
        }
        
        self.datos.append(datos_incidente)
# Convierte la lista de datos en un DF e pandas
    def a_dataframe(self):
        """Convierte los datos en un DataFrame de Pandas."""
        return pd.DataFrame(self.datos)
# Por ultimo utilizamos guardar_csv para guardar los datos en un archivo CSV
    def guardar_csv(self, nombre_archivo='estadisticas/estadisticas_incidentes.csv'):
        """Guarda los datos en un archivo CSV."""
        df = self.a_dataframe()
        df.to_csv(nombre_archivo, index=False)

