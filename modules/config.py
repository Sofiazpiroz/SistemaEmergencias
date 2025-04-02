from modules.models import Recurso

recursos = [
    Recurso(1, "Ambulancia"),
    Recurso(2, "Camion de Bomberos"),
    Recurso(3, "Patrulla de Policia")
]

tipo_recurso = {
    "Accidente": "Ambulancia",
    "Incendio": "Camion de Bomberos",
    "Robo": "Patrulla de Policia"
}

ubicaciones = ["Centro", "Arganzuela", "Retiro", "Salamanca", "Chamartín", "Tetuán", 
                "Chamberí", "Fuencarral-El Pardo", "Moncloa", "Latina", "Carabanchel",
                "Usera", "Puente de Vallecas", "Moratalaz", "Ciudad Lineal", "Hortaleza",
                "Villaverde", "Villa de Vallecas", "Vicálvaro", "San Blas", "Barajas" ]

cola_incidentes = []