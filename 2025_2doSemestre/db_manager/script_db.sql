-- script para definir la base de datos en PostgreSQL

-- actualizado al 24/04/2025 21:26

CREATE TABLE profesores (
    cedula VARCHAR PRIMARY KEY,
    nombre VARCHAR UNIQUE NOT NULL,
    nombre_completo VARCHAR UNIQUE,
    min_max_dias VARCHAR CHECK (min_max_dias IN ('min', 'max')),
    mail VARCHAR
);

CREATE TABLE horarios (
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    PRIMARY KEY (hora_inicio, hora_fin),
    CHECK (hora_fin > hora_inicio)
);

CREATE TABLE bloques_horarios (
    id SERIAL PRIMARY KEY,
    dia VARCHAR NOT NULL CHECK (dia IN ('lun', 'mar', 'mie', 'jue', 'vie')),
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    FOREIGN KEY (hora_inicio, hora_fin) REFERENCES horarios(hora_inicio, hora_fin)
);

CREATE TABLE prioridades (
    profesor VARCHAR NOT NULL,
    bloque_horario INT NOT NULL,
    valor INT CHECK (valor IN (0, 1, 2, 3)),
    PRIMARY KEY (profesor, bloque_horario),
    FOREIGN KEY (profesor) REFERENCES profesores(cedula),
    FOREIGN KEY (bloque_horario) REFERENCES bloques_horarios(id)
);

CREATE TABLE turnos (
    nombre VARCHAR PRIMARY KEY
);

CREATE TABLE turnos_horarios (
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    turno VARCHAR NOT NULL,
    PRIMARY KEY (hora_inicio, hora_fin, turno),
    FOREIGN KEY (hora_inicio, hora_fin) REFERENCES horarios(hora_inicio, hora_fin),
    FOREIGN KEY (turno) REFERENCES turnos(nombre)
);

CREATE TABLE materias (
    codigo VARCHAR PRIMARY KEY,
    nombre VARCHAR UNIQUE NOT NULL,
    nombre_completo VARCHAR UNIQUE,
    cantidad_dias INT NOT NULL CHECK (cantidad_dias IN (0, 1, 2, 3, 4, 5)),
    carga_horaria INT NOT NULL CHECK (carga_horaria >= 0)
);

CREATE TABLE puede_dictar (
    profesor VARCHAR NOT NULL,
    materia VARCHAR NOT NULL,
    grupos_max INT DEFAULT 1 CHECK (grupos_max > 0),
    PRIMARY KEY (profesor, materia),
    FOREIGN KEY (profesor) REFERENCES profesores(cedula),
    FOREIGN KEY (materia) REFERENCES materias(codigo)
);

