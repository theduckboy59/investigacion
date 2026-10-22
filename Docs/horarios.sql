CREATE TABLE carreras (
    id_carrera SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    descripcion TEXT,
    estado BOOLEAN DEFAULT TRUE
);

CREATE TABLE ciclos (
    id_ciclo SERIAL PRIMARY KEY,
    nombre VARCHAR(50),
    orden INTEGER
);

CREATE TABLE catalogo_estados_horario (
    id_estado SERIAL PRIMARY KEY,
    codigo VARCHAR(20)
);

INSERT INTO catalogo_estados_horario (codigo) VALUES
('pendiente'),
('optimo'),
('factible'),
('infactible'),
('error');

CREATE TABLE periodos_academicos (
    id_periodo SERIAL PRIMARY KEY,
    nombre VARCHAR(30),
    fecha_inicio DATE,
    fecha_fin DATE,
    estado BOOLEAN DEFAULT TRUE
);

CREATE TABLE cursos (
    id_curso SERIAL PRIMARY KEY,
    codigo VARCHAR(20),
    nombre VARCHAR(120),
    horas_semanales INTEGER,
    id_carrera INTEGER REFERENCES carreras(id_carrera),
    id_ciclo INTEGER REFERENCES ciclos(id_ciclo),
    estado BOOLEAN DEFAULT TRUE
);

CREATE TABLE profesores (
    id_profesor SERIAL PRIMARY KEY,
    codigo VARCHAR(20),
    nombres VARCHAR(100),
    apellidos VARCHAR(100),
    correo VARCHAR(120),
    carga_minima INTEGER DEFAULT 0,
    carga_maxima INTEGER,
    estado BOOLEAN DEFAULT TRUE
);

CREATE TABLE secciones (
    id_seccion SERIAL PRIMARY KEY,
    codigo VARCHAR(20),
    id_curso INTEGER REFERENCES cursos(id_curso),
    nombre VARCHAR(10),
    cantidad_estudiantes INTEGER,
    id_periodo INTEGER REFERENCES periodos_academicos(id_periodo),
    estado BOOLEAN DEFAULT TRUE
);

CREATE TABLE profesor_curso (
    id_profesor INTEGER REFERENCES profesores(id_profesor),
    id_curso INTEGER REFERENCES cursos(id_curso),
    PRIMARY KEY (id_profesor, id_curso)
);

CREATE TABLE aulas (
    id_aula SERIAL PRIMARY KEY,
    codigo VARCHAR(20),
    nombre VARCHAR(80),
    capacidad INTEGER,
    ubicacion VARCHAR(100),
    estado BOOLEAN DEFAULT TRUE
);

CREATE TABLE recursos (
    id_recurso SERIAL PRIMARY KEY,
    nombre VARCHAR(80),
    descripcion TEXT
);

CREATE TABLE aula_recurso (
    id_aula INTEGER REFERENCES aulas(id_aula),
    id_recurso INTEGER REFERENCES recursos(id_recurso),
    cantidad INTEGER DEFAULT 1,
    PRIMARY KEY (id_aula, id_recurso)
);

CREATE TABLE curso_recurso (
    id_curso INTEGER REFERENCES cursos(id_curso),
    id_recurso INTEGER REFERENCES recursos(id_recurso),
    cantidad_requerida INTEGER DEFAULT 1,
    PRIMARY KEY (id_curso, id_recurso)
);

CREATE TABLE bloques_horarios (
    id_bloque SERIAL PRIMARY KEY,
    dia_semana SMALLINT,
    hora_inicio TIME,
    hora_fin TIME,
    duracion_minutos INTEGER,
    orden_dia INTEGER,
    estado BOOLEAN DEFAULT TRUE
);

CREATE TABLE disponibilidad_docente (
    id_profesor INTEGER REFERENCES profesores(id_profesor),
    id_bloque INTEGER REFERENCES bloques_horarios(id_bloque),
    disponible BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (id_profesor, id_bloque)
);

CREATE TABLE preferencias_docente (
    id_profesor INTEGER REFERENCES profesores(id_profesor),
    id_bloque INTEGER REFERENCES bloques_horarios(id_bloque),
    valor_preferencia SMALLINT,
    observacion TEXT,
    PRIMARY KEY (id_profesor, id_bloque)
);

CREATE TABLE configuracion_optimizacion (
    id_configuracion SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    peso_horas_muertas_docente NUMERIC(8,3) DEFAULT 1,
    peso_horas_muertas_seccion NUMERIC(8,3) DEFAULT 1,
    peso_preferencias NUMERIC(8,3) DEFAULT 1,
    tiempo_limite_segundos INTEGER DEFAULT 60,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE horarios_generados (
    id_horario SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    id_periodo INTEGER REFERENCES periodos_academicos(id_periodo),
    id_configuracion INTEGER REFERENCES configuracion_optimizacion(id_configuracion),
    id_estado INTEGER REFERENCES catalogo_estados_horario(id_estado),
    fecha_generacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    valor_objetivo NUMERIC(12,2),
    tiempo_ejecucion_segundos NUMERIC(10,3)
);

CREATE TABLE asignaciones_horario (
    id_asignacion SERIAL PRIMARY KEY,
    id_horario INTEGER REFERENCES horarios_generados(id_horario),
    id_seccion INTEGER REFERENCES secciones(id_seccion),
    id_profesor INTEGER REFERENCES profesores(id_profesor),
    id_aula INTEGER REFERENCES aulas(id_aula),
    id_bloque INTEGER REFERENCES bloques_horarios(id_bloque)
);

CREATE INDEX idx_cursos_carrera_ciclo ON cursos(id_carrera, id_ciclo);
CREATE INDEX idx_secciones_periodo ON secciones(id_periodo);
CREATE INDEX idx_asignaciones_horario ON asignaciones_horario(id_horario);
CREATE INDEX idx_asignaciones_seccion ON asignaciones_horario(id_seccion);
CREATE INDEX idx_asignaciones_profesor ON asignaciones_horario(id_profesor);
CREATE INDEX idx_asignaciones_aula ON asignaciones_horario(id_aula);
