from models.usuario import Usuario
from config import Config

class Tesis:

    tabla = "tesis"

    def __init__(self, id, nombre, jurado_id=0, director_id=0):
        self.id = id
        self.nombre = nombre
        self.jurado = Usuario.getById(jurado_id)
        self.director = Usuario.getById(director_id)

    @staticmethod
    def create(nombre):
        query = " INSERT INTO %s (id, nombre) VALUES (sequence_tesis.nextval, '%s')" % (Tesis.tabla, str(nombre))
        cursor = Config.getCursor()
        try:
            cursor.execute(query)
            cursor.execute("select sequence_tesis.currval from DUAL")
        except Exception, e:
            print e
            print "No es posible guardar objeto"
        id = cursor.fetchone()
        return Tesis(id[0],nombre)

    def setDirector(self, director):
        query = "UPDATE %s SET director_id=%s WHERE id=%s" % (Tesis.tabla, str(director.id), str(self.id))
        cursor = Config.getCursor()
        try:
            cursor.execute(query)
            return True
        except Exception, e:
            print e
            return False

    def setJurado(self, jurado):
        query = "UPDATE %s SET jurado_id=%s WHERE id=%s" % (Tesis.tabla, str(jurado.id), str(self.id))
        cursor = Config.getCursor()
        try:
            cursor.execute(query)
            return True
        except Exception, e:
            print e
            return False
            

    def getJurado(self):
        return None

    def getDirector(self):
        return None

    @staticmethod
    def getById(id):
        query =  "SELECT * FROM %s WHERE id=%s" (Tesis.tabla, id)
        cursor = Config.getCursor()
        try:
            cursor.execute(query)
            row = cursor.fetchone()
        except Exception, e:
            print e
            return None
        return Tesis(row[0], row[3], row[1], row[2])
