from .db_config import *
from ..entities import *


class Asignatura:
    def __init__(self, codigo, nombre, nombre_completo, carga_horaria: int, cantidad_dias: int):
        self.codigo = codigo
        self.nombre = nombre
        self.nombre_completo = nombre_completo
        self.carga_horaria = carga_horaria
        self.cantidad_dias = cantidad_dias


def write_profesores(connection, profesores: list[Profesor]):
    """
    Write professors to the database.
    """
    cursor = connection.cursor()

    for profesor in profesores:
        cursor.execute(f"""
                    INSERT INTO profesores (nombre, nombre_completo, min_max_dias)
                    VALUES ('{profesor.nombre}', '{profesor.nombre_completo}', {profesor.min_max_dias if profesor.min_max_dias else 'NULL'})
                    """)
        connection.commit()

        # for prioridad in profesor[3]:
        #     cursor.execute(f"""
        #                 INSERT INTO prioridades (profesor, bloque_horario, valor)
        #                 VALUES ('{profesor[0]}', {prioridad[0]}, {prioridad[2]})
        #                 """)
        #     connection.commit()

    cursor.close()

def write_materias(connection, asignaturas: list[Asignatura]):
    """
    Write subjects to the database.
    """
    cursor = connection.cursor()

    for materia in asignaturas:
        cursor.execute(f"""
                    INSERT INTO materias (codigo, nombre, nombre_completo, cantidad_dias, carga_horaria)
                    VALUES ('{materia.codigo}', '{materia.nombre}', '{materia.nombre_completo}', {materia.carga_horaria}, {materia.cantidad_dias})
                    """)
        connection.commit()

    cursor.close()




def write_solution():
    pass


