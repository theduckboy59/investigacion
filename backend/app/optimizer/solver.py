
import time
import pulp


def resolver_modelo(modelo, variables, tiempo_limite=60):
    inicio = time.perf_counter()

    solver = pulp.PULP_CBC_CMD(
        msg=False,
        timeLimit=max(1, int(tiempo_limite))
    )

    codigo = modelo.solve(solver)
    estado_solver = pulp.LpStatus.get(codigo, "Undefined")

    valores = [v.varValue for v in variables.values()]
    valores_disponibles = all(v is not None for v in valores)

    asignaciones = []

    if valores_disponibles:
        for clave, variable in variables.items():
            if variable.varValue > 0.5:
                seccion_id, profesor_id, aula_id, bloque_id = clave

                asignaciones.append({
                    "seccion_id": seccion_id,
                    "profesor_id": profesor_id,
                    "aula_id": aula_id,
                    "bloque_id": bloque_id
                })

    if estado_solver == "Optimal":
        estado = "OPTIMAL"
        mensaje = "Se encontró una solución óptima."

    elif estado_solver == "Infeasible":
        estado = "INFEASIBLE"
        mensaje = "No existe una solución que cumpla todas las restricciones."
        asignaciones = []

    elif valores_disponibles and asignaciones:
        estado = "FEASIBLE"
        mensaje = "Se encontró una solución factible."

    else:
        estado = "ERROR"
        mensaje = f"No se obtuvo una solución válida. Estado: {estado_solver}."
        asignaciones = []

    objetivo = (
        pulp.value(modelo.objective)
        if estado in ("OPTIMAL", "FEASIBLE")
        else None
    )

    return {
        "estado": estado,
        "mensaje": mensaje,
        "asignaciones": asignaciones,
        "objetivo": float(objetivo) if objetivo is not None else None,
        "tiempo_ejecucion_segundos": round(
            time.perf_counter() - inicio, 3
        ),
        "estado_solver": estado_solver
    }
