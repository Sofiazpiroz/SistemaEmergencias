import simpy
from process import generar_incidentes
from entities import Ambulancia, CamionBomberos, PatrullaPolicia

'''Main'''

if __name__ == "__main__":
    env = simpy.Environment()

    # Definimos los recursos necesarios para atender las emergencias
    recursos = [ Ambulancia, CamionBomberos, PatrullaPolicia]

    # Generamos los incidentes
    env.process(generar_incidentes(env, [], recursos))

    # Ejecutamos la simulación por 30 unidades de tiempo
    env.run(until=30)
    
