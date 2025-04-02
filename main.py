import simpy
import pandas as pd
import os
from modules.methods import generador_incidentes
from modules.methods import generador_incidentes, estadisticas


    
if __name__ == "__main__":
    env = simpy.Environment()
    env.process(generador_incidentes(env))
    print("Bienvenido a la simulación de Sistema de Emergencias")
    duracion = input("Introduzca el número de unidades de tiempo de duración de la simulación: ")
    env.run(until=duracion) #AQUI GESTIONAMOS LAS UNIDADES DE TIEMPO QUE DURA LA SIMULACION

    # Guardar estadísticas al finalizar la simulación
    estadisticas.guardar_csv()
    print("Datos de la simulación guardados en 'estadisticas_incidentes.csv'")

    ruta_csv = os.path.join('estadisticas', 'estadisticas_incidentes.csv') #para mayor robustez y que siemopre funcione
    df = pd.read_csv(ruta_csv)

    opcion = input("¿Desea ver un resumen de la simulación? (Y/N)\n")
    if opcion.strip().lower() == 'y': #strip por si el usuario pone espacios, y lower por si pone Y o y
        print("\nRESUMEN DE LA SIMULACIÓN:")
        print("Total de incidentes: ", len(df))
        print("Tipos de incidentes:\n", df['Tipo'].value_counts())
        print("Promedio de tiempo en espera:", round(df['Tiempo Espera'].mean(), 2)," uds de tiempo")
        print("Promedio de tiempo de resolución:", round(df['Tiempo Resolución'].mean(),2), "uds de tiempo")
    else: 
        print("No se mostrará el resumen")


