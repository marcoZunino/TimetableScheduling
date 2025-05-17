-- script para definir la base de datos en PostgreSQL

-- actualizado al 16/05/2025

CREATE DATABASE horarios;

\c horarios

CREATE TABLE personas (
    cedula VARCHAR PRIMARY KEY,
    mail VARCHAR UNIQUE
);

CREATE TABLE profesores (
    nombre VARCHAR PRIMARY KEY,
    nombre_completo VARCHAR UNIQUE NULL,
    ultima_modificacion TIMESTAMP NULL,
    min_max_dias BOOLEAN DEFAULT NULL, -- TRUE = min, FALSE = max
    cedula VARCHAR NULL,
    FOREIGN KEY (cedula) REFERENCES personas(cedula)
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
    FOREIGN KEY (profesor) REFERENCES profesores(nombre),
    FOREIGN KEY (bloque_horario) REFERENCES bloques_horarios(id)
);

CREATE TABLE turnos (
    nombre VARCHAR PRIMARY KEY
);

CREATE TABLE turnos_horarios (
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    turno VARCHAR NOT NULL,
    excepcional BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (hora_inicio, hora_fin, turno),
    FOREIGN KEY (hora_inicio, hora_fin) REFERENCES horarios(hora_inicio, hora_fin),
    FOREIGN KEY (turno) REFERENCES turnos(nombre)
);

CREATE TABLE materias (
    -- codigo VARCHAR PRIMARY KEY,
    -- nombre VARCHAR UNIQUE NOT NULL,
    nombre VARCHAR PRIMARY KEY,
    nombre_completo VARCHAR UNIQUE
    -- cantidad_dias INT NOT NULL CHECK (cantidad_dias IN (0, 1, 2, 3, 4, 5)),
    -- carga_horaria INT NOT NULL CHECK (carga_horaria >= 0)
);

CREATE TABLE puede_dictar (
    profesor VARCHAR NOT NULL,
    materia VARCHAR NOT NULL,
    turno VARCHAR NOT NULL,
    grupos_max INT DEFAULT 1 CHECK (grupos_max > 0),
    PRIMARY KEY (profesor, materia, turno),
    FOREIGN KEY (profesor) REFERENCES profesores(nombre),
    FOREIGN KEY (materia) REFERENCES materias(nombre),
    FOREIGN KEY (turno) REFERENCES turnos(nombre)
);

-- cargar horarios
INSERT INTO horarios (hora_inicio, hora_fin) VALUES
('08:00', '08:50'),
('08:50', '09:40'),
('09:50', '10:40'),
('10:40', '11:30'),
('11:40', '12:30'),
('12:30', '13:20'),
('13:20', '14:10'),
('14:10', '15:00'),
('15:10', '16:00'),
('16:10', '17:00'),
('17:00', '17:50'),
('18:00', '18:50'),
('18:50', '19:40'),
('19:50', '20:40'),
('20:40', '21:30'),
('21:40', '22:30');

-- cargar bloques horarios
INSERT INTO bloques_horarios (dia, hora_inicio, hora_fin)
SELECT dia, hora_inicio, hora_fin
FROM (VALUES
    ('lun'),
    ('mar'),
    ('mie'),
    ('jue'),
    ('vie')
) AS dias(dia)
CROSS JOIN horarios;

INSERT INTO turnos (nombre) VALUES
('mañana'),
('tarde1'),
('tarde2'),
('noche');

-- cargar turnos de cada horario
INSERT INTO turnos_horarios (hora_inicio, hora_fin, turno) VALUES
('08:00', '08:50', 'mañana'),
('08:50', '09:40', 'mañana'),
('09:50', '10:40', 'mañana'),
('10:40', '11:30', 'mañana'),
('11:40', '12:30', 'mañana'),
('12:30', '13:20', 'mañana'),
('14:10', '15:00', 'tarde1'),
('15:10', '16:00', 'tarde1'),
('15:10', '16:00', 'tarde2'),
('16:10', '17:00', 'tarde1'),
('16:10', '17:00', 'tarde2'),
('17:00', '17:50', 'tarde1'),
('17:00', '17:50', 'tarde2'),
('18:00', '18:50', 'tarde1'),
('18:00', '18:50', 'tarde2'),
('18:00', '18:50', 'noche'),
('18:50', '19:40', 'tarde1'),
('18:50', '19:40', 'tarde2'),
('18:50', '19:40', 'noche'),
('19:50', '20:40', 'noche'),
('20:40', '21:30', 'noche'),
('21:40', '22:30', 'noche');

-- horarios excepcionales
INSERT INTO turnos_horarios (hora_inicio, hora_fin, turno, excepcional) VALUES
('13:20', '14:10', 'mañana', TRUE),
('14:10', '15:00', 'tarde2', TRUE),
('17:00', '17:50', 'noche', TRUE),
('19:50', '20:40', 'tarde2', TRUE);



