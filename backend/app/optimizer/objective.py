
import pulp


def agregar_objetivo(modelo, x, datos):
    """
    Agrega la función objetivo del modelo.

    Los pesos y valores de preferencias deberán venir
    de la configuración y los datos acordados por el equipo.
    """

    # Esta versión inicial solo prepara la estructura.
    # La función definitiva incluirá horas muertas y preferencias.
    modelo += pulp.lpSum(x.values()), "Objetivo_temporal"
