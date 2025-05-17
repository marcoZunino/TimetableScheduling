from entities import *
from variables import *
import random
import pandas as pd
from gurobipy import *
import gurobipy as gp

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
def add_materia(materias: list[Materia], id, nombre, nombre_completo, carga_horaria, cantidad_dias, grupos: list[Grupo] = [], profesores: list[Profesor] = [], cantidad_profesores=1, electiva=False, teo_prac=None):
    # id = len(materias)
    try:
        carga_horaria = int(carga_horaria)
    except:
        carga_horaria = 0
    try:
        cantidad_dias = int(cantidad_dias)
    except:
        cantidad_dias = 0
    materias.append(Materia(id, nombre, nombre_completo, carga_horaria=carga_horaria, cantidad_dias=cantidad_dias,
                            grupos=grupos, profesores=profesores, cantidad_profesores=cantidad_profesores,
                            electiva=electiva, teo_prac=teo_prac))
    

def add_horario(horarios: list[Horario], inicio, fin, turnos, turnos_excepcional):
    id = len(horarios)
    horarios.append(Horario(id, inicio, fin, turnos, turnos_excepcional))

# crear grupo
def add_grupo(grupos: list[Grupo], anio, turno, carrera, particion, recurse):
    id = len(grupos)
    grupos.append(Grupo(id, anio, turno, carrera, particion, bool(recurse)))

# crear profesor
def add_profesor(profesores: list[Profesor], id, nombre, min_max_dias=None, nombre_completo=None, cedula=None, mail=None):
    # id = len(profesores)
    profesor = Profesor(id, nombre, min_max_dias, nombre_completo, cedula, mail)
    if not profesor in profesores:
        profesores.append(profesor)

def lista_profesores(profesores: list[Profesor], nombres):
    return [p for p in profesores if str(p) in nombres]

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


def fixed_pr(bloques_horario: dict[tuple, BloqueHorario], value):
    return [[b, value] for b in bloques_horario]

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

def calcular_super(m1: Materia, m2: Materia):
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

def copy_variables_excel(u_dict: dict[tuple, u], w_dict: dict[tuple, w], output):

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

def materias_profesor(profesor: Profesor, materias_total: list[Materia]):
    return [m for m in materias_total if profesor in m.profesores]

def agrupar_materias(lista_materias):
    lista_nombres = {}

    for m in lista_materias:
        if str(m) not in lista_nombres:
            lista_nombres[str(m)] = [m]
        else:
            lista_nombres[str(m)].append(m)

    return lista_nombres

def materias_grupo(grupo: Grupo, materias_total: list[Materia]):            
    return [m for m in materias_total if m.grupos.count(grupo) > 0]

def electivas(materias: list[Materia]):
    return [m for m in materias if m.electiva]

def bloques_horario_materia(materia: Materia, bloques_horario: dict[tuple, BloqueHorario]):
    ret = []
    for b_id in bloques_horario:
        if set(materia.turnos()).issubset(set(bloques_horario[b_id].horario.turnos)):
            ret.append(b_id)
    return ret


# variables
"""
This script initializes and populates several dictionaries to map combinations of entities 
(materias, bloques_horario, dias, profesores, and grupos) to corresponding function outputs.
Variables:
    u_dict (dict): Maps tuples of (materia.id, bloque_horario) to the result of function u(m, bloques_horario[b_id]).
    v_dict (dict): Maps tuples of (materia.id, dia.id) to the result of function v(m, d).
    w_dict (dict): Maps tuples of (materia.id, profesor.id) to the result of function w(m, p).
    x_dict (dict): Maps tuples of (grupo.id, bloque_horario) to the result of function x(g, bloques_horario[b_id]).
    y_dict (dict): Maps tuples of (profesor.id, bloque_horario) to the result of function y(p, bloques_horario[b_id]).
    z_dict (dict): Maps tuples of (profesor.id, dia.id) to the result of function z(p, d).
Prints:
    The length of each dictionary after it has been populated.
"""
def initialize_variables(materias: list[Materia], bloques_horario: dict[tuple, BloqueHorario], dias: list[Dia], profesores: list[Profesor], grupos: list[Grupo]):
    u_dict = {}
    for m in materias:
        for b_id in bloques_horario:
            u_dict[(m.id, b_id)] = u(m, bloques_horario[b_id])
    print("u: ", len(u_dict))

    v_dict = {}
    for m in materias:
        for d in dias:
            v_dict[(m.id, d.id)] = v(m, d)
    print("v: ", len(v_dict))

    w_dict = {}
    for m in materias:
        for p in profesores:
            w_dict[(m.id, p.id)] = w(m, p)
    print("w: ", len(w_dict))

    x_dict = {}
    for g in grupos:
        for b_id in bloques_horario:
            x_dict[(g.id, b_id)] = x(g, bloques_horario[b_id])
    print("x: ", len(x_dict))

    y_dict = {}
    for p in profesores:
        for b_id in bloques_horario:
            y_dict[(p.id, b_id)] = y(p, bloques_horario[b_id])
    print("y: ", len(y_dict))

    z_dict = {}
    for p in profesores:
        for d in dias:
            z_dict[(p.id, d.id)] = z(p, d)
    print("z: ", len(z_dict))

    return u_dict, v_dict, w_dict, x_dict, y_dict, z_dict


# Create variables
"""
This script creates binary decision variables for multiple dictionaries using the Gurobi optimization model.
Variables:
    u_dict (dict): Dictionary containing elements for which binary variables "u" are created.
    v_dict (dict): Dictionary containing elements for which binary variables "v" are created.
    w_dict (dict): Dictionary containing elements for which binary variables "w" are created.
    x_dict (dict): Dictionary containing elements for which binary variables "x" are created.
    y_dict (dict): Dictionary containing elements for which binary variables "y" are created.
    z_dict (dict): Dictionary containing elements for which binary variables "z" are created.
Each element in the dictionaries is assigned a binary variable using the Gurobi model's `addVar` method.
"""

# u_vars = m.addMVar(shape=len(u_dict), vtype=GRB.BINARY, name="u") # variable matrix

def create_variables(model: gp.Model, u_dict: dict[tuple, u], v_dict: dict[tuple, v], w_dict: dict[tuple, w], x_dict: dict[tuple, x], y_dict: dict[tuple, y], z_dict: dict[tuple, z]):
    
    for u_i in u_dict: # crear variables "u" a partir de u_dict
        u_dict[u_i].variable = model.addVar(vtype=GRB.BINARY, name=str(u_dict[u_i]))

    for v_i in v_dict: # crear variables "v" a partir de v_dict
        v_dict[v_i].variable = model.addVar(vtype=GRB.BINARY, name=str(v_dict[v_i]))

    for w_i in w_dict: # crear variables "v" a partir de v_dict
        w_dict[w_i].variable = model.addVar(vtype=GRB.BINARY, name=str(w_dict[w_i]))


    for x_i in x_dict: # crear variables "x" a partir de x_dict
        x_dict[x_i].variable = model.addVar(vtype=GRB.BINARY, name=str(x_dict[x_i]))

    for y_i in y_dict: # crear variables "y" a partir de y_dict
        y_dict[y_i].variable = model.addVar(vtype=GRB.BINARY, name=str(y_dict[y_i]))

    for z_i in z_dict: # crear variables "z" a partir de z_dict
        z_dict[z_i].variable = model.addVar(vtype=GRB.BINARY, name=str(z_dict[z_i]))


