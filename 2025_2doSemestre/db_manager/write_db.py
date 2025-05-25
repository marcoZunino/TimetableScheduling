from .db_config import *
from entities import Profesor, Materia



def write_profesores(connection: psycopg2.extensions.connection, profesores: list[Profesor]):
    """
    Write professors to the database.
    """
    cursor = connection.cursor()

    for profesor in profesores:
        
        min_max = 'NULL'
        match profesor.min_max_dias:
            case "min":
                min_max = True
            case "max":
                min_max = False

        cedula = profesor.cedula if profesor.cedula else 'NULL'

        cursor.execute(f"""
                    INSERT INTO profesores (nombre, nombre_completo, min_max_dias, cedula)
                    VALUES ('{profesor.nombre}', '{profesor.nombre_completo}', {min_max}, {cedula})
                    ON CONFLICT (nombre)
                        DO UPDATE SET
                            nombre_completo = EXCLUDED.nombre_completo,
                            min_max_dias = EXCLUDED.min_max_dias,
                            cedula = EXCLUDED.cedula;
                    """)
        connection.commit()

        # for prioridad in profesor[3]:
        #     cursor.execute(f"""
        #                 INSERT INTO prioridades (profesor, bloque_horario, valor)
        #                 VALUES ('{profesor[0]}', {prioridad[0]}, {prioridad[2]})
        #                 """)
        #     connection.commit()

    cursor.close()


# class Asignatura:
#     def __init__(self, nombre, nombre_completo, carga_horaria: int, cantidad_dias: int):
#         # self.codigo = codigo
#         self.nombre = nombre
#         self.nombre_completo = nombre_completo
#         self.carga_horaria = carga_horaria
#         self.cantidad_dias = cantidad_dias


def write_materias(connection: psycopg2.extensions.connection, materias: list[Materia], profesores: list[Profesor]):

    """
    Write subjects to the database.
    """
    cursor = connection.cursor()

    materias_rows = []

    for profesor in profesores:
        
        for mat in profesor.lista_materias:

            nombre = mat["nombre_materia"]
            materia_obj = [m for m in materias if m.nombre == nombre][0]
            nombre_completo = materia_obj.nombre_completo
            cant_grupos = mat["grupos_max"]


            if nombre not in materias_rows:
                materias_rows.append(nombre)
                cursor.execute(f"""
                    INSERT INTO materias (nombre, nombre_completo)
                    VALUES ('{nombre}', '{nombre_completo}')
                    ON CONFLICT (nombre) DO NOTHING
                    """)
                connection.commit()

            for t in materia_obj.turnos():
                cursor.execute(f"""
                    INSERT INTO puede_dictar (profesor, materia, turno, grupos_max)
                    VALUES ('{profesor.nombre}', '{nombre}', '{t}', {cant_grupos})
                    ON CONFLICT (profesor, materia, turno) DO NOTHING
                    """)
                connection.commit()
    # asignaturas: list[Asignatura] = []




    # for materia in asignaturas:
    #     cursor.execute(f"""
    #                 INSERT INTO materias (nombre, nombre_completo, cantidad_dias, carga_horaria)
    #                 VALUES ('{materia.nombre}', '{materia.nombre_completo}', {materia.carga_horaria}, {materia.cantidad_dias})
    #                 """)
    #     connection.commit()

    cursor.close()

def write_prioridades(connection: psycopg2.extensions.connection, profesor: Profesor):
    """
    Write priorities to the database.
    """
    cursor = connection.cursor()

    for prioridad in profesor.prioridades:
        
        dia = prioridad.bloque_horario.dia
        hora_inicio = prioridad.bloque_horario.horario.inicio

        cursor.execute(f"""
                    INSERT INTO prioridades (profesor, bloque_horario, valor)
                    SELECT '{profesor.nombre}', b.id, {prioridad.value}
                    FROM bloques_horarios b
                    WHERE '{dia}' = b.dia AND '{hora_inicio}' = b.hora_inicio
                    ON CONFLICT (profesor, bloque_horario) 
                        DO UPDATE SET valor = EXCLUDED.valor;
                    """)
        connection.commit()

        cursor.execute(f"""
                    UPDATE profesores
                    SET ultima_modificacion = NOW()::timestamp WITHOUT TIME ZONE
                    WHERE nombre = '{profesor.nombre}'
                    """)

    cursor.close()



def write_solution():
    pass


