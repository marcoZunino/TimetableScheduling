from entities import *
import random
import pandas as pd

# funciones para cargar datos en entidades

"""
This module provides functions to manage and manipulate data related to 'materias', 'grupos', and 'profesores'.

Functions:
    add_materia(materias, id, nombre, carga_horaria, cantidad_dias, grupos=[], profesores=[], cantidad_profesores=1):
        Adds a new 'materia' to the list of 'materias'.
        
    add_grupo(grupos, anio, turno, carrera, particion, recurse):
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
    

def add_horario(horarios: list[Horario], inicio, fin, turnos):
    id = len(horarios)
    horarios.append(Horario(id, inicio, fin, turnos))

# crear grupo
def add_grupo(grupos, anio, turno, carrera, particion, recurse):
    id = len(grupos)
    grupos.append(Grupo(id, anio, turno, carrera, particion, bool(recurse)))

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

    

#buscar materias
"""
This module provides functions to filter and group subjects (materias) based on professors and groups.
Functions:
    materias_profesor(profesor, materias_total):
        Filters and returns a list of subjects taught by a specific professor.
    agrupar_materias(lista_materias):
        Groups subjects by their string representation and returns a dictionary where keys are subject names and values are lists of subjects.
    materias_grupo(grupo, materias_total):
        Filters and returns a list of subjects that belong to a specific group.
    materias_grupo_ids(grupo, materias_total):
        Filters and returns a list of subject IDs that belong to a specific group.
"""

def materias_profesor(profesor, materias_total):
    mats = []

    for m in materias_total:
        if profesor in m.profesores:
            mats.append(m)

    return mats

def agrupar_materias(lista_materias):
    lista_nombres = {}

    for m in lista_materias:
        if str(m) not in lista_nombres:
            lista_nombres[str(m)] = [m]
        else:
            lista_nombres[str(m)].append(m)

    return lista_nombres

def materias_grupo(grupo, materias_total):
    materias = []

    for m in materias_total:
        if grupo is not None and grupo in m.grupos:
            materias.append(m)
            
    return materias

def materias_grupo_ids(grupo, materias_total):
    materias_ids = []

    for m in materias_grupo(grupo, materias_total):
        if grupo is not None and grupo in m.grupos:
            materias_ids.append(m.id)
            
    return materias_ids

def electivas(materias):
    return [m for m in materias if m.electiva]

def bloques_horario_materia(materia, bloques_horario):
    ret = []
    for b_id in bloques_horario:
        if set(materia.turnos()).issubset(set(bloques_horario[b_id].horario.turnos)):
            ret.append(b_id)
    return ret

