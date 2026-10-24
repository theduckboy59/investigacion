
import os
import psycopg2
from psycopg2.extras import RealDictCursor

from app.optimizer.data_loader import cargar_datos
from app.optimizer.model import construir_modelo
from app.optimizer.solver import resolver_modelo


def conectar_bd():
    database_url = os.getenv("DATABASE_URL")

    if database_url:
        return psycopg2.connect(database_url)

    variables = ["DB_HOST", "DB_NAME", "DB_USER", "DB_PASSWORD"]
    faltantes = [v for v in variables if not os.getenv(v)]

    if faltantes:
        raise RuntimeError(
            "Configura las variables de PostgreSQL: "
            + ", ".join(faltantes)
        )

    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )


def generar_horario(periodo_id: int):
    with conectar_bd() as conexion:
        with conexion.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:

            cursor.execute("""
                SELECT id_periodo
                FROM periodos_academicos
                WHERE id_periodo = %s
                  AND estado = TRUE
            """, (periodo_id,))

            if cursor.fetchone() is None:
                raise ValueError(
                    f"El período {periodo_id} no existe o está inactivo."
                )

            datos = cargar_datos(cursor, periodo_id)

            if not datos["secciones"]:
                raise ValueError(
                    "El período no tiene secciones activas para programar."
                )

            if not datos["bloques"]:
                raise ValueError(
                    "No existen bloques horarios válidos de lunes a viernes."
                )

            modelo, variables = construir_modelo(datos)

            limite = datos["configuracion"][
                "tiempo_limite_segundos"
            ] or 60

            resultado = resolver_modelo(
                modelo,
                variables,
                limite
            )

            codigos_estado = {
                "OPTIMAL": "optimo",
                "FEASIBLE": "factible",
                "INFEASIBLE": "infactible",
                "ERROR": "error"
            }

            cursor.execute("""
                SELECT id_estado
                FROM catalogo_estados_horario
                WHERE codigo = %s
            """, (codigos_estado[resultado["estado"]],))

            estado_row = cursor.fetchone()

            if estado_row is None:
                raise RuntimeError(
                    "Falta el estado correspondiente en "
                    "catalogo_estados_horario."
                )

            config_id = datos["configuracion"]["id_configuracion"]

            cursor.execute("""
                INSERT INTO horarios_generados (
                    nombre,
                    id_periodo,
                    id_configuracion,
                    id_estado,
                    valor_objetivo,
                    tiempo_ejecucion_segundos
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id_horario
            """, (
                f"Generación del período {periodo_id}",
                periodo_id,
                config_id,
                estado_row["id_estado"],
                resultado["objetivo"],
                resultado["tiempo_ejecucion_segundos"]
            ))

            horario_id = cursor.fetchone()["id_horario"]

            # Solo se persisten asignaciones si la solución es válida.
            if resultado["estado"] in ("OPTIMAL", "FEASIBLE"):
                for asignacion in resultado["asignaciones"]:
                    cursor.execute("""
                        INSERT INTO asignaciones_horario (
                            id_horario,
                            id_seccion,
                            id_profesor,
                            id_aula,
                            id_bloque
                        )
                        VALUES (%s, %s, %s, %s, %s)
                    """, (
                        horario_id,
                        asignacion["seccion_id"],
                        asignacion["profesor_id"],
                        asignacion["aula_id"],
                        asignacion["bloque_id"]
                    ))

            resultado["version_id"] = horario_id
            resultado["periodo_id"] = periodo_id
            resultado["asignaciones"] = obtener_detalle_asignaciones(
                cursor,
                resultado["asignaciones"]
            )

            return resultado


def obtener_detalle_asignaciones(cursor, asignaciones):
    detalle = []

    for a in asignaciones:
        cursor.execute("""
            SELECT
                c.id_curso,
                c.codigo AS codigo_curso,
                c.nombre AS curso,
                s.id_seccion,
                s.codigo AS codigo_seccion,
                p.id_profesor,
                p.nombres,
                p.apellidos,
                au.id_aula,
                au.codigo AS codigo_aula,
                au.nombre AS aula,
                b.id_bloque,
                b.dia_semana,
                b.hora_inicio,
                b.hora_fin
            FROM secciones s
            JOIN cursos c ON c.id_curso = s.id_curso
            JOIN profesores p ON p.id_profesor = %s
            JOIN aulas au ON au.id_aula = %s
            JOIN bloques_horarios b ON b.id_bloque = %s
            WHERE s.id_seccion = %s
        """, (
            a["profesor_id"],
            a["aula_id"],
            a["bloque_id"],
            a["seccion_id"]
        ))

        fila = cursor.fetchone()

        if not fila:
            continue

        dias = {
            1: "LUNES",
            2: "MARTES",
            3: "MIERCOLES",
            4: "JUEVES",
            5: "VIERNES"
        }

        detalle.append({
            "curso_id": fila["id_curso"],
            "curso": fila["curso"],
            "seccion_id": fila["id_seccion"],
            "seccion": fila["codigo_seccion"],
            "profesor_id": fila["id_profesor"],
            "profesor": (
                f'{fila["nombres"]} {fila["apellidos"]}'
            ).strip(),
            "aula_id": fila["id_aula"],
            "aula": fila["codigo_aula"] or fila["aula"],
            "bloque_id": fila["id_bloque"],
            "dia": dias.get(fila["dia_semana"], "DESCONOCIDO"),
            "hora_inicio": fila["hora_inicio"].strftime("%H:%M"),
            "hora_fin": fila["hora_fin"].strftime("%H:%M")
        })

    return detalle
