
from app.optimizer.model import construir_modelo
from app.optimizer.solver import resolver_modelo


def datos_prueba():
    return {
        "periodo_id": 1,
        "secciones": [{
            "id_seccion": 1,
            "id_curso": 10,
            "horas_semanales": 2,
            "cantidad_estudiantes": 20,
            "id_carrera": 1,
            "id_ciclo": 1
        }],
        "profesores": [{
            "id_profesor": 1,
            "carga_minima": 0,
            "carga_maxima": 10
        }],
        "aulas": [{
            "id_aula": 1,
            "capacidad": 30
        }],
        "bloques": [
            {
                "id_bloque": 1,
                "dia_semana": 1,
                "orden_dia": 1,
                "hora_inicio": "08:00"
            },
            {
                "id_bloque": 2,
                "dia_semana": 1,
                "orden_dia": 2,
                "hora_inicio": "09:00"
            },
            {
                "id_bloque": 3,
                "dia_semana": 1,
                "orden_dia": 3,
                "hora_inicio": "10:00"
            }
        ],
        "profesor_curso": {(10, 1)},
        "disponibilidad": {
            (1, 1): True,
            (1, 2): True,
            (1, 3): True
        },
        "preferencias": {
            (1, 1): 1,
            (1, 2): 2,
            (1, 3): 1
        },
        "requisitos_recursos": {},
        "recursos_aula": {},
        "configuracion": {
            "id_configuracion": None,
            "peso_horas_muertas_docente": 1,
            "peso_horas_muertas_seccion": 1,
            "peso_preferencias": 1,
            "tiempo_limite_segundos": 10
        }
    }


def test_generacion_basica():
    datos = datos_prueba()

    modelo, variables = construir_modelo(datos)
    resultado = resolver_modelo(modelo, variables, 10)

    assert resultado["estado"] == "OPTIMAL"
    assert len(resultado["asignaciones"]) == 2


def test_sin_disponibilidad_es_infactible():
    datos = datos_prueba()
    datos["disponibilidad"] = {}

    modelo, variables = construir_modelo(datos)
    resultado = resolver_modelo(modelo, variables, 10)

    assert resultado["estado"] == "INFEASIBLE"
    assert resultado["asignaciones"] == []
