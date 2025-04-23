# Importamos la clase Recurso desde el modulo models
from modules.models import Recurso

# Lista de ubicaciones posibles donde pueden ocurrir incidentes
# Corresponde a los 21 distritos de la ciudad de Madrid
ubicaciones = ["Centro", "Arganzuela", "Retiro", "Salamanca", "Chamartín", "Tetuán", 
                "Chamberí", "Fuencarral-El Pardo", "Moncloa", "Latina", "Carabanchel",
                "Usera", "Puente de Vallecas", "Moratalaz", "Ciudad Lineal", "Hortaleza",
                "Villaverde", "Villa de Vallecas", "Vicálvaro", "San Blas", "Barajas" ]


# Diccionario que asocia cada tipo de incidente con el recurso necesario para atenderlo
tipo_recurso = {
    "Accidente": "Ambulancia",
    "Incendio": "Camion de Bomberos",
    "Robo": "Patrulla de Policia"
}


# Lista de recursos disponibles en el sistema
# Cada recurso tiene un ID y un tipo (nombre del vehiculo de emergencia)
recursos = []

id_counter = 1
for ubicacion in ubicaciones:  # ["Distrito 1", "Distrito 2", ...]
    for tipo in tipo_recurso.values():  # ["Bombero", "Ambulancia", "Policía"]
        for _ in range(2):  # Número de recursos por tipo y ubicación
            recursos.append(Recurso(id=id_counter, tipo=tipo, ubicacion=ubicacion))
            id_counter += 1


# Cola de incidentes pendientes por atender
# Aqui se almacenarán temporalmente los incidenes que no puedan ser atendidos al momento
cola_incidentes = []


