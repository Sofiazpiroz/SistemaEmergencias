import simpy
import random
from entities import Incidente, Ambulancia, CamionBomberos, PatrullaPolicia

'''Funciones'''

distritos_madrid = ["Centro", "Arganzuela", "Retiro", "Salamanca", "Chamartín", "Tetuán", 
                    "Chamberí", "Fuencarral-El Pardo", "Moncloa", "Latina", "Carabanchel",
                    "Usera", "Puente de Vallecas", "Moratalaz", "Ciudad Lineal", "Hortaleza",
                    "Villaverde", "Villa de Vallecas", "Vicálvaro", "San Blas", "Barajas"]

# Límite de recursos por distrito (3 de cada tipo por distrito)
limite_recursos = {distrito: {"Ambulancia": 3, "Bomberos": 3, "Policia": 3} for distrito in distritos_madrid}

def generar_incidentes(env, recursos, limite_recursos):

    id_incidente=0

    while True:
        tipo_incidente = random.choice(["Incendio", "Accidente", "Robo"])
        ubicacion = random.choice(distritos_madrid)
        prioridad = random.randint(1, 5)

        print(f"\n[{env.now}] 🚨 Nuevo incidente: {tipo_incidente} en {ubicacion} (Prioridad {prioridad})")

        # Crear el objeto Incidente
        incidente = Incidente(env, id_incidente, tipo_incidente, ubicacion, prioridad)
        id_incidente += 1

        recurso_asignado = None
        tipo_recurso = None

        # Determinar el tipo de recurso necesario
        if tipo_incidente == "Incendio":
            tipo_recurso = "Bomberos"
        elif tipo_incidente == "Accidente":
            tipo_recurso = "Ambulancia"
        elif tipo_incidente == "Robo":
            tipo_recurso = "Policia"


        # Buscar recurso disponible del tipo correcto y en la ubicación correcta
        for recurso in recursos:
            if isinstance(recurso, CamionBomberos) and tipo_incidente == "Incendio" and recurso.disponible:
                recurso_asignado = recurso
                break
            elif isinstance(recurso, Ambulancia) and tipo_incidente == "Accidente" and recurso.disponible:
                recurso_asignado = recurso
                break
            elif isinstance(recurso, PatrullaPolicia) and tipo_incidente == "Robo" and recurso.disponible:
                break

        if recurso_asignado:
            limite_recursos[ubicacion][tipo_recurso] -= 1
            print(f"[{env.now}] {recurso_asignado.tipo} asignado a {tipo_incidente} en {ubicacion}")
            env.process(recurso_asignado.asignar(incidente))
        else:
            print(f"[{env.now}] No hay recursos disponibles para {tipo_incidente} en {ubicacion}, incidente en espera...")
            yield env.timeout(random.randint(3, 6))  # Esperamos antes de volver a intentar

        yield env.timeout(random.randint(3, 6)) 


# Inicializamos el entorno de simulación
env = simpy.Environment()

# Crear recursos aleatoriamente distribuidos en los distritos
recursos = []
for i in range(3):  # 3 ambulancias por distrito (según límite)
    for distrito in distritos_madrid:
        recursos.append(Ambulancia(env, len(recursos), distrito, random.randint(1, 5)))

for i in range(3):  # 3 camiones de bomberos por distrito
    for distrito in distritos_madrid:
        recursos.append(CamionBomberos(env, len(recursos), distrito, random.randint(1, 5)))

for i in range(3):  # 3 patrullas de policía por distrito
    for distrito in distritos_madrid:
        recursos.append(PatrullaPolicia(env, len(recursos), distrito, random.randint(1, 5)))

# Iniciar la simulación
env.process(generar_incidentes(env, recursos, limite_recursos))

# Ejecutar la simulación por 400 unidades de tiempo
env.run(until=400)
