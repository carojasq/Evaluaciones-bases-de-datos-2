from config import Config
from datetime import date, datetime
from models.plantilla import Plantilla
from models.usuario import *
#Este modelo es de otro proyecto, hay que adaptarlo para las necesidades
class Evaluacion:

    tabla = "evaluaciones"
    tabla_usuarios = "evaluacion_usuario"
    tabla_resultados = "resultados_evaluaciones"

    def __init__(self, identificador, periodo, fecha_inicial, fecha_final, tiempo_maximo, plantilla_id):
        self.id = identificador
        self.periodo = periodo
        self.fecha_inicial = fecha_inicial.date()
        self.fecha_final = fecha_final.date()
        self.tiempo_maximo = tiempo_maximo
        self.plantilla_id = plantilla_id
        self.plantilla = Plantilla.getById(plantilla_id)

    #insertar
    @staticmethod
    def create(periodo, fecha_final, fecha_inicial, tiempo_maximo, plantilla):
        query = " INSERT INTO %s (id, periodo, fecha_final, fecha_inicial, tiempo_maximo, plantilla_id) VALUES (sequence_evaluaciones.nextval,'%s',to_date('%s','yyyy/mm/dd'),to_date('%s','yyyy/mm/dd'),'%s','%s')" % (Evaluacion.tabla, periodo, fecha_final, fecha_inicial, tiempo_maximo, plantilla.id)
        cursor = Config.getCursor()
        try:
            cursor.execute(query)
            cursor.execute("select sequence_evaluaciones.currval from DUAL")
        except Exception, e:
            print e
            print "No es posible guardar objeto"
        id = cursor.fetchone()
        return Evaluacion(id[0],periodo, fecha_inicial, fecha_final, tiempo_maximo, plantilla.id)

    def asignarEvaluaciones(self, evaluador, evaluado):
        cursor = Config.getCursor()
        query = "execute prep_examenes_est_prof(%s)" % self.id
        if evaluado=="Docente" and evaluador=="Estudiante":
            print query
            cursor.callproc(prep_examenes_est_prof)
            return True;
        return False

    
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
    def getAvailableForUser(usuario):
        fecha_actual = date.today()
        #Validad que no haya sido contestada y que el usuario pueda contestarla 
        query =  "SELECT evaluacion_id, evaluado_id, evaluador_id FROM %s WHERE evaluador_id=%s MINUS SELECT evaluacion_id, evaluado_id, evaluador_id FROM %s" % (Evaluacion.tabla_usuarios, usuario.id, Evaluacion.tabla_resultados)
        cursor = Config.getCursor()
        available = []
        import ipdb; ipdb.set_trace()
        try:
            cursor.execute(query)
            rows =  cursor.fetchall()
        except Exception, e:
            print e
            return []
        for row in rows:
            evaluacion = Evaluacion.getById(row[0])
            evaluado = Usuario.getById(row[1])
            #Validar la fecha
            if evaluacion.fecha_final >= fecha_actual:
                available.append({'evaluacion': evaluacion, 'evaluado': evaluado})
        return available

    @staticmethod
    def getAll():
        query = "SELECT * FROM %s" % Evaluacion.tabla
        cursor = Config.getCursor()
        evaluaciones = []
        try:
            cursor.execute(query)
            rows =  cursor.fetchall()
        except:
            return evaluaciones
        for row in rows:
            evaluaciones.append(Evaluacion(row[0], row[1], row[3], row[2], row[4], row[5]))
        return evaluaciones



#insert into evaluacion_usuario(EVALUADO_ID, EVALUACION_ID, EVALUADOR_ID) values(8, 1, 6)
#insert into evaluacion_usuario(EVALUADO_ID, EVALUACION_ID, EVALUADOR_ID) values(8, 1, 7)
#INSERT INTO resultados_evaluaciones (ID, EVALUADOR_ID, EVALUADO_ID, FECHA, PROMEDIO, EVALUACION_ID, ESTADO) VALUES (1, 6, 8, to_date('2015/05/06', 'yyyy/mm/dd'), 5.1, 1, 'completo');
