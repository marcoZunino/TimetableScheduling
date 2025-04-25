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

# leer horarios

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



