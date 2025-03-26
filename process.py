import simpy
import random
from entities import Incidente, Ambulancia, CamionBomberos, PatrullaPolicia

'''Funciones'''

distritos_madrid = ["Centro", "Arganzuela", "Retiro", "Salamanca", "Chamartín", "Tetuán", 
                    "Chamberí", "Fuencarral-El Pardo", "Moncloa", "Latina", "Carabanchel",
                    "Usera", "Puente de Vallecas", "Moratalaz", "Ciudad Lineal", "Hortaleza",
                    "Villaverde", "Villa de Vallecas", "Vicálvaro", "San Blas", "Barajas" ]

def generar_incidentes(env, recursos):
    id_incidente = 0

    while True:
        tipo_incidente = random.choice(["Incendio", "Accidente", "Robo"])
        ubicacion = random.choice(distritos_madrid)
        prioridad = random.randint(1, 5)

        print(f"\n[{env.now}] 🚨 Nuevo incidente: {tipo_incidente} en {ubicacion} (Prioridad {prioridad})")

        # Crear el objeto Incidente correctamente
        incidente = Incidente(env, id_incidente, tipo_incidente, ubicacion, prioridad)
        id_incidente += 1

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

        if recurso_asignado:
            print(f"[{env.now}] {recurso_asignado.tipo} asignado a {tipo_incidente} en {ubicacion}")
            env.process(recurso_asignado.asignar(incidente))
        else:
            print(f"[{env.now}] No hay recursos disponibles para {tipo_incidente}, incidente en espera...")

        yield env.timeout(random.randint(3, 6))


# Inicializamos el entorno de simulación
env = simpy.Environment()

# Crear recursos aleatoriamente distribuidos en los distritos
recursos = []
for i in range(5): 
    id_incidente = i
    tipo = "ambulancia"
    prioridad = random.randint(1, 3)
    recursos.append(Ambulancia(env, id_incidente, random.choice(distritos_madrid), prioridad))
 
for i in range(5):
    id_incidente = i + 5
    tipo = "bomberos"
    prioridad = random.randint(1, 3)
    recursos.append(CamionBomberos(env, id_incidente,  random.choice(distritos_madrid), prioridad))

for i in range(5):
    id_incidente = i + 10
    tipo = "policía"
    prioridad = random.randint(1, 3)
    recursos.append(PatrullaPolicia(env, id_incidente, random.choice(distritos_madrid), prioridad))


# Iniciar la simulación
env.process(generar_incidentes(env,recursos))

# Ejecutar la simulación por 30 unidades de tiempo
env.run(until=30)
