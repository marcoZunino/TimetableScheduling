from entities import *
from variables import *

#imprimir
def print_timetable(dias, horarios, u_dict, w_dict, grupos, anios):
    """
    Prints the timetable for given days, schedules, groups, and years.

    Args:
        dias (list): List of days to be included in the timetable.
        horarios (list): List of schedules to be included in the timetable.
        u_dict (dict): Dictionary containing information about subjects.
        w_dict (dict): Dictionary containing information about professors.
        grupos (list): List of groups to be included in the timetable.
        anios (list): List of years to be included in the timetable.

    """
    for a in anios:
        print('\n', '-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -')
        print("Año: ", str(a))
        # filtrar grupos dentro del año
        for g in grupos_anio(grupos, a):
            print('\n', "Grupo: ", str(g))
            print('\t', *[str(d) for d in dias], sep='\t\t')
            print('··········································································································')
            for h in horarios_turno(horarios, g.turno):
                mats = [search_materia(BloqueHorario(d,h), g, u_dict) for d in dias]
                lista = []
                for ms in mats:
                    if len(ms) == 0:
                        lista.append("---")
                    else:
                        # mostrar profesor:
                        # ps = search_profesor(m, w_dict)
                        # lista.append([str(m) + " " + str(*[str(p) for p in search_profesor(m, w_dict)]) for m in ms])
                        # lista.append("/".join(map(str, [str(m) + " " + str(*[str(p) for p in search_profesor(m, w_dict)]) for m in ms])))
                        lista.append("/".join(map(str, ms)))
                        
                print(str(h), *lista, sep='\t\t')

def print_prof_timetable(dias, horarios, u_dict, w_dict, profesores, materias):
    """
    Prints the timetable for each professor.

    Parameters:
    dias (list): List of days to include in the timetable.
    horarios (list): List of time slots to include in the timetable.
    u_dict (dict): Dictionary containing university-related data.
    w_dict (dict): Dictionary containing week-related data.
    profesores (list): List of professor objects.
    materias (list): List of subject objects.
    """
    for p in profesores:
        if len(intersection([m.nombre for m in materias], p.materias())) == 0:
            continue
        print('\n', "Profesor: ", str(p))
        print('\t', *[str(d) for d in dias], sep='\t')
        print('·····················································')
        for h in horarios:
            mats = [search_materia_prof(BloqueHorario(d,h), p, u_dict, w_dict, materias) for d in dias]
            lista = []
            for m in mats:
                if m is None:
                    lista.append("---")
                else:
                    lista.append(str(m))
            if len([l for l in lista if l != "---"]) > 0:
                print(str(h), *lista, sep='\t')
            

def intersection(array1, array2):
    ret = []
    for i in array1:
        if i in array2:
            ret.append(i)
    return ret

def print_prioridades(dias: list[Dia], horarios: list[Horario], profesores: list[Profesor]):
    for p in profesores:
        print('\n', "Profesor:", str(p), p.nombre_completo)
        print('\t', *[str(d) for d in dias], sep='\t')
        print('·····················································')
        for h in horarios:
            prioridades = [str(search_prioridad(BloqueHorario(d,h),p)) for d in dias]
            print(str(h), *prioridades, sep='\t')


def search_materia(b, g, u_dict: dict[tuple, u]) -> list[Materia]:
    """
    Searches for a 'materia' object in the given dictionary of 'u' objects that matches the specified criteria.

    Args:
        b (str): The schedule (horario) to match.
        g (str): The group (grupo) to match within the 'materia'.
        u_dict (dict): A dictionary where keys are 'u' object IDs and values are 'u' objects.

    Returns:
        materia: The 'materia' object that matches the specified schedule and group, and has a variable 'x' rounded to 1.
        None: If no matching 'materia' object is found.
    """
    ms = []
    for u_id in u_dict:
        u_obj = u_dict[u_id]
        if u_obj.horario == b and g in u_obj.materia.grupos and round(u_obj.variable.x) == 1:
            ms.append(u_obj.materia)
    return ms

def search_profesor(materia: Materia, w_dict: dict[tuple, w]) -> list[Profesor]:
    """
    Searches for professors assigned to a given subject based on a weight dictionary.
    Args:
        materia (object): The subject object which contains a list of professors.
        w_dict (dict): A dictionary with keys as tuples of (subject_id, professor_id) and values as objects 
                       containing a variable attribute with an x property.
    Returns:
        list: A list of professors assigned to the given subject.
    """
    
    if materia is None:
        return []
    
    ps = []
    for p in materia.profesores:
        if round(w_dict[materia.id, p.id].variable.x) == 1:
            ps.append(p)
    return ps

def search_profesor_by_nombre(profesores: list[Profesor], nombre) -> Profesor:
    for p in profesores:
        if p.nombre == nombre:
            return p
    return None

def search_materias_by_nombre(materias: list[Materia], nombre) -> list[Materia]:
    ret = []
    for m in materias:
        if m.nombre == nombre:
            ret.append(m)
    return ret
    
def search_materia_prof(b: BloqueHorario, p: Profesor, u_dict: dict[tuple, u], w_dict: dict[tuple, w], materias: list[Materia]) -> Materia:
    """
    Searches for a 'materia' (subject) that matches the given block and professor.
    Args:
        b: The block to search within.
        p: The professor to search for.
        u_dict (dict): A dictionary where keys are 'materia' IDs and values are objects containing scheduling information.
        w_dict (dict): A dictionary where keys are tuples of 'materia' and professor IDs, and values are objects containing assignment information.
        materias (list): A list of 'materia' objects to search through.
    Returns:
        The 'materia' object that matches the given block and professor, or None if no match is found.
    """
    for m in materias:
        if round(w_dict[m.id, p.id].variable.x * u_dict[m.id, b.id].variable.x) == 1:
            return m
    #     ps = search_profesor(u_obj.materia, w_dict)
    #     if bloque == b and p in ps and round(u_obj.variable.x) == 1:
    #         return u_obj.materia

    # for u_id in u_dict:
    #     u_obj = u_dict[u_id]
    #     bloque = u_obj.horario
    #     ps = search_profesor(u_obj.materia, w_dict)
    #     if bloque == b and p in ps and round(u_obj.variable.x) == 1:
    #         return u_obj.materia
    return None

def search_prioridad(b: BloqueHorario, p: Profesor):
    if b in p.no_disponible:
        return "-"
    for pr in p.prioridades:
        if pr.bloque_horario == b:
            return pr.value
        
def grupos_anio(grupos: list[Grupo], anio) -> list[Grupo]:
    """
    Filters a list of groups by a specific year.

    Args:
        grupos (list): A list of group objects, where each object has an 'anio' attribute.
        anio (int): The year to filter the groups by.

    Returns:
        list: A list of group objects that match the specified year.
    """
    gs = []
    for g in grupos:
        if g.anio == anio:
            gs.append(g)
    return gs

def horarios_turno(horarios: list[Horario], turno) -> list[Horario]:
    """
    Filters a list of schedule objects based on a specified shift.

    Args:
        horarios (list): A list of schedule objects. Each object should have a 'turnos' attribute.
        turno (str): The shift to filter by.

    Returns:
        list: A list of schedule objects that include the specified shift.
    """
    hs = []
    for h in horarios:
        if turno in h.turnos:
            hs.append(h)
    return hs

def horarios_ids_turno(horarios: list[Horario], turno):
    return [h.id for h in horarios_turno(horarios, turno)]


###########################################################################

# imprimir para mostrar en Excel
def print_timetable_excel(dias, horarios, u_dict, w_dict, grupos, anios, show_profs=True):
    for a in anios:
        print('\n', '-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -')
        print("Año: ", str(a))
        # filtrar grupos dentro del año
        for g in grupos_anio(grupos, a):
            print('\n', "Grupo: ", str(g))
            # print('\t', *[str(d) for d in dias], sep='\t\t')
            print('', *[str(d) for d in dias], sep='\t')
            for h in horarios_turno(horarios, g.turno):
                mats = [search_materia(BloqueHorario(d,h), g, u_dict) for d in dias]
                lista = []
                for ms in mats:
                    if len(ms) == 0:
                        lista.append("---")
                    else:
                        # mostrar profesor:
                        # ps = search_profesor(m, w_dict)
                        # lista.append([str(m) + " " + str(*[str(p) for p in search_profesor(m, w_dict)]) for m in ms])
                        # print_list = [str(m) + str([str(p) for p in search_profesor(m, w_dict)]) for m in ms]
                        if show_profs:
                            print_list = [str(m) + "[" + ",".join(map(str, [str(p) for p in search_profesor(m, w_dict)])) + "]" for m in ms]
                        else:
                            print_list = [str(m) for m in ms]
                        lista.append("/".join(map(str, print_list)))
                        # lista.append(print_list)
                        # lista.append("/".join(map(str, ms)))
                        
                # print(str(h), *lista, sep='\t\t')
                print(str(h), *lista, sep='\t')


def print_prof_timetable_excel(dias, horarios, u_dict, w_dict, profesores, materias):
    for p in profesores:
        if len(intersection([m.nombre for m in materias], p.materias())) == 0:
            continue
        print('\n', "Profesor: ", str(p), p.nombre_completo)
        print('', *[str(d) for d in dias], sep='\t')
        for h in horarios:
            mats = [search_materia_prof(BloqueHorario(d,h), p, u_dict, w_dict, materias) for d in dias]
            lista = []
            for m in mats:
                if m is None:
                    lista.append("---")
                else:
                    lista.append(str(m))
            if len([l for l in lista if l != "---"]) > 0:
                print(str(h), *lista, sep='\t')

def print_timetable_salones(dias, horarios, niveles):
    print('\t', *[str(d) for d in dias], sep='\t')
    print('··········································································································')
    for h in horarios:
        lista = [str(niveles[d.id, h.id])+"%" for d in dias]
        print(str(h), *lista, sep='\t')



