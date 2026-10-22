# Contrato de API — Horarios Inteligentes

**Proyecto:** Optimización y Automatización de la Programación de Horarios Académicos  
**Tecnologías:** Python, FastAPI, Angular, TypeScript, PostgreSQL y PuLP  
**Versión del contrato:** 1.0  
**Estado:** Propuesta para revisión y aprobación del equipo

---

## 1. Objetivo

Definir las reglas de comunicación entre el frontend Angular, el backend FastAPI, la base de datos PostgreSQL y el motor de optimización PuLP.

Todos los integrantes deben respetar las rutas, los nombres de campos, los tipos de datos y los formatos de respuesta establecidos en este documento.

## 2. Convenciones generales

- La API utilizará HTTP y JSON.
- Todas las rutas estarán bajo el prefijo `/api`.
- Los nombres de los campos utilizarán `snake_case`.
- Las relaciones entre registros se establecerán mediante identificadores (`id`), no mediante nombres visibles.
- El backend será responsable de validar los datos recibidos.
- Los errores se devolverán con un código HTTP apropiado y un mensaje comprensible.
- FastAPI generará la documentación OpenAPI en `/docs`.
- No se deben cambiar rutas, campos ni tipos de datos sin informar al equipo y actualizar este contrato.
- Las credenciales se configurarán mediante variables de entorno; nunca se subirán secretos reales a GitHub.

**URL local propuesta:** `http://localhost:8000`

## 3. Formato de respuestas

### 3.1. Respuesta de consulta

Las consultas devolverán un objeto o una lista de objetos JSON, según el endpoint.

Ejemplo:

```json
[
  {
    "id": 1,
    "nombre": "Aula 101",
    "capacidad": 40,
    "tiene_pizarra": true,
    "tiene_canonera": true,
    "tiene_escritorio_docente": true
  }
]
```

Los campos del ejemplo representan una propuesta de estructura; deben ajustarse al modelo de datos aprobado.

### 3.2. Respuesta de error

Se propone utilizar el siguiente formato común:

```json
{
  "detail": "No se encontró el aula solicitada"
}
```

FastAPI podrá utilizar su formato estándar de errores de validación cuando corresponda. El frontend deberá interpretar el código HTTP y mostrar un mensaje apropiado.

## 4. Códigos HTTP

| Código | Significado | Uso |
|---|---|---|
| 200 | OK | Consulta o ejecución procesada correctamente. |
| 201 | Created | Registro o versión creada correctamente. |
| 400 | Bad Request | Solicitud inválida o incompleta. |
| 404 | Not Found | Registro o versión inexistente. |
| 409 | Conflict | Conflicto con el estado actual o una operación no permitida. |
| 422 | Unprocessable Entity | Error de validación de FastAPI, cuando corresponda. |
| 500 | Internal Server Error | Error inesperado del servidor. |

Una solución sin horario factible no debe tratarse como un error interno del servidor. Debe comunicarse mediante el estado del motor de optimización.

## 5. Módulo de aulas y recursos físicos

**Responsable:** Integrante 2.

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/api/aulas` | Listar aulas. |
| POST | `/api/aulas` | Registrar un aula. |
| GET | `/api/aulas/{id}` | Consultar un aula. |
| PUT | `/api/aulas/{id}` | Actualizar un aula. |
| DELETE | `/api/aulas/{id}` | Eliminar un aula, sujeto a las restricciones de integridad. |

### Campos propuestos para un aula

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | integer | Identificador del aula. |
| `nombre` | string | Nombre o código visible del aula. |
| `capacidad` | integer | Capacidad máxima de estudiantes. |
| `tiene_pizarra` | boolean | Disponibilidad de pizarra. |
| `tiene_canonera` | boolean | Disponibilidad de cañonera. |
| `tiene_escritorio_docente` | boolean | Disponibilidad de escritorio para el docente. |

### Ejemplo de creación

`POST /api/aulas`

Solicitud:

```json
{
  "nombre": "Aula 101",
  "capacidad": 40,
  "tiene_pizarra": true,
  "tiene_canonera": true,
  "tiene_escritorio_docente": true
}
```

Respuesta propuesta — `201 Created`:

```json
{
  "id": 1,
  "nombre": "Aula 101",
  "capacidad": 40,
  "tiene_pizarra": true,
  "tiene_canonera": true,
  "tiene_escritorio_docente": true
}
```

La capacidad debe ser un entero positivo. No se permitirá eliminar un aula si existen relaciones que impidan hacerlo, según las reglas de integridad aprobadas.

## 6. Módulo académico y docente

**Responsable:** Integrante 3.

### 6.1. Cursos

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/api/cursos` | Listar cursos. |
| POST | `/api/cursos` | Crear un curso. |
| GET | `/api/cursos/{id}` | Consultar un curso. |
| PUT | `/api/cursos/{id}` | Actualizar un curso. |
| DELETE | `/api/cursos/{id}` | Eliminar un curso, respetando sus relaciones. |

Campos propuestos: `id`, `codigo`, `nombre` y `periodos_por_semana`.

### 6.2. Secciones

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/api/secciones` | Listar secciones. |
| POST | `/api/secciones` | Crear una sección. |
| GET | `/api/secciones/{id}` | Consultar una sección. |
| PUT | `/api/secciones/{id}` | Actualizar una sección. |
| DELETE | `/api/secciones/{id}` | Eliminar una sección, respetando sus relaciones. |

Campos propuestos: `id`, `codigo`, `curso_id`, `periodo_id` y `alumnos_inscritos`.

### 6.3. Catedráticos

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/api/catedraticos` | Listar catedráticos. |
| POST | `/api/catedraticos` | Registrar un catedrático. |
| GET | `/api/catedraticos/{id}` | Consultar un catedrático. |
| PUT | `/api/catedraticos/{id}` | Actualizar un catedrático. |
| DELETE | `/api/catedraticos/{id}` | Eliminar un catedrático, respetando sus relaciones. |

Campos propuestos: `id`, `nombre` y los datos adicionales que apruebe el equipo.

### 6.4. Disponibilidad docente

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/api/catedraticos/{id}/disponibilidad` | Consultar la disponibilidad de un catedrático. |
| PUT | `/api/catedraticos/{id}/disponibilidad` | Registrar o actualizar su disponibilidad. |

La estructura definitiva deberá representar los días y bloques horarios permitidos u ocupados.

### 6.5. Otros datos académicos

El equipo deberá definir las rutas y los esquemas de los siguientes elementos según el modelo de base de datos aprobado:

- Ciclos y períodos académicos.
- Cargas académicas mínimas y máximas.
- Preferencias de los catedráticos.
- Planes de estudio y mallas curriculares.

Estos datos deberán estar disponibles para el motor cuando sean necesarios para generar horarios válidos.

## 7. Módulo de generación de horarios

**Responsable:** Integrante 4.

### 7.1. Generar un horario

**Método:** `POST`  
**Ruta propuesta:** `/api/horarios/generar`

Solicitud:

```json
{
  "periodo_id": 1
}
```

El backend deberá obtener los datos necesarios, ejecutar el motor PuLP y guardar una nueva versión cuando exista una solución factible.

Respuesta de ejemplo:

```json
{
  "estado": "OPTIMAL",
  "mensaje": "Horario generado",
  "version_id": 7,
  "asignaciones": [
    {
      "curso_id": 12,
      "seccion_id": 2,
      "catedratico_id": 5,
      "aula_id": 3,
      "dia": "LUNES",
      "hora_inicio": "08:00",
      "hora_fin": "09:00"
    }
  ],
  "objetivo": 14.5
}
```

Los identificadores y valores son ilustrativos. La estructura definitiva de la respuesta y el significado de `objetivo` deberán acordarse antes de implementar la integración.

### 7.2. Estados del motor

| Estado | Significado |
|---|---|
| `OPTIMAL` | Se encontró una solución óptima. |
| `FEASIBLE` | Se encontró una solución válida, pero no se confirmó su optimalidad. |
| `INFEASIBLE` | No existe una solución que cumpla las restricciones actuales. |
| `ERROR` | Ocurrió un error durante la ejecución. |

El frontend deberá distinguir entre una solución no factible y un error técnico.

### 7.3. Consultar una versión generada

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/api/horarios/{id}` | Consultar una versión de horario generada. |

Cada generación factible deberá guardarse como una nueva versión. Las versiones anteriores no deben reemplazarse automáticamente.

Las rutas adicionales para listar versiones o consultar el historial quedan pendientes de aprobación.

## 8. Restricciones del motor de optimización

La generación debe respetar obligatoriamente las siguientes condiciones:

1. Un catedrático no puede impartir dos clases simultáneamente.
2. Un aula no puede utilizarse para dos cursos simultáneamente.
3. La capacidad del aula debe ser suficiente para los alumnos inscritos en la sección.
4. Las clases deben respetar la disponibilidad horaria permitida.

Entre las soluciones que cumplan todas las restricciones obligatorias, el motor buscará:

- Minimizar las horas muertas de catedráticos y estudiantes.
- Favorecer las preferencias horarias de los catedráticos.

La programación se realizará de lunes a viernes, entre las 07:00 y las 18:00, en bloques de 60 minutos. La representación de clases que requieran varios bloques consecutivos debe definirse en el modelo matemático.

## 9. Reglas de validación

Todos los endpoints deben validar, según corresponda:

- Campos obligatorios y tipos de datos.
- Identificadores y existencia de registros relacionados.
- Valores positivos para capacidades, cantidades y cargas cuando aplique.
- Horarios dentro del rango permitido.
- Relaciones y restricciones de integridad de la base de datos.
- Conflictos con registros o asignaciones existentes.

La validación del frontend no sustituye la validación del backend.

## 10. Integración con Angular

El frontend consumirá los endpoints mediante el cliente HTTP de Angular.

Se recomienda centralizar la URL de la API en la configuración de entornos de Angular y separar las llamadas HTTP en servicios por módulo.

Los servicios deberán respetar las rutas y los tipos de datos definidos en este contrato. No deben inventar campos ni simular respuestas definitivas que no estén acordadas con el backend.

## 11. Documentación OpenAPI

FastAPI deberá mantener actualizada la documentación de los endpoints.

En desarrollo local estará disponible en:

- Swagger UI: `/docs`
- OpenAPI JSON: `/openapi.json`
- ReDoc: `/redoc`

Cada endpoint deberá documentar el método, la ruta, su propósito, parámetros, solicitud, respuesta y posibles errores.

## 12. Convenciones de Git y cambios al contrato

- Cada integrante trabajará en una rama de funcionalidad.
- Los cambios se integrarán mediante Pull Request y revisión.
- El esquema de PostgreSQL será coordinado por el integrante 1.
- Los cambios en rutas, campos o tipos de datos deberán discutirse y documentarse.
- Se evitará modificar simultáneamente los mismos archivos.
- No se subirán archivos `.env` reales, contraseñas ni tokens.
- Se actualizarán las pruebas y la documentación cuando cambie el comportamiento de un endpoint.

**Regla final:** ningún integrante debe modificar unilateralmente el contrato. Los cambios se revisan, se aprueban y se documentan para mantener la compatibilidad entre todos los módulos.
