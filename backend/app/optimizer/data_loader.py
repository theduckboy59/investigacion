
from collections import defaultdict


def cargar_datos(cursor, periodo_id: int) -> dict:
    """Carga los datos del período desde el esquema SQL del proyecto."""

    cursor.execute("""
        SELECT
            s.id_seccion,
            s.codigo AS codigo_seccion,
            s.nombre AS nombre_seccion,
            s.cantidad_estudiantes,
            s.id_periodo,
            c.id_curso,
            c.codigo AS codigo_curso,
            c.nombre AS nombre_curso,
            c.horas_semanales,
            c.id_carrera,
            c.id_ciclo
        FROM secciones s
        JOIN cursos c ON c.id_curso = s.id_curso
        WHERE s.id_periodo = %s
          AND s.estado = TRUE
          AND c.estado = TRUE
        ORDER BY s.id_seccion
    """, (periodo_id,))
    secciones = [dict(r) for r in cursor.fetchall()]

    cursor.execute("""
        SELECT id_profesor, codigo, nombres, apellidos,
               carga_minima, carga_maxima
        FROM profesores
        WHERE estado = TRUE
    """)
    profesores = [dict(r) for r in cursor.fetchall()]

    cursor.execute("""
        SELECT id_aula, codigo, nombre, capacidad
        FROM aulas
        WHERE estado = TRUE
    """)
    aulas = [dict(r) for r in cursor.fetchall()]

    cursor.execute("""
        SELECT id_bloque, dia_semana, hora_inicio, hora_fin,
               duracion_minutos, orden_dia
        FROM bloques_horarios
        WHERE estado = TRUE
          AND dia_semana BETWEEN 1 AND 5
          AND hora_inicio >= TIME '07:00'
          AND hora_fin <= TIME '18:00'
          AND duracion_minutos = 60
        ORDER BY dia_semana, orden_dia, hora_inicio
    """)
    bloques = [dict(r) for r in cursor.fetchall()]

    cursor.execute("""
        SELECT id_profesor, id_curso
        FROM profesor_curso
    """)
    profesor_curso = {
        (r["id_curso"], r["id_profesor"])
        for r in cursor.fetchall()
    }

    cursor.execute("""
        SELECT id_profesor, id_bloque, disponible
        FROM disponibilidad_docente
    """)
    disponibilidad = {
        (r["id_profesor"], r["id_bloque"]): bool(r["disponible"])
        for r in cursor.fetchall()
    }

    cursor.execute("""
        SELECT id_profesor, id_bloque, valor_preferencia
        FROM preferencias_docente
    """)
    preferencias = {
        (r["id_profesor"], r["id_bloque"]): int(r["valor_preferencia"] or 0)
        for r in cursor.fetchall()
    }

    cursor.execute("""
        SELECT id_curso, id_recurso, cantidad_requerida
        FROM curso_recurso
    """)
    requisitos_recursos = defaultdict(dict)
    for r in cursor.fetchall():
        requisitos_recursos[r["id_curso"]][r["id_recurso"]] = int(
            r["cantidad_requerida"] or 1
        )

    cursor.execute("""
        SELECT id_aula, id_recurso, cantidad
        FROM aula_recurso
    """)
    recursos_aula = {
        (r["id_aula"], r["id_recurso"]): int(r["cantidad"] or 0)
        for r in cursor.fetchall()
    }

    cursor.execute("""
        SELECT id_configuracion, peso_horas_muertas_docente,
               peso_horas_muertas_seccion, peso_preferencias,
               tiempo_limite_segundos
        FROM configuracion_optimizacion
        ORDER BY fecha_creacion DESC, id_configuracion DESC
        LIMIT 1
    """)
    config = cursor.fetchone()

    configuracion = dict(config) if config else {
        "id_configuracion": None,
        "peso_horas_muertas_docente": 1,
        "peso_horas_muertas_seccion": 1,
        "peso_preferencias": 1,
        "tiempo_limite_segundos": 60,
    }

    return {
        "periodo_id": periodo_id,
        "secciones": secciones,
        "profesores": profesores,
        "aulas": aulas,
        "bloques": bloques,
        "profesor_curso": profesor_curso,
        "disponibilidad": disponibilidad,
        "preferencias": preferencias,
        "requisitos_recursos": dict(requisitos_recursos),
        "recursos_aula": recursos_aula,
        "configuracion": configuracion,
    }
