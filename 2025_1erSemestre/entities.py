import math

class Dia:
    def __init__(self, id: int, nombre: str):
        self.id = id
        self.nombre = nombre

    def __str__(self) -> str:
        return self.nombre
        # return self.id
    
    def __eq__(self, __value: object) -> bool:
        return type(__value) == type(self) and self.nombre == __value.nombre
 
class Horario:
    def __init__(self, id: int, inicio: str, fin: str, turnos=[]):
        self.id = id
        self.inicio = str(inicio)
        self.fin = str(fin)
        self.turnos = turnos # [str]

    def __str__(self) -> str:
        return self.inicio + "-" + self.fin
        # return self.id
    
    def __eq__(self, __value: object) -> bool:
        return type(__value) == type(self) and self.inicio == __value.inicio and self.fin == __value.fin

class Grupo:
    def __init__(self, id: int, anio: int=None, turno: str=None, carrera: str=None, particion: int=None, recurse: bool=False, aux=None) -> None:
        self.id = id
        self.anio = anio
        self.turno = turno
        self.carrera = carrera
        self.particion = particion
        self.recurse = recurse
        self.aux = aux

    def __str__(self) -> str:
        st = ""
        # st += str(self.id) + "_"
        st += str(self.anio) if self.anio is not None else ""
        st += str(self.carrera) if self.carrera is not None else ""
        st += "REC" if self.recurse else ""
        st += str(self.particion) if self.particion is not None else ""
        st += str(self.aux) if self.aux is not None else ""
        # st += str(self.turno) if self.turno is not None else ""
        return st

    def __eq__(self, __value: object) -> bool:
        return type(__value) == type(self) and self.id == __value.id and self.anio == __value.anio
    
class BloqueHorario:
    def __init__(self, dia: Dia, horario: Horario) -> None:
        self.dia = dia
        self.horario = horario
        
    def __str__(self) -> str:
        return str(self.dia) + "_" + str(self.horario)
    
    def __eq__(self, __value: object) -> bool:
        return type(__value) == type(self) and self.dia == __value.dia and self.horario == __value.horario
    
    def id(self):
        return (self.dia.id, self.horario.id)

class Profesor:
    def __init__(self, id: int, nombre: str, minimizar_dias: bool = False):
        self.id = id
        self.nombre = nombre
        self.no_disponible = []
        self.prioridades = []
        self.lista_materias = [] # lista_materias[i] = (nombre_materia: str, max_grupos: int)
        self.minimizar_dias = minimizar_dias

    def __str__(self) -> str:
        return self.nombre

    def __eq__(self, __value: object) -> bool:
        return type(__value) == type(self) and self.nombre == __value.nombre
    
    def materias(self):
        ms = []
        for i in self.lista_materias:
            ms.append(i["nombre_materia"])
        return ms

class Materia:
    def __init__(self,
                 id: int,
                 nombre: str,
                 carga_horaria: int=None,
                 cantidad_dias: int=3,
                 grupos = [],
                 profesores = [],
                 cantidad_profesores = 1,
                 ) -> None:
        
        self.nombre = nombre
        self.id = id
        self.carga_horaria = carga_horaria  #C_m
        self.cantidad_dias = cantidad_dias  #D_m
        self.grupos = grupos
        self.profesores = profesores
        self.no_disponible = []
        self.prioridades = []
        self.cantidad_profesores = cantidad_profesores
        
    def __str__(self) -> str:
        # if self.grupo is not None:
        #     return self.nombre + " " + str(self.grupo)
        return self.nombre
    
    def __eq__(self, __value: object) -> bool:
        return type(__value) == type(self) and self.id == __value.id
    
    # def anio(self):
    #     if self.grupo is not None:
    #         return self.grupo.anio

    # H_max
    def horas_max(self) -> int:
        if self.cantidad_dias == 0:
            return 0
        return math.ceil(self.carga_horaria / self.cantidad_dias)
    
    # H_min
    def horas_min(self) -> int:
        if self.cantidad_dias == 0:
            return 0
        return math.floor(self.carga_horaria / self.cantidad_dias)
    
    def turnos(self):
        turnos = []
        for g in self.grupos:
            if g.turno is not None and g.turno not in turnos:
                turnos.append(g.turno)
        return turnos
    
    def anios(self):
        anios = []
        for g in self.grupos:
            if g.anio is not None and g.anio not in anios:
                anios.append(g.anio)
        return anios

class Prioridad:
    def __init__(self, value: int, bloque_horario: BloqueHorario, profesor: Profesor = None, materia: Materia = None) -> None:
        self.value = value
        self.profesor = profesor
        self.materia = materia
        self.bloque_horario = bloque_horario
    
    def __str__(self) -> str:
        if (not self.profesor is None):
            return str(self.profesor) + "_" + str(self.bloque_horario) + ":prioridad=" + str(self.value)
        elif (not self.materia is None):
            return str(self.materia) + "_" + str(self.bloque_horario) + ":prioridad=" + str(self.value)
        else:
            return "error"
    
    def __eq__(self, __value: object) -> bool:
        if (not self.profesor is None):
            return type(__value) == type(self) and self.profesor == __value.profesor and self.bloque_horario == __value.bloque_horario
        if (not self.materia is None):
            return type(__value) == type(self) and self.materia == __value.materia and self.bloque_horario == __value.bloque_horario
        
    
    def id(self):
        if (not self.profesor is None):
            return (self.profesor.id, self.bloque_horario.id())
        if (not self.materia is None):
            return (self.materia.id, self.bloque_horario.id())
        
    
class Superposicion:
    def __init__(self, value: int, materia1: Materia, materia2: Materia) -> None:
        self.value = value
        self.materia1 = materia1
        self.materia2 = materia2
    
    def __str__(self) -> str:
        return "s_" + str(self.materia1) + "," + str(self.materia2) + "=" + str(self.value)
    
    def __eq__(self, __value: object) -> bool:
        return type(__value) == type(self) and ((self.materia1 == __value.materia1 and self.materia2 == __value.materia2) or (self.materia1 == __value.materia2 and self.materia2 == __value.materia1))
    
    def id(self):
        return (self.profesor.id, self.bloque_horario.id())

