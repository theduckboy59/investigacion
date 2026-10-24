
import pulp


def agregar_restricciones(modelo, x, secciones, profesores, aulas, bloques, datos):
    """
    Agrega las restricciones obligatorias del horario académico.

    x[(seccion_id, profesor_id, aula_id, bloque_id)] es una
    variable binaria que indica si se realiza esa asignación.
    """

    # 1. Cada sección debe recibir sus horas semanales requeridas.
    for seccion in secciones:
        seccion_id = seccion["id"]
        horas = seccion["horas_semanales"]

        variables = [
            variable
            for clave, variable in x.items()
            if clave[0] == seccion_id
        ]

        modelo += (
            pulp.lpSum(variables) == horas,
            f"horas_seccion_{seccion_id}"
        )

    # 2. Un profesor no puede impartir dos clases en el mismo bloque.
    for profesor in profesores:
        profesor_id = profesor["id"]

        for bloque in bloques:
            bloque_id = bloque["id"]

            variables = [
                variable
                for clave, variable in x.items()
                if clave[1] == profesor_id and clave[3] == bloque_id
            ]

            modelo += (
                pulp.lpSum(variables) <= 1,
                f"profesor_{profesor_id}_bloque_{bloque_id}"
            )

    # 3. Un aula no puede tener dos clases en el mismo bloque.
    for aula in aulas:
        aula_id = aula["id"]

        for bloque in bloques:
            bloque_id = bloque["id"]

            variables = [
                variable
                for clave, variable in x.items()
                if clave[2] == aula_id and clave[3] == bloque_id
            ]

            modelo += (
                pulp.lpSum(variables) <= 1,
                f"aula_{aula_id}_bloque_{bloque_id}"
            )

    # 4. Solo se permiten combinaciones válidas de profesor,
    # aula y bloque para cada sección.
    for clave, variable in x.items():
        seccion_id, profesor_id, aula_id, bloque_id = clave

        if not datos["disponibilidad"].get(
            (profesor_id, bloque_id), False
        ):
            modelo += variable == 0

        capacidad = datos["capacidad_aula"][aula_id]
        alumnos = datos["alumnos_seccion"][seccion_id]

        if capacidad < alumnos:
            modelo += variable == 0

        if (seccion_id, profesor_id) not in datos["profesores_curso"]:
            modelo += variable == 0
