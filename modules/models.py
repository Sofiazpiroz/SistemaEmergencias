# Clase que representa un incidente dentro del sistema
class Incidente:
    def __init__(self, id, tipo, prioridad, ubicacion):
        self.id = id # Identificador del incidente
        self.tipo = tipo # Tipo de incidente = "Robo", "Incendio", "Accidente"
        self.prioridad = prioridad # Nivel de prioridad del incidente (1 mas alto)
        self.ubicacion = ubicacion # Distrito donde ocurre el incidente
        self.tiempo_creacion = None # Tiempo simulado en el que se genera el incidente


# Clase que representa un recurso de emergencia
class Recurso:
    def __init__(self, id, tipo):
        self.id = id # Identificador del recurso
        self.tipo = tipo  # Tipo de recurso = "Ambulancia", "Camión de Bomberos", "Policía"
        self.disponible = True # Indica si el recurso esta disponible u ocupado
