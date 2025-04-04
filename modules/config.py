# Importamos la clase Recurso desde el modulo models
from modules.models import Recurso

# Lista de recursos disponibles en el sistema
# Cada recurso tiene un ID y un tipo (nombre del vehiculo de emergencia)
recursos = [
    Recurso(1, "Ambulancia"), # Recurso para atender accidentes
    Recurso(2, "Camion de Bomberos"), # Recurso para atender incendios
    Recurso(3, "Patrulla de Policia") # Recurso para atender robos
]

# Diccionario que asocia cada tipo de incidente con el recurso necesario para atenderlo
tipo_recurso = {
    "Accidente": "Ambulancia",
    "Incendio": "Camion de Bomberos",
    "Robo": "Patrulla de Policia"
}

# Lista de ubicaciones posibles donde pueden ocurrir incidentes
# Corresponde a los 21 distritos de la ciudad de Madrid
ubicaciones = ["Centro", "Arganzuela", "Retiro", "Salamanca", "Chamartín", "Tetuán", 
                "Chamberí", "Fuencarral-El Pardo", "Moncloa", "Latina", "Carabanchel",
                "Usera", "Puente de Vallecas", "Moratalaz", "Ciudad Lineal", "Hortaleza",
                "Villaverde", "Villa de Vallecas", "Vicálvaro", "San Blas", "Barajas" ]

# Cola de incidentes pendientes por atender
# Aqui se almacenarán temporalmente los incidenes que no puedan ser atendidos al momento
cola_incidentes = []

