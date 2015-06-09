from models.usuario import Usuario, Estructura
from models.cargo import Cargo
from config import Config
import random
import string


def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class Grupo:

    tabla =  "grupos"
    tabla_estudiantes = "estudiantes_grupos"

    def __init__(self, estructura, estructura_padre, asignatura, docente):
        self.id = estructura.id
        self.usuario = estructura
        self.estructura_padre =  estructura_padre
        self.asignatura =  asignatura
        self.docente = docente


    @staticmethod
    def create(asignatura, docente, periodo, estructura_padre):
        nombre_usuario  = "%s  - %s" % (asignatura.nombre, str(periodo))
        username = id_generator()
        u =  Usuario.create(nombre_usuario, username, "DSAFGHGFDSFGFDS", e_mail=username+"@u.co", habilitado="N")
        c = Cargo.getByName("Docente")
        estruc = Estructura.create(u, c, estructura_padre)
        query = "INSERT INTO %s (id, asignatura_id, docente_id, periodo) VALUES (%s, %s, %s, %s) " % ( Grupo.tabla, u.id, asignatura.id, docente.id, periodo)
        cursor = Config.getCursor()
        try:
            cursor.execute(query)
        except Exception, e:
            print e
            import ipdb; ipdb.set_trace()
            print "No es posible ejecutar query  o no hay resultados validos"
            return None
        return Grupo(estruc, estructura_padre, asignatura, docente)


    def addEstudiante(self, estudiante):
        query =  "INSERT INTO %s  (grupo_id, estudiante_id) VALUES (%s, %s)" % (Grupo.tabla_estudiantes, self.id, estudiante.id)
        cursor = Config.getCursor()
        try:
            cursor.execute(query)
            return True
        except Exception, e:
            print e
            return False

    def getEstudiantes(self):
        return None