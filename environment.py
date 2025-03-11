
import simpy
from process import generar_incidentes
from entities import Ambulancia, CamionBomberos, PatrullaPolicia

'''
Inicialización del entorno de simulación de emergencias
'''

if __name__ == "_main_":
    env = simpy.Environment()

    # Crear recursos disponibles en la ciudad
    recursos = [
        Ambulancia(env, "Centro"),
        CamionBomberos(env, "Zona Norte"),
        PatrullaPolicia(env, "Zona Sur")
    ]

    # Iniciar el proceso de generación de incidentes
    env.process(generar_incidentes(env, [], recursos))

    # Ejecutar la simulación por 30 unidades de tiempo
    env.run(until=30)