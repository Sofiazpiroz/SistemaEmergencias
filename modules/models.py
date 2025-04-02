class Incidente:
    def __init__(self, id, tipo, prioridad, ubicacion):
        self.id = id
        self.tipo = tipo
        self.prioridad = prioridad
        self.ubicacion = ubicacion
        self.tiempo_creacion = None

class Recurso:
    def __init__(self, id, tipo):
        self.id = id
        self.tipo = tipo
        self.disponible = True