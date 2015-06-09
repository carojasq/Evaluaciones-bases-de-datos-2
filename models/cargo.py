from config import Config


class Cargo:

    tabla = "cargos"

    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre


    @staticmethod
    def create(nombre):
        query = " INSERT INTO %s (id, nombre)  VALUES (sequence_cargos.nextval, '%s')" % (Cargo.tabla, nombre)
        cursor = Config.getCursor()
        try:
            cursor.execute(query)
            cursor.execute("select sequence_cargos.currval from DUAL")
        except Exception, e:
            print e
            print query
            print "No es posible guardar objeto"
            return None
        id = cursor.fetchone()[0]
        return Cargo(id, nombre)


    @staticmethod
    def getById(id):
        cursor = Config.getCursor()
        query = "SELECT * FROM %s WHERE id=%s" % (Cargo.tabla, id)
        try:
            cursor.execute(query)
            row = cursor.fetchone()  
        except:
            print "No es posible ejecutar query  o no hay resultados validos"
            return None
        return Cargo(row[0], row[1])


    @staticmethod
    def getAll():
        cursor = Config.getCursor()
        query = "SELECT * FROM %s " % Cargo.tabla
        try:
            cursor.execute(query)
        except:
            print "No es posible ejecutar query  o no hay resultados validos"
            return []
        cargos  = []
        rows = cursor.fetchall()
        for row in rows:
            cargos.append(Cargo(row[0], row[1]))
        return cargos

    @staticmethod
    def getByName(nombre):
        cursor = Config.getCursor()
        query = "SELECT * FROM %s WHERE nombre='%s'" % (Cargo.tabla, nombre.strip())
        try:
            cursor.execute(query)
            row = cursor.fetchone()  
        except:
            print "No es posible ejecutar query  o no hay resultados validos"
            return None
        return Cargo(row[0], row[1])