
import random


class Incidente:
    def _init_(self, env, id_incidente, tipo, ubicacion, prioridad):
        self.env = env
        self.id_incidente = id_incidente
        self.tipo = tipo
        self.ubicacion = ubicacion
        self.prioridad = prioridad
        self.tiempo_resolucion = random.randint(3, 10)  # Tiempo aleatorio

    def _str_(self):
        return f"Incidente {self.id_incidente}: {self.tipo} en {self.ubicacion} (Prioridad {self.prioridad})"


class Recurso:
    def _init_(self, env, tipo, ubicacion):
        self.env = env
        self.tipo = tipo
        self.ubicacion = ubicacion
        self.disponible = True  # Estado del recurso

    def asignar(self, incidente):
        '''Simula la asignación del recurso a un incidente'''
        if self.disponible:
            self.disponible = False
            print(f"{self.tipo} asignado a {incidente} en el tiempo {self.env.now}")
            yield self.env.timeout(incidente.tiempo_resolucion)  # Tiempo de atención
            self.disponible = True
            print(f"{self.tipo} disponible nuevamente en el tiempo {self.env.now}")

    def _str_(self):
        return f"{self.tipo} en {self.ubicacion}"


# Subclases de Recurso
class Ambulancia(Recurso):
    def _init_(self, env, ubicacion):
        super()._init_(env, "Ambulancia", ubicacion)

class CamionBomberos(Recurso):
    def _init_(self, env, ubicacion):
        super()._init_(env, "Camión de Bomberos", ubicacion)

class PatrullaPolicia(Recurso):
    def _init_(self, env, ubicacion):
        super()._init_(env, "Patrulla de Policía", ubicacion)