import simpy
import random
from entities import Incidente, Ambulancia, CamionBomberos, PatrullaPolicia

distritos_madrid = ["Centro", "Arganzuela", "Retiro", "Salamanca", "Chamartín", "Tetuán"]

limite_recursos = {distrito: {"Ambulancia": 2, "Bomberos": 2, "Policia": 2} for distrito in distritos_madrid}
lista_incidentes_esperando = []

# ✅ Redondeo bonito
def tiempo_redondeado_dos_decimales(tiempo):
    return f"{round(tiempo, 2)} minutos"

def obtener_prioridad(incidente):
    return incidente.prioridad

def generar_incidentes(env, recursos, limite_recursos):
    id_incidente = 0

    while True:
        nuevos_incidentes = []
        cantidad = random.randint(2, 4)

        for _ in range(cantidad):
            tipo = random.choice(["Incendio", "Accidente", "Robo"])
            ubicacion = random.choice(distritos_madrid)
            prioridad = random.randint(1, 5)
            incidente = Incidente(env, id_incidente, tipo, ubicacion, prioridad)
            nuevos_incidentes.append(incidente)
            id_incidente += 1
            print(f"🚨 Nuevo incidente: {tipo} en {ubicacion} (Prioridad {prioridad})")

        incidentes_totales = lista_incidentes_esperando + nuevos_incidentes
        incidentes_totales.sort(key=obtener_prioridad)
        lista_incidentes_esperando.clear()

        for incidente in incidentes_totales:
            tipo_recurso = None
            clase_recurso = None

            if incidente.tipo == "Incendio":
                tipo_recurso = "Bomberos"
                clase_recurso = CamionBomberos
            elif incidente.tipo == "Accidente":
                tipo_recurso = "Ambulancia"
                clase_recurso = Ambulancia
            elif incidente.tipo == "Robo":
                tipo_recurso = "Policia"
                clase_recurso = PatrullaPolicia

            recurso_asignado = None
            for recurso in recursos:
                if isinstance(recurso, clase_recurso) and recurso.ubicacion == incidente.ubicacion and recurso.disponible:
                    if limite_recursos[incidente.ubicacion][tipo_recurso] > 0:
                        recurso_asignado = recurso
                        break

            if recurso_asignado:
                print(f"{recurso_asignado.tipo} asignado a {incidente.tipo} en {incidente.ubicacion}")
                recurso_asignado.disponible = False  # 🚨 Marcar como ocupado
                limite_recursos[incidente.ubicacion][tipo_recurso] -= 1
                env.process(gestionar_asignacion(env, recurso_asignado, incidente, tipo_recurso, limite_recursos))
            else:
                print(f"🚨 Incidente {incidente.id_incidente}: {incidente.tipo} en {incidente.ubicacion} (Prioridad {incidente.prioridad}) está en espera. No hay recursos disponibles.")
                lista_incidentes_esperando.append(incidente)

        yield env.timeout(random.uniform(1, 4))

def gestionar_asignacion(env, recurso, incidente, tipo_recurso, limite_recursos):
    yield env.process(recurso.asignar(incidente))  # Se supone que aquí hay tiempo de atención
    recurso.disponible = True  # ✅ Liberamos el recurso al terminar
    limite_recursos[incidente.ubicacion][tipo_recurso] += 1
    print(f"{recurso.tipo} disponible nuevamente en {incidente.ubicacion} en {tiempo_redondeado_dos_decimales(env.now)}")
    print(f"{recurso.tipo} asignado a Incidente {incidente.id_incidente}: {incidente.tipo} en {incidente.ubicacion} (Prioridad {incidente.prioridad}) en {tiempo_redondeado_dos_decimales(env.now)}")

# Simulación
env = simpy.Environment()
recursos = []

for distrito in distritos_madrid:
    for _ in range(2):
        recursos.append(Ambulancia(env, len(recursos), distrito, random.randint(1, 5)))
        recursos.append(CamionBomberos(env, len(recursos), distrito, random.randint(1, 5)))
        recursos.append(PatrullaPolicia(env, len(recursos), distrito, random.randint(1, 5)))

env.process(generar_incidentes(env, recursos, limite_recursos))
env.run(until=30)


