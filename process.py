import simpy
import random
from entities import Incidente, Ambulancia, CamionBomberos, PatrullaPolicia

# Configuración inicial
distritos_madrid = ["Centro", "Arganzuela", "Retiro", "Salamanca", "Chamartín", "Tetuán", 
                    "Chamberí", "Fuencarral-El Pardo", "Moncloa", "Latina", "Carabanchel",
                    "Usera", "Puente de Vallecas", "Moratalaz", "Ciudad Lineal", "Hortaleza",
                    "Villaverde", "Villa de Vallecas", "Vicálvaro", "San Blas", "Barajas" ]
tipos_recursos = {
    "Incendio": ("Bomberos", CamionBomberos),
    "Accidente": ("Ambulancia", Ambulancia),
    "Robo": ("Policia", PatrullaPolicia)
}
limite_recursos = {d: {"Ambulancia": 3, "Bomberos": 3, "Policia": 3} for d in distritos_madrid}
lista_incidentes_esperando = []
resueltos = []

def formato_tiempo_min_seg(tiempo):
    minutos = int(tiempo)
    segundos = int((tiempo - minutos) * 60)
    return f"{minutos} minutos y {segundos} segundos"

def obtener_prioridad(incidente):
    return incidente.prioridad

def generar_incidentes(env, recursos, limite_recursos):
    id_incidente = 0
    while True:
        nuevos_incidentes = []
        cantidad = random.randint(2, 4)  # más de uno a la vez

        for _ in range(cantidad):
            tipo = random.choice(list(tipos_recursos.keys()))
            ubicacion = random.choice(distritos_madrid)
            prioridad = random.randint(1, 5)
            incidente = Incidente(env, id_incidente, tipo, ubicacion, prioridad)
            incidente.tiempo_creacion = env.now
            nuevos_incidentes.append(incidente)
            id_incidente += 1

        lista_incidentes_esperando.extend(nuevos_incidentes)
        procesar_incidentes(env, recursos, limite_recursos)

        yield env.timeout(random.uniform(2, 4))  # más natural

def procesar_incidentes(env, recursos, limite_recursos):
    incidentes_por_tipo = {"Incendio": [], "Accidente": [], "Robo": []}
    for incidente in lista_incidentes_esperando:
        incidentes_por_tipo[incidente.tipo].append(incidente)

    lista_incidentes_esperando.clear()

    for tipo, incidentes in incidentes_por_tipo.items():
        incidentes.sort(key=obtener_prioridad)
        tipo_recurso, clase_recurso = tipos_recursos[tipo]

        for incidente in incidentes:
            recurso_asignado = None
            for recurso in recursos:
                if isinstance(recurso, clase_recurso) and recurso.ubicacion == incidente.ubicacion and recurso.disponible:
                    if limite_recursos[incidente.ubicacion][tipo_recurso] > 0:
                        recurso_asignado = recurso
                        break

            if recurso_asignado:
                recurso_asignado.disponible = False
                limite_recursos[incidente.ubicacion][tipo_recurso] -= 1
                env.process(gestionar_asignacion(env, recurso_asignado, incidente, tipo_recurso, limite_recursos, recursos))
            else:
                print(f"\n🚨 Incidente: {tipo} en {incidente.ubicacion} (Prioridad {incidente.prioridad})")
                print(f"En espera. No hay recursos disponibles ({tipo_recurso}) en {incidente.ubicacion}")
                lista_incidentes_esperando.append(incidente)

def gestionar_asignacion(env, recurso, incidente, tipo_recurso, limite_recursos, recursos):
    yield env.process(recurso.asignar(incidente))

    recurso.disponible = True
    limite_recursos[incidente.ubicacion][tipo_recurso] += 1
    tiempo_resolucion = env.now - incidente.tiempo_creacion

    print(f"\n🚨 Incidente: {incidente.tipo} en {incidente.ubicacion} (Prioridad {incidente.prioridad})")
    print(f"{recurso.tipo} asignado en {incidente.ubicacion}")
    print(f"Tiempo de resolución: {formato_tiempo_min_seg(tiempo_resolucion)}")
    print(f"{recurso.tipo} disponible nuevamente en {incidente.ubicacion}")

    resueltos.append({
        "tipo": incidente.tipo,
        "ubicacion": incidente.ubicacion,
        "prioridad": incidente.prioridad,
        "recurso": recurso.tipo,
        "tiempo": tiempo_resolucion
    })

    procesar_incidentes(env, recursos, limite_recursos)

# Inicialización de entorno
env = simpy.Environment()
recursos = []

for distrito in distritos_madrid:
    for _ in range(3):
        recursos.append(Ambulancia(env, len(recursos), distrito, random.randint(1, 5)))
        recursos.append(CamionBomberos(env, len(recursos), distrito, random.randint(1, 5)))
        recursos.append(PatrullaPolicia(env, len(recursos), distrito, random.randint(1, 5)))

env.process(generar_incidentes(env, recursos, limite_recursos))
env.run(until=70)  # duración extendida
