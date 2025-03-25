import simpy
import random
from entities import Incidente, Ambulancia, CamionBomberos, PatrullaPolicia

'''Funciones'''

distritos_madrid = ["Centro", "Arganzuela", "Retiro", "Salamanca", "Chamartín", "Tetuán", 
                    "Chamberí", "Fuencarral-El Pardo", "Moncloa", "Latina", "Carabanchel",
                    "Usera", "Puente de Vallecas", "Moratalaz", "Ciudad Lineal", "Hortaleza",
                    "Villaverde", "Villa de Vallecas", "Vicálvaro", "San Blas", "Barajas" ]

def generar_incidentes(env, incidente, recursos):

    incidente_id = 1
    while True:
        # Creamos un nuevo incidente
        tipo_incidente = random.choice(["Incendio", "Accidente", "Robo"])
        ubicacion = random.choice(distritos_madrid)
        prioridad = random.randint(1, 5)  # 1 = menos urgente , 5 = más urgente
        
        print(f"\n[{env.now}] U0001F6A8 Nuevo incidente: {tipo_incidente} en {ubicacion} (Prioridad {prioridad})")

        # Buscamos un recurso adecuado y disponible
        recurso_asignado = None

        if tipo_incidente == "Incendio":
            for recurso in recursos:
                if isinstance(recurso, CamionBomberos) and recurso.disponible:
                    recurso_asignado = recurso
                    break

        elif tipo_incidente == "Accidente":
            for recurso in recursos:
                if isinstance(recurso, Ambulancia) and recurso.disponible:
                    recurso_asignado = recurso
                    break

        elif tipo_incidente == "Robo":
            for recurso in recursos:
                if isinstance(recurso, PatrullaPolicia) and recurso.disponible:
                    recurso_asignado = recurso
                    break
        
        # Asignamos un recurso si hay disponibilidad
        if recurso_asignado:
            print(f"[{env.now}] U00002705 {recurso_asignado.tipo} asignado a {tipo_incidente} en {ubicacion}")
            env.process(recurso_asignado.asignar(tipo_incidente))  # Simulación de asignación
        else:
            print(f"[{env.now}] U0000274C No hay recursos disponibles para {tipo_incidente}, incidente en espera.")

        # Esperar un tiempo antes de generar otro incidente
        yield env.timeout(random.randint(3, 6))  # Simula tiempo entre incidentes

# Inicialización del entorno de simulación
env = simpy.Environment()

# Crear recursos aleatoriamente distribuidos en los distritos
recursos = [
    Ambulancia(env, random.choice(distritos_madrid)) for _ in range(5)] + [ 
        CamionBomberos(env, random.choice(distritos_madrid)) for _ in range(5)
] + [
    PatrullaPolicia(env, random.choice(distritos_madrid)) for _ in range(5)
]

# Iniciar la simulación
env.process(generar_incidentes(env,recursos))

# Ejecutar la simulación por 30 unidades de tiempo
env.run(until=30)
