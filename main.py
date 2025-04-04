
import simpy # Para crear y gestionar el entorno de simulación
import pandas as pd  # Para analizar y manipular los datos de simulación
import os # Para trabajar con rutas de archivos
from modules.methods import generador_incidentes # Función que genera los incidentes
from modules.methods import generador_incidentes, estadisticas # Estadisticas para guardar y analizar datos

if __name__ == "__main__":

    env = simpy.Environment()  #Creamos el entorno de simulación con Simpy
    env.process(generador_incidentes(env)) # Iniciamos el proceso de generación de incidentes dentro del entorno

    print("Bienvenido a la simulación de Sistema de Emergencias")
    duracion = input("Introduzca el número de unidades de tiempo de duración de la simulación: ")

    #Ejecutamos la simulación hasta que se cumpla el tiempo indicado
    env.run(until=duracion) # Se gestiona la duración total de la simulación

    # Guardamos las estadísticas generados durante la simulación en un archivo CSV
    estadisticas.guardar_csv()
    print("Datos de la simulación guardados en 'estadisticas_incidentes.csv'")

    # Cargamos el archivo CSV generado para analizarlo
    ruta_csv = os.path.join('estadisticas', 'estadisticas_incidentes.csv') #para mayor robustez y que siemopre funcione
    df = pd.read_csv(ruta_csv)

    opcion = input("¿Desea ver un resumen de la simulación? (Y/N)\n")
    if opcion.strip().lower() == 'y': #strip por si el usuario pone espacios los elimina, y lower ignora mayúsculas y minúsculas
        print("\nRESUMEN DE LA SIMULACIÓN:")
        print("Total de incidentes: ", len(df))
        print("Tipos de incidentes:\n", df['Tipo'].value_counts())
        print("Promedio de tiempo en espera:", round(df['Tiempo Espera'].mean(), 2)," uds de tiempo")
        print("Promedio de tiempo de resolución:", round(df['Tiempo Resolución'].mean(),2), "uds de tiempo")
    else: 
        print("No se mostrará el resumen")
        print("Hasta pronto")


