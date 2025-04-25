from entities import *
import random
import pandas as pd

# cargar datos
"""
This module provides functions to manage and manipulate data related to 'materias', 'grupos', and 'profesores'.

Functions:
    add_materia(materias, id, nombre, carga_horaria, cantidad_dias, grupos=[], profesores=[], cantidad_profesores=1):
        Adds a new 'materia' to the list of 'materias'.
        
    add_grupo(grupos, anio, turno, carrera, particion, recurse, aux):
        Adds a new 'grupo' to the list of 'grupos'.
        
    add_profesor(profesores, id, nombre, min_max_dias=None):
        Adds a new 'profesor' to the list of 'profesores'.
        
    lista_profesores(profesores, nombres):
        Returns a list of 'profesores' matching the given names.
        
    lista_grupos(grupos, nombres):
        Returns a list of 'grupos' matching the given names.
"""

# crear materia
def add_materia(materias, id, nombre, carga_horaria, cantidad_dias, grupos=[], profesores=[], cantidad_profesores=1, electiva=False, teo_prac=None):
    # id = len(materias)
    try:
        carga_horaria = int(carga_horaria)
    except:
        carga_horaria = 0
    try:
        cantidad_dias = int(cantidad_dias)
    except:
        cantidad_dias = 0
    materias.append(Materia(id, nombre, carga_horaria=carga_horaria, cantidad_dias=cantidad_dias,
                            grupos=grupos, profesores=profesores, cantidad_profesores=cantidad_profesores,
                            electiva=electiva, teo_prac=teo_prac))

# crear grupo
def add_grupo(grupos, anio, turno, carrera, particion, recurse, aux):
    id = len(grupos)
    grupos.append(Grupo(id, anio, turno, carrera, particion, bool(recurse), bool(aux)))

# crear profesor
def add_profesor(profesores, id, nombre, min_max_dias=None, nombre_completo=None):
    # id = len(profesores)
    profesor = Profesor(id, nombre, min_max_dias, nombre_completo)
    if not profesor in profesores:
        profesores.append(profesor)

def lista_profesores(profesores, nombres):
    profs = []
    for n in nombres:
        for p in profesores:
            if str(p) == n:
                profs.append(p)
                break
    return profs

def lista_grupos(grupos, nombres):
    gs = []
    for n in nombres:
        for g in grupos:
            if str(g) == n:
                gs.append(g)
                break
    return gs


#prioridades

"""
Generates a fixed priority array for the given time blocks with the specified priority value.
Args:
    bloques_horario (list): A list of time blocks.
    value (int): The fixed priority value to be assigned to each time block.
Returns:
    list: A list of lists where each inner list contains a time block and the specified priority value.
"""


def update_no_disp(profesor, bloques_horario, no_disp_index):
    for i in no_disp_index:
        if bloques_horario[i] not in profesor.no_disponible:
            profesor.no_disponible.append(bloques_horario[i])
"""
Updates the 'no_disponible' list of a professor by adding the specified time blocks.
Args:
    profesor (Profesor): The professor whose availability is being updated.
    bloques_horario (list): A list of time blocks.
    no_disp_index (list): A list of indices indicating which time blocks the professor is not available for.
"""


def update_prioridad(profesor, bloques_horario, array_prioridad):

    if profesor is None: return
    
    # reset:
    profesor.prioridades = []
    profesor.no_disponible = []

    """
    Updates the priority list of a professor based on the given priority array.
    Args:
        profesor (Profesor): The professor whose priorities are being updated.
        bloques_horario (list): A list of time blocks.
        array_prioridad (list): A list of tuples where each tuple contains a time block index and a priority value.
    """
    # array_prioridad[i] = [(d,h),a]
    for i in array_prioridad:
        b_id = i[0]
        value = i[1]
    
        if value == 0:
            update_no_disp(profesor, bloques_horario, [b_id])
        
        prior = Prioridad(value, bloques_horario[b_id], profesor = profesor)
        if not (prior in profesor.prioridades):
            profesor.prioridades.append(prior)

def random_pr(bloques_horario):
    pr_array = []
    for b in bloques_horario:
        pr_array.append([b, random.randint(0,3)])
    return pr_array
"""
Generates a random priority array for the given time blocks.
Args:
    bloques_horario (list): A list of time blocks.
Returns:
    list: A list of lists where each inner list contains a time block and a random priority value between 0 and 3.
"""


def fixed_pr(bloques_horario, value):
    pr_array = []
    for b in bloques_horario:
        pr_array.append([b, value])
    return pr_array

"""
Generates a fixed priority array for the given time blocks with the specified priority value.
Args:
    bloques_horario (list): A list of time blocks.
    value (int): The fixed priority value to be assigned to each time block.
Returns:
    list: A list of lists where each inner list contains a time block and the specified priority value.
"""


#superposicion
"""
Calculate the overlap between two given objects.

This function checks if two objects, `m1` and `m2`, are the same or if they have any common groups.
It returns a `Superposicion` object indicating the type of overlap.

Parameters:
m1 (object): The first object to compare. It should have an attribute `grupos` which is a list of groups.
m2 (object): The second object to compare. It should have an attribute `grupos` which is a list of groups.

Returns:
Superposicion: An object representing the overlap. If `m1` and `m2` are the same, it returns `Superposicion(0, m1, m2)`.
               If they share any common groups, it returns `Superposicion(1, m1, m2)`. Otherwise, it returns `Superposicion(0, m1, m2)`.
"""

def calcular_super(m1, m2):
    if m1 == m2:
        return Superposicion(0, m1, m2)
    else:
        s = False
        for g1 in m1.grupos:
            if g1 in m2.grupos:
                s = True
                break
        return Superposicion(1 if s else 0, m1, m2)
    
def fix_super(value, superposicion, mats1, mats2):
    for m1 in mats1:
        for m2 in mats2:
            if m1 != m2:
                superposicion[(m1.id, m2.id)] = Superposicion(value, m1, m2)
                superposicion[(m2.id, m1.id)] = Superposicion(value, m2, m1)
    

#copiar resultados de variables a hoja de excel

def copy_variables_excel(u_dict, w_dict, output):

    data_u = {
        'materia': [],
        'dia': [],
        'horario': [],
        'U': []
    }
    for u_i in u_dict:
        data_u['materia'].append(u_dict[u_i].materia.id)
        data_u['dia'].append(u_dict[u_i].horario.dia.id)
        data_u['horario'].append(u_dict[u_i].horario.horario.id)
        data_u['U'].append(round(u_dict[u_i].variable.x))

    data_w = {
        'materia': [],
        'profesor': [],
        'W': []
    }
    for w_i in w_dict:
        data_w['materia'].append(w_dict[w_i].materia.id)
        data_w['profesor'].append(w_dict[w_i].profesor.id)
        data_w['W'].append(round(w_dict[w_i].variable.x))

    with pd.ExcelWriter(output) as writer:
        pd.DataFrame(data_u).to_excel(writer, sheet_name="u", index=False)
        pd.DataFrame(data_w).to_excel(writer, sheet_name="w", index=False)

    