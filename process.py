import simpy
import random
from entities import Incidente, Ambulancia, CamionBomberos, PatrullaPolicia

'''
Simulación de generación de incidentes y asignación de recursos
'''

def generar_incidentes(env, incidentes, recursos):
    incidente_id = 1
    while True:
        # Crear un nuevo incidente
        tipo_incidente = random.choice(["Incendio", "Accidente", "Robo"])
        ubicacion = random.choice(["Centro", "Zona Norte", "Zona Sur"])
        prioridad = random.randint(1, 3)  # 1 = más urgente, 3 = menos urgente
        
        incidente = Incidente(env, incidente_id, tipo_incidente, ubicacion, prioridad)
        print(f"[{env.now}] {incidente}")

        # Buscar un recurso disponible
        for recurso in recursos:
            if recurso.disponible:
                env.process(recurso.asignar(incidente))
                break
        else:
            print(f"[{env.now}] No hay recursos disponibles, incidente en espera.")

        incidente_id += 1
        yield env.timeout(random.randint(3, 6))  # Tiempo entre incidentes