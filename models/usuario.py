from config import Config
from datetime import date
from models.cargo import Cargo
#Este modelo es de otro proyecto, hay que adaptarlo para las necesidades
class Usuario:

    tabla = "usuarios"

    def __init__(self, identificador, nombre, usuario, contrasena, e_mail, habilitado="Y"):
        self.id = identificador
        self.nombre = nombre
        self.usuario = usuario
        self.contrasena = contrasena
        self.e_mail = e_mail
        self.habilitado = habilitado
        self.tipo = Usuario.getTipo(self.id)

    #insertar
    @staticmethod
    def create(nombre, usuario, contrasena, e_mail="none@none.com", habilitado="Y"):
        query = " INSERT INTO %s (id, email, contrasena, nombre, habilitado, username) VALUES (sequence_usuarios.nextval,'%s','%s','%s','%s','%s')" % (Usuario.tabla, str(e_mail), contrasena, nombre, habilitado, usuario)
        cursor = Config.getCursor()
        try:
            cursor.execute(query)
            cursor.execute("select sequence_usuarios.currval from DUAL")
        except Exception, e:
            print e
            print "No es posible guardar objeto"
        id = cursor.fetchone()
        return Usuario(id[0],nombre, usuario, contrasena, e_mail, habilitado)
    
    #consultar
    @staticmethod
    def getById(id):
        cursor = Config.getCursor()
        query = "SELECT * FROM %s WHERE id=%s" % (Usuario.tabla, id)
        try:
            cursor.execute(query)
            row = cursor.fetchone()  
        except Exception, e:
            print e
            print "No es posible ejecutar query  o no hay resultados validos"
            return None
        if row == None: #si no se encuentra ningun registro
            return None         
        return Usuario(row[0], row[3], row[5], row[2], row[1], row[4])

 
    @staticmethod
    def getTipo(id):
        cursor = Config.getCursor()
        query = "SELECT id FROM administradores WHERE id=%d" %id
        try:
            cursor.execute(query)
        except Exception, e:
            print e
            print "No es posible ejecutar query  o no hay resultados validos"
            return []
        resultado =  "NoTipo"
        row = cursor.fetchone()
        if row != None:
            resultado="Administrador"

        query = "SELECT id FROM funcionarios WHERE id=%d" %id
        try:
            cursor.execute(query)
        except Exception, e:
            print e
            print "No es posible ejecutar query  o no hay resultados validos"
            return []
        row = cursor.fetchone()
        if row != None:
            resultado="Funcionario"

        query = "SELECT id FROM estudiantes WHERE id=%d" %id
        try:
            cursor.execute(query)
        except Exception, e:
            print e
            print "No es posible ejecutar query  o no hay resultados validos"
            return []
        row = cursor.fetchone()
        if row != None:
            resultado="Estudiante"

        query = "SELECT id FROM estructuras WHERE id=%d" %id
        try:
            cursor.execute(query)
        except Exception, e:
            print e
            print "No es posible ejecutar query  o no hay resultados validos"
            return []
        row = cursor.fetchone()
        if row != None:
            resultado="Estructura"

        return resultado

    @staticmethod
    def isValidUser(username, contrasena):
        query =  "SELECT id FROM %s WHERE username='%s' AND contrasena='%s' AND HABILITADO='Y'" % (Usuario.tabla, username, contrasena)
        cursor =  Config.getCursor()
        try:
            cursor.execute(query)
        except Exception, e:
            print e
            print "No es posible guardar objeto"
        id = cursor.fetchone()
        if id is None:
            return None
        else:
            return id[0]


class  Funcionario:
    tabla = "funcionarios"
    tabla_cargos = "cargos_historicos"

    def __init__(self, usuario, codigo):
        self.nombre = usuario.nombre
        self.usuario = usuario
        self.codigo = codigo

        self.cargo = self.getCargo()
        self.id = usuario.id
    
    @staticmethod
    def create(usuario, codigo):
        query = " INSERT INTO %s (id, codigo) VALUES (%s, %s)" % (Funcionario.tabla, str(usuario.id), str(codigo))
        cursor = Config.getCursor()
        try:
            cursor.execute(query)
        except Exception, e:
            print e
            print "No es posible guardar objeto"
        return Funcionario(usuario, codigo)

    def setCargo(self, cargo, fecha_inicio=date.today()):
        # Primero le doy formato a la fecha
        fecha = fecha_inicio.strftime("%d/%m/%Y")
        query = "INSERT INTO %s (fecha_inicio, funcionario_id, cargo_id)  VALUES (to_date('%s', 'dd/mm/yyyy'), %s, %s)" % (Funcionario.tabla_cargos, fecha, self.id, cargo.id)
        try:
            cursor = Config.getCursor()
            cursor.execute(query)
            return True
        except Exception, e:
            print e
            print "No es posible guardar objeto"
            return False

    @staticmethod
    def getAll():
        query = "SELECT * FROM %s" % (Funcionario.tabla)
        cursor = Config.getCursor()
        funcionarios = []
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
        except Exception, e:
            print e
        for row in rows:
            try:
                u = Usuario.getById(row[0])
                funcionarios.append(Funcionario(u, row[0]))
            except:
                print "Error trayendo usuario"

        return funcionarios


    def getCargo(self):
        return None

class Estudiante:
    tabla = "estudiantes"

    def __init__(self, usuario, codigo, estructura):
        self.usuario = usuario
        self.codigo =  codigo
        self.estructura = estructura
        self.nombre = usuario.nombre
        self.id = usuario.id
        self.tesis = self.getTesis()

    @staticmethod
    def create(usuario, codigo, estructura):
        query = " INSERT INTO %s (id, codigo, estructura_id) VALUES (%s, %s, %s)" % (Estudiante.tabla, str(usuario.id), str(codigo), str(estructura.id))
        cursor = Config.getCursor()
        try:
            cursor.execute(query)
        except Exception, e:
            print e
            print "No es posible guardar objeto"
        return Estudiante(usuario, codigo, estructura)

    def setTesis(self, tesis):
        query = "UPDATE %s SET tesis_id=%s WHERE id=%s" % (Estudiante.tabla, str(tesis.id), str(self.usuario.id))
        cursor = Config.getCursor()
        try:
            cursor.execute(query)
            return True
        except Exception, e:
            print e
            print "No es posible guardar objeto"
            return False
    
    def getTesis(self):
        return None

    @staticmethod
    def getById(id):
        query = "SELECT * FROM %s WHERE id=%s" % (Estudiante.tabla, id)
        cursor = Config.getCursor()
        try:
            cursor.execute(query)
            row = cursor.fetchone()
        except Exception, e:
            print e
            return None
        u = Usuario.getById(row[0])
        e = Estructura.getById(row[2])
        est = Estudiante(u, row[1], e)
        return est

    @staticmethod
    def getAll():
        query =  "SELECT * FROM %s" % (Estudiante.tabla)
        cursor = Config.getCursor()
        estudiantes = []
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
        except Exception, e:
            print e
            return []
        for row in rows:
            u = Usuario.getById(row[0])
            e = Estructura.getById(row[2])
            estudiantes.append(Estudiante(u, row[1], e))
        return estudiantes


class Administrador:
    tabla = "administradores"

    def __init__(self, usuario):
        self.usuario = usuario
        self.id = usuario.id

    @staticmethod
    def create(usuario):
        query = " INSERT INTO %s (id) VALUES (%s)" % (Administrador.tabla, str(usuario.id))
        cursor = Config.getCursor()
        try:
            cursor.execute(query)
        except Exception, e:
            print e
            print "No es posible guardar objeto"
        return Administrador(usuario)


class  Estructura:
    tabla = "estructuras"

    def __init__(self, usuario, cargo_director, estructura_padre=None):
        self.usuario = usuario
        self.nombre = usuario.nombre
        self.cargo_director = cargo_director
        self.id =  usuario.id
        self.estructura_padre =  estructura_padre

    @staticmethod
    def create(usuario, cargo_director, estructura_padre=None):
        if estructura_padre:
            query = " INSERT INTO %s (id, director_id, dependencia_id) VALUES (%s, %s, %s)" % (Estructura.tabla, str(usuario.id),  str(cargo_director.id), str(estructura_padre.id))
        else:
            query = " INSERT INTO %s (id, director_id) VALUES (%s, %s)" % (Estructura.tabla, str(usuario.id), str(cargo_director.id))
        try:
            cursor = Config.getCursor()
            cursor.execute(query)
        except Exception, e:
            print e
            print "No es posible guardar objeto"
        return Estructura(usuario, cargo_director, estructura_padre)

    @staticmethod
    def getById(id):
        return None

    def setCargoDirector(self, cargo):
        return True

    @staticmethod
    def getAll():
        query =  "select * from estructuras"
        cursor = Config.getCursor()
        estructuras = []
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
        except:
            print "Error en el cursor"
            return estructuras
        for row in rows:
            u =  Usuario.getById(row[0])
            c =  Cargo.getById(row[2])
            estructuras.append(Estructura(u, c))
        return estructuras




    
