
from collections import defaultdict
import pulp


def construir_modelo(datos):
    secciones = datos["secciones"]
    profesores = datos["profesores"]
    aulas = datos["aulas"]
    bloques = datos["bloques"]

    modelo = pulp.LpProblem(
        "Horarios_Inteligentes",
        pulp.LpMinimize
    )

    profesor_por_id = {p["id_profesor"]: p for p in profesores}
    aula_por_id = {a["id_aula"]: a for a in aulas}

    requisitos = datos["requisitos_recursos"]
    recursos_aula = datos["recursos_aula"]
    disponibilidad = datos["disponibilidad"]

    # x = 1 si una sección se asigna a un profesor,
    # aula y bloque determinados.
    x = {}

    for seccion in secciones:
        sid = seccion["id_seccion"]
        cid = seccion["id_curso"]
        alumnos = int(seccion["cantidad_estudiantes"] or 0)

        for profesor in profesores:
            pid = profesor["id_profesor"]

            if (cid, pid) not in datos["profesor_curso"]:
                continue

            for bloque in bloques:
                bid = bloque["id_bloque"]

                # La ausencia de registro se interpreta como no disponible.
                if disponibilidad.get((pid, bid)) is not True:
                    continue

                for aula in aulas:
                    aid = aula["id_aula"]

                    if int(aula["capacidad"] or 0) < alumnos:
                        continue

                    # Validar todos los recursos exigidos por el curso.
                    tiene_recursos = all(
                        recursos_aula.get((aid, rid), 0) >= cantidad
                        for rid, cantidad in requisitos.get(cid, {}).items()
                    )

                    if not tiene_recursos:
                        continue

                    clave = (sid, pid, aid, bid)
                    x[clave] = pulp.LpVariable(
                        f"x_s{sid}_p{pid}_a{aid}_b{bid}",
                        cat="Binary"
                    )

    # Restricción 1: cada sección recibe las horas semanales del curso.
    for seccion in secciones:
        sid = seccion["id_seccion"]
        horas = int(seccion["horas_semanales"] or 0)

        modelo += (
            pulp.lpSum(v for k, v in x.items() if k[0] == sid) == horas,
            f"horas_seccion_{sid}"
        )

    # Restricción 2: un profesor no puede impartir dos clases a la vez.
    for profesor in profesores:
        pid = profesor["id_profesor"]

        for bloque in bloques:
            bid = bloque["id_bloque"]

            modelo += (
                pulp.lpSum(
                    v for k, v in x.items()
                    if k[1] == pid and k[3] == bid
                ) <= 1,
                f"profesor_{pid}_bloque_{bid}"
            )

    # Restricción 3: un aula no puede recibir dos clases a la vez.
    for aula in aulas:
        aid = aula["id_aula"]

        for bloque in bloques:
            bid = bloque["id_bloque"]

            modelo += (
                pulp.lpSum(
                    v for k, v in x.items()
                    if k[2] == aid and k[3] == bid
                ) <= 1,
                f"aula_{aid}_bloque_{bid}"
            )

    # Restricción 4: cursos de la misma carrera y ciclo no coinciden.
    # Es una aproximación porque el SQL no tiene una tabla de planes/grupos.
    cohortes = defaultdict(list)

    for seccion in secciones:
        cohorte = (
            seccion["id_carrera"],
            seccion["id_ciclo"]
        )
        cohortes[cohorte].append(seccion["id_seccion"])

    for cohorte, ids_secciones in cohortes.items():
        for bloque in bloques:
            bid = bloque["id_bloque"]

            modelo += (
                pulp.lpSum(
                    v for k, v in x.items()
                    if k[0] in ids_secciones and k[3] == bid
                ) <= 1,
                f"cohorte_{cohorte[0]}_{cohorte[1]}_bloque_{bid}"
            )

    # Carga mínima y máxima de cada profesor.
    for profesor in profesores:
        pid = profesor["id_profesor"]
        asignaciones = pulp.lpSum(
            v for k, v in x.items() if k[1] == pid
        )

        minimo = int(profesor["carga_minima"] or 0)
        maximo = profesor["carga_maxima"]

        modelo += asignaciones >= minimo, f"carga_minima_{pid}"

        if maximo is not None:
            modelo += asignaciones <= int(maximo), f"carga_maxima_{pid}"

    # Función objetivo: penalizar bloques vacíos entre clases y
    # premiar asignaciones en horarios preferidos.
    bloques_por_dia = defaultdict(list)

    for bloque in bloques:
        bloques_por_dia[bloque["dia_semana"]].append(bloque)

    for dia in bloques_por_dia:
        bloques_por_dia[dia].sort(
            key=lambda b: (b["orden_dia"] or 0, b["hora_inicio"])
        )

    gaps_docente = []
    gaps_seccion = []

    # Cada gap representa un bloque libre entre dos bloques ocupados.
    for profesor in profesores:
        pid = profesor["id_profesor"]

        for dia, lista in bloques_por_dia.items():
            ocupacion = [
                pulp.lpSum(
                    v for k, v in x.items()
                    if k[1] == pid and k[3] == b["id_bloque"]
                )
                for b in lista
            ]

            for i in range(1, len(lista) - 1):
                antes = pulp.LpVariable(
                    f"antes_p{pid}_d{dia}_i{i}", cat="Binary"
                )
                despues = pulp.LpVariable(
                    f"despues_p{pid}_d{dia}_i{i}", cat="Binary"
                )
                gap = pulp.LpVariable(
                    f"gap_p{pid}_d{dia}_i{i}", cat="Binary"
                )

                for j in range(i):
                    modelo += antes >= ocupacion[j]

                for j in range(i + 1, len(lista)):
                    modelo += despues >= ocupacion[j]

                modelo += gap >= antes + despues - ocupacion[i] - 1
                gaps_docente.append(gap)

    for seccion in secciones:
        sid = seccion["id_seccion"]

        for dia, lista in bloques_por_dia.items():
            ocupacion = [
                pulp.lpSum(
                    v for k, v in x.items()
                    if k[0] == sid and k[3] == b["id_bloque"]
                )
                for b in lista
            ]

            for i in range(1, len(lista) - 1):
                antes = pulp.LpVariable(
                    f"antes_s{sid}_d{dia}_i{i}", cat="Binary"
                )
                despues = pulp.LpVariable(
                    f"despues_s{sid}_d{dia}_i{i}", cat="Binary"
                )
                gap = pulp.LpVariable(
                    f"gap_s{sid}_d{dia}_i{i}", cat="Binary"
                )

                for j in range(i):
                    modelo += antes >= ocupacion[j]

                for j in range(i + 1, len(lista)):
                    modelo += despues >= ocupacion[j]

                modelo += gap >= antes + despues - ocupacion[i] - 1
                gaps_seccion.append(gap)

    config = datos["configuracion"]
    peso_docente = float(config["peso_horas_muertas_docente"] or 0)
    peso_seccion = float(config["peso_horas_muertas_seccion"] or 0)
    peso_preferencias = float(config["peso_preferencias"] or 0)

    preferencia = pulp.lpSum(
        float(datos["preferencias"].get((k[1], k[3]), 0)) * v
        for k, v in x.items()
    )

    modelo += (
        peso_docente * pulp.lpSum(gaps_docente)
        + peso_seccion * pulp.lpSum(gaps_seccion)
        - peso_preferencias * preferencia
    ), "Objetivo_horas_muertas_y_preferencias"

    return modelo, x
