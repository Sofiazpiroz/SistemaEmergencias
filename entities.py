
iimport random

'''Clases'''

class Incidente:
    def __init__(self, env, id_incidente, tipo, ubicacion, prioridad):
        self.env = env
        self.id_incidente = id_incidente
        self.tipo = tipo
        self.ubicacion = ubicacion
        self.prioridad = prioridad
        self.tiempo_resolucion = random.randint(3, 10)  # Tiempo aleatorio


    def __str__(self):
        return f"Incidente {self.id_incidente}: {self.tipo} en {self.ubicacion} (Prioridad {self.prioridad})"


class Recurso(Incidente):
    def __init__(self, env, tipo, ubicacion):
        self.env = env
        self.tipo = tipo
        self.ubicacion = ubicacion
        self.disponible = True  # Estado del recurso

    def asignar(self, incidente):
        if self.disponible:
            self.disponible = False
            print(f"{self.tipo} asignado a {incidente} en {self.env.now} minutos")
            yield self.env.timeout(incidente.tiempo_resolucion)  # Tiempo de atención al cliente
            self.disponible = True
            print(f"{self.tipo} disponible nuevamente en {self.env.now} minutos")

    def __str__(self):
        return f"{self.tipo} en {self.ubicacion}"


# Subclases de la clase "Recurso"
class Ambulancia(Recurso):
    def __init__(self, env, ubicacion):
        super().__init__(env, "Ambulancia", ubicacion)

class CamionBomberos(Recurso):
    def __init__(self, env, ubicacion):
        super().__init__(env, "Camión de Bomberos", ubicacion)

class PatrullaPolicia(Recurso):
    def __init__(self, env, ubicacion):
        super().__init__(env, "Patrulla de Policía", ubicacion)

class PatrullaPolicia(Recurso):
    def _init_(self, env, ubicacion):
        super()._init_(env, "Patrulla de Policía", ubicacion)
