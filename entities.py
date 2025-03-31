
  import random

class Incidente:
    def __init__(self, env, id_incidente, tipo, ubicacion, prioridad):
        self.env = env
        self.id_incidente = id_incidente
        self.tipo = tipo
        self.ubicacion = ubicacion
        self.prioridad = prioridad
        self.tiempo_creacion = None

class Recurso:
    def __init__(self, env, id_recurso, ubicacion, prioridad):
        self.env = env
        self.id = id_recurso
        self.ubicacion = ubicacion
        self.prioridad = prioridad
        self.disponible = True

    def asignar(self, incidente):
        # Simulación de tiempos realistas y variados por tipo
        if incidente.tipo == "Incendio":
            tiempo_atencion = random.uniform(10, 20)  # más largo
        elif incidente.tipo == "Accidente":
            tiempo_atencion = random.uniform(5, 15)
        elif incidente.tipo == "Robo":
            tiempo_atencion = random.uniform(4, 10)
        else:
            tiempo_atencion = random.uniform(5, 12)

        yield self.env.timeout(tiempo_atencion)

class Ambulancia(Recurso):
    def __init__(self, env, id_recurso, ubicacion, prioridad):
        super().__init__(env, id_recurso, ubicacion, prioridad)
        self.tipo = "Ambulancia"

class CamionBomberos(Recurso):
    def __init__(self, env, id_recurso, ubicacion, prioridad):
        super().__init__(env, id_recurso, ubicacion, prioridad)
        self.tipo = "Camión de Bomberos"

class PatrullaPolicia(Recurso):
    def __init__(self, env, id_recurso, ubicacion, prioridad):
        super().__init__(env, id_recurso, ubicacion, prioridad)
        self.tipo = "Patrulla de Policía"


