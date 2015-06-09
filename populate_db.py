from models.asignatura import Asignatura
from models.cargo import Cargo
from models.plantilla import Plantilla
from models.usuario import Usuario, Administrador, Estudiante, Estructura, Funcionario
from models.tesis import Tesis
from models.grupo import Grupo
from models.evaluacion import Evaluacion

#Creo 2 asignaturas
a1 = Asignatura.create("Bases de datos 2")
a2 = Asignatura.create("Bases de datos 1")

# Creo algunos cargos
docente_c =  Cargo.create("Docente")
decano_ing_c = Cargo.create("Decano Ingenieria")
rector_c = Cargo.create("Rector") 
coordinador_ing_sistemas = Cargo.create("Coordinador ingenieria de sistemas")

#Creo una plantilla y anado una pregunta
pl = Plantilla.create("Plantilla de prueba")
pl.addPregunta("El profesor sabe?")
pl.addPregunta("El profesor va a clase?")
pl.addPregunta("El profesor es claro?")

#Creo usuario administrador
u1 = Usuario.create("Cristian Rojas", "carojasq", "contrasena", "carojasq@u.co")
admin1 = Administrador.create(u1)

#Creo una estructura (rectoria)
u1 = Usuario.create("Rectoria",  "rectoria", "contrasena", "recotoria@u.co")
es1 = Estructura.create(u1, rector_c)

#Creo una estructura derivada de rectoria
u2 = Usuario.create("Decanatura de ingenieria",  "decanaturaing", "contrasena", "decanaturaing@u.co")
es2 = Estructura.create(u2, decano_ing_c, es1)

#Creo proyecto curricular, derivado de decanatura
u3 = Usuario.create("Ingenieria de sistemas",  "ingsistemas", "contrasena", "ingsistemas@u.co")
es3 = Estructura.create(u3, coordinador_ing_sistemas, es2)


#Creo un estudiante
u10 =  Usuario.create("Fabian Puentes", "fpuentes", "contrasena", "fpuentes@u.co")
e10 = Estudiante.create(u10, "3454554", es3)

#Otro estuduante
u15 =  Usuario.create("Viviana Sotelo", "vsotelo", "contrasena", "vsotelo@u.co")
e15 = Estudiante.create(u15, "98765432", es3)
#Otro
u16 =  Usuario.create("Andres Cobos", "acobos", "contrasena", "acobos@u.co")
e16 = Estudiante.create(u16, "54532453", es3)

#Creo un funcionario y le doy cargo
u11 = Usuario.create("Sonia Ordonez", "soniaordo", "contrasena", "soniaordo@u.co")
f11 = Funcionario.create(u11, "8789798")
f11.setCargo(docente_c)

#Creo una tesis
t1 = Tesis.create("Este es el titulo")

#Doy tesis a estudiante
e10.setTesis(t1)

#Ejemplo para obtener el tipo de un usuario
tipo = u11.getTipo(u11.id)

# Creo dos grupos de bases de datos 1 y 2
g1 =  Grupo.create(a1, f11, 20151, es3)
g2 =  Grupo.create(a2, f11, 20151, es3)
g1.addEstudiante(e10)
g2.addEstudiante(e10)
g1.addEstudiante(e15)


#Creo una evaluacion
eva1 = Evaluacion.create("20151", "2015/08/05", "2015/01/01", 100, pl )
eva1.asignarEvaluaciones("Estudiante", "Docente")