from entities import BloqueHorario, Dia, Materia, Profesor, Grupo
import gurobipy as gp

class u:
    def __init__(self, materia: Materia, horario: BloqueHorario) -> None:
        self.materia = materia
        self.horario = horario
        self.variable: gp.Var  = None

    def __str__(self) -> str:
        return "u_{" + str(self.materia) + "_" + str(self.horario) + "}"
    
    def __eq__(self, __value: object) -> bool:
        return type(__value) == type(self) and self.materia == __value.materia and self.horario == __value.horario
    
class v:
    def __init__(self, materia: Materia, dia: Dia) -> None:
        self.materia = materia
        self.dia = dia
        self.variable = None

    def __str__(self) -> str:
        return "v_{" + str(self.materia) + "_" + str(self.dia) + "}"
    
    def __eq__(self, __value: object) -> bool:
        return type(__value) == type(self) and self.materia == __value.materia and self.dia == __value.dia

class w:
    def __init__(self, materia: Materia, profesor: Profesor) -> None:
        self.materia = materia
        self.profesor = profesor
        self.variable = None
    
    def __str__(self) -> str:
        return "w_{" + str(self.materia) + "_" + str(self.profesor) + "}"
    
    def __eq__(self, __value: object) -> bool:
        return type(__value) == type(self) and self.profesor == __value.profesor and self.materia == __value.materia 

class x:
    def __init__(self, grupo: Grupo, horario: BloqueHorario) -> None:
        self.grupo = grupo
        self.horario = horario
        self.variable = None

    def __str__(self) -> str:
        return "x_{" + str(self.grupo) + "_" + str(self.horario) + "}"
    
    def __eq__(self, __value: object) -> bool:
        return type(__value) == type(self) and self.grupo == __value.grupo and self.horario == __value.horario

class y:
    def __init__(self, profesor: Profesor, horario: BloqueHorario) -> None:
        self.profesor = profesor
        self.horario = horario
        self.variable = None

    def __str__(self) -> str:
        return "y_{" + str(self.profesor) + "_" + str(self.horario) + "}"
    
    def __eq__(self, __value: object) -> bool:
        return type(__value) == type(self) and self.profesor == __value.profesor and self.horario == __value.horario

class z:
    def __init__(self, profesor: Profesor, dia: Dia) -> None:
        self.profesor = profesor
        self.dia = dia
        self.variable = None

    def __str__(self) -> str:
        return "z_{" + str(self.profesor) + "_" + str(self.dia) + "}"
    
    def __eq__(self, __value: object) -> bool:
        return type(__value) == type(self) and self.profesor == __value.profesor and self.dia == __value.dia
