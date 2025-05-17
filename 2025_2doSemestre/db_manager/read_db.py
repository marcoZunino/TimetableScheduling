from .db_config import *
from openpyxl import Workbook


# leer materias
def read_materias(connection):
    cursor = connection.cursor()
    # cursor.execute("SELECT id, nombre FROM materias")
    # rows = cursor.fetchall()
    # materias = []
    # for row in rows:
    #     materias.append({"id": row[0], "nombre": row[1]})
    # return materias

# leer grupos

# leer profesores
def read_profesores(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT nombre, nombre_completo, min_max_dias FROM profesores")
    rows = cursor.fetchall()
    profesores = []
    for row in rows:
        nombre = row[0]
        cursor.execute(f"""
                    SELECT b.dia, b.hora_inicio, p.valor
                    FROM prioridades p, profesores prof, bloques_horarios b
                    WHERE p.profesor = prof.cedula
                    AND prof.nombre = '{nombre}'
                    AND p.bloque_horario = b.id
                    """)
        prioridades = cursor.fetchall()
        profesores.append([r for r in row] + [prioridades])
    return profesores

# leer horarios
def read_horarios(connection: psycopg2.extensions.connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM horarios")

    rows = cursor.fetchall()

    horarios = []

    for inicio, fin in rows:
        cursor.execute(f"""
                    SELECT t.turno, t.excepcional
                    FROM turnos_horarios t
                    WHERE t.hora_inicio = '{inicio}'
                    AND t.hora_fin = '{fin}'
                    """)
        data = cursor.fetchall()
        turnos = [t[0] for t in data]
        turnos_excepcional = [t[0] for t in data if t[1]]

        horarios.append((inicio, fin, turnos, turnos_excepcional))

    cursor.close()

    return horarios

def read_turnos(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT nombre FROM turnos")
    rows = cursor.fetchall()
    cursor.close()
    return [row[0] for row in rows]


def retrieve_all_data():
    connection = get_database_connection()
    # print(read_turnos(connection))


def write_prioridades_excel(dias, horarios, profesores):
    
    # Crear un libro de trabajo y una hoja
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Prioridades"

    # Escribir encabezados
    sheet["A1"] = "Profesor"
    for i, dia in enumerate(dias):
        sheet.cell(row=1, column=i + 2, value=dia)

    # # Escribir datos de profesores y prioridades
    # for i, profesor in enumerate(profesores):
    #     sheet.cell(row=i + 2, column=1, value=profesor.nombre)
    #     for j, dia in enumerate(dias):
    #         if dia in profesor.prioridades:
    #             sheet.cell(row=i + 2, column=j + 2, value="X")

    # Guardar el archivo
    workbook.save("prioridades.xlsx")



