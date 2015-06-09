from config import Config
from datetime import date

#Este modelo es de otro proyecto, hay que adaptarlo para las necesidades
class Evaluacion:

    tabla = "evaluaciones"

    def __init__(self, identificador, periodo, fecha_inicial, fecha_final, tiempo_maximo, plantilla_id):
        self.id = identificador
        self.periodo = periodo
        self.fecha_inicial = fecha_inicial
        self.fecha_final = fecha_final
        self.tiempo_maximo = tiempo_maximo
        self.plantilla_id = plantilla_id

    #insertar
    @staticmethod
    def create(periodo, fecha_final, fecha_inicial, tiempo_maximo, plantilla_id):
        query = " INSERT INTO %s (id, periodo, fecha_final, fecha_inicial, tiempo_maximo, plantilla_id) VALUES (sequence_evaluaciones.nextval,'%s',to_date('%s','yyyy/mm/dd'),to_date('%s','yyyy/mm/dd'),'%s','%s')" % (Evaluacion.tabla, periodo, fecha_final, fecha_inicial, tiempo_maximo, plantilla_id)
        cursor = Config.getCursor()
        try:
            cursor.execute(query)
            cursor.execute("select sequence_evaluaciones.currval from DUAL")
        except Exception, e:
            print e
            print "No es posible guardar objeto"
        id = cursor.fetchone()
        return Evaluacion(id[0],periodo, fecha_inicial, fecha_final, tiempo_maximo, plantilla_id)
    
    #consultar
    @staticmethod
    def getById(id):
        cursor = Config.getCursor()
        query = "SELECT * FROM %s WHERE id=%s" % (Evaluacion.tabla, id)
        try:
            cursor.execute(query)
            row = cursor.fetchone()  
        except Exception, e:
            print e
            print "No es posible ejecutar query  o no hay resultados validos"
            return None
        if row == None: #si no se encuentra ningun registro
            return None         
        return Evaluacion(row[0], row[1], row[3], row[2], row[4], row[5])


    @staticmethod
    def getPlantilla(self):
        query = "SELECT pr.id, pr.pregunta FROM %s tr, %s pr WHERE tr.plantilla_id=%s" % (Plantilla.tabla_preguntas_plantillas, Pregunta.tabla, self.id)
        cursor = Config.getCursor()
        preguntas = []
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                preguntas.append(Pregunta(row[0], row[1]))
            return preguntas
        except Exception, e:
            print query
            print e
            return []
    '''@staticmethod
    def isValidUser(username, contrasena):
        query =  "SELECT id FROM %s WHERE username='%s' AND contrasena='%s'" % (Usuario.tabla, username, contrasena)
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
            return id[0]'''


