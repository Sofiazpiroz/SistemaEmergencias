import random # Genera valores aleatorios
import simpy # Simula eventos discretos
from modules.models import Incidente
from modules.config import cola_incidentes, tipo_recurso, ubicaciones, recursos
from estadisticas.stats import Estadisticas  # Importar estadísticas


estadisticas = Estadisticas()  # Crear objeto para registrar datos

# Generador de incidentes
def generador_incidentes(env):
    id_incidente = 1 # Es un contador de ID para cada incidente nuevo
    while True:
        yield env.timeout(random.randint(1, 2))  # Generar incidentes cada 1-2 unidades de tiempo
        # Creamos un nuevo incidente con atributos aleatorios 
        nuevo_incidente = Incidente(
            id=id_incidente,
            tipo=random.choice(list(tipo_recurso.keys())),
            prioridad=random.randint(1, 3),
            ubicacion=random.choice(ubicaciones)
        )
        nuevo_incidente.tiempo_creacion = env.now # Registrar tiempo de creación del incidente
        # Mostramos por consola que se ha creado un nuevo incidente
        print(f"[{env.now}]: 🆕 Incidente {id_incidente} ({nuevo_incidente.tipo}) , Prioridad {nuevo_incidente.prioridad} , Ubicación: {nuevo_incidente.ubicacion}")
        cola_incidentes.append(nuevo_incidente) # Añadimos el nuevo incidente a la cola
        id_incidente += 1 # Incrementamos el ID para el siguiente incidente

        procesar_cola(env)

# Procesar la cola de incidentes
def procesar_cola(env):
    cola_ordenada = sorted(cola_incidentes, key=lambda x: x.prioridad) #Ordena la cola en funcion de la prioridad
# Recorre los incidentes ordenados de manera que pueda asignar recursos
    for incidente in cola_ordenada:
        recurso_necesario = tipo_recurso[incidente.tipo] # Determina el recurso necesario para cada incidente
    # Determine si hay un recurso disponible del tipo necesario
        for recurso in recursos:
            if recurso.tipo == recurso_necesario and recurso.disponible:
                recurso.disponible = False # Marca el recruso como no disponible
                cola_incidentes.remove(incidente) # Elimina el incidente de la cola
            # Utilizamos tiempo_espera para calcular cuanto tiempo ha esperado el incidente desde su creacion
                tiempo_espera = env.now - incidente.tiempo_creacion  # Calcular tiempo de espera y luego se lo paso con env.process al csv

                print(f"[{env.now}]: 🚨 Asignado {recurso.tipo} a incidente {incidente.id} en {incidente.ubicacion}")
            # Inicia el proceso de atencion al incidente
                env.process(atender_incidente(env, recurso, incidente, tiempo_espera)) # le he metido tiempo de espera para el csv
                break
        else:
            print(f"[{env.now}]: ⏳ Incidente {incidente.id} ({incidente.tipo}) en espera, no hay recursos disponibles...")

# Simula la atencion de un incidente por parte de el respectivo recurso
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

