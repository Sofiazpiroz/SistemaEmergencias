import random
import simpy
from modules.models import Incidente
from modules.config import cola_incidentes, tipo_recurso, ubicaciones, recursos
from estadisticas.stats import Estadisticas  # Importar estadísticas


estadisticas = Estadisticas()  # Crear objeto para registrar datos

# Generador de incidentes
def generador_incidentes(env):
    id_incidente = 1
    while True:
        yield env.timeout(random.randint(1, 2))  # Generar incidentes cada 1-3 unidades de tiempo
        
        nuevo_incidente = Incidente(
            id=id_incidente,
            tipo=random.choice(list(tipo_recurso.keys())),
            prioridad=random.randint(1, 3),
            ubicacion=random.choice(ubicaciones)
        )
        nuevo_incidente.tiempo_creacion = env.now # Registrar tiempo de creación del incidente

        print(f"[{env.now}]: 🆕 Incidente {id_incidente} ({nuevo_incidente.tipo}) , Prioridad {nuevo_incidente.prioridad} , Ubicación: {nuevo_incidente.ubicacion}")
        cola_incidentes.append(nuevo_incidente)
        id_incidente += 1

        procesar_cola(env)

# Procesar la cola de incidentes
def procesar_cola(env):
    cola_ordenada = sorted(cola_incidentes, key=lambda x: x.prioridad) #Ordena la cola en funcion de la prioridad

    for incidente in cola_ordenada:
        recurso_necesario = tipo_recurso[incidente.tipo]

        for recurso in recursos:
            if recurso.tipo == recurso_necesario and recurso.disponible:
                recurso.disponible = False
                cola_incidentes.remove(incidente)

                tiempo_espera = env.now - incidente.tiempo_creacion  # Calcular tiempo de espera y luego se lo paso con env.process al csv

                print(f"[{env.now}]: 🚨 Asignado {recurso.tipo} a incidente {incidente.id} en {incidente.ubicacion}")

                env.process(atender_incidente(env, recurso, incidente, tiempo_espera)) # le he metido tiempo de espera para el csv
                break
        else:
            print(f"[{env.now}]: ⏳ Incidente {incidente.id} ({incidente.tipo}) en espera, no hay recursos disponibles...")

# Atención de incidentes
def atender_incidente(env, recurso, incidente, tiempo_espera):
    # Simulación de tiempos realistas y variados por tipo
    if incidente.tipo == "Incendio":
            tiempo_atencion = 2
    elif incidente.tipo == "Accidente":
            tiempo_atencion = 3
    elif incidente.tipo == "Robo":
            tiempo_atencion = 4
    else:
            tiempo_atencion = 1
        
    yield env.timeout(tiempo_atencion)

    tiempo_total_resolucion = env.now - incidente.tiempo_creacion  # Calcular tiempo de resolución
    recurso.disponible = True

    print(f"[{env.now}]: ✅ Incidente {incidente.id} resuelto en {env.now - incidente.tiempo_creacion} unidades de tiempo")
    
    # Guardar datos en estadísticas
    estadisticas.agregar_datos(
        id_incidente=incidente.id,
        tipo=incidente.tipo,
        prioridad=incidente.prioridad,
        ubicacion=incidente.ubicacion,
        tiempo_espera=tiempo_espera,
        tiempo_resolucion = tiempo_total_resolucion,
        recurso_asignado=recurso.tipo
    )

    procesar_cola(env)

