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
        self.fecha_inicial = fecha_inicial
        self.fecha_final = fecha_final
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
        if evaluado=="Docente" and evaluador=="Estudiante":
            cursor.callproc("prep_examenes_est_prof", [self.id])
            return True;
        elif evaluado =="Estudiante"  and evaluador=="Estudiante":
            cursor.callproc("prep_examenes_est_est", [self.id])
            return True
        elif evaluado =="Funcionario"  and evaluador=="Estudiante":
            cursor.callproc("prep_examenes_est_funcionario", [self.id])
            return True
        elif evaluado =="Estructura"  and evaluador=="Estudiante":
            cursor.callproc("prep_examenes_est_estruc", [self.id])
            return True
        elif evaluado =="Tesis"  and evaluador=="Estudiante":
            cursor.callproc("prep_examenes_est_direc", [self.id])
            return True
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
            if evaluacion.fecha_final.date() >= fecha_actual:
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

class Resultado:

    tabla = "resultados_evaluaciones"
    tabla_preguntas =  "resultados_preguntas"


    def __init__(self, id, evaluador_id, evaluado_id, fecha, promedio, estado="Completo", preguntas=[]):
        self.id = id
        self.evaluado = Usuario.getById(evaluado_id)
        self.evaluador = Usuario.getById(evaluador_id)
        self.fecha = fecha
        self.promedio = promedio
        self.estado = estado
        self.resultados = preguntas
    
    @staticmethod
    def create(evaluacion_id, evaluado_id, evaluador_id, preguntas, estado="Completo", fecha=date.today()):
        # Preguntas, arreglo parejas ordenadas (id_pregunta, calificacion)
        calificaciones = [float(p[0]) for p in preguntas]
        promedio =  sum(calificaciones) / len(calificaciones)
        query = "INSERT INTO %s (id, evaluador_id, evaluado_id, fecha, promedio, evaluacion_id, estado) values (sequence_resultados.nextval, %s, %s, to_date('%s', 'yyyy/mm/dd'), %s, %s, '%s')" % (Resultado.tabla, evaluador_id, evaluado_id, fecha.strftime('%Y/%m/%d'), str(promedio), str(evaluacion_id), str(estado))
        try:
            cursor  = Config.getCursor()
            cursor.execute(query)
        except Exception, e:
            return None
        try:
            cursor.execute("SELECT sequence_resultados.currval FROM DUAL")
            row  = cursor.fetchone()
        except Exception, e:
            return None
        id_resultado = row[0]
        for p in preguntas:
            query = "INSERT INTO %s (pregunta_id, resultado_id,  nota) values (%s, %s, %s)"   % (Resultado.tabla_preguntas, str(p[1]), str(id_resultado), str(p[0]))
            try:
                cursor.execute(query)
            except Exception, e:
                return None

        return Resultado(row[0], evaluador_id, evaluado_id, fecha, promedio, estado, preguntas)



#insert into evaluacion_usuario(EVALUADO_ID, EVALUACION_ID, EVALUADOR_ID) values(8, 1, 6)
#insert into evaluacion_usuario(EVALUADO_ID, EVALUACION_ID, EVALUADOR_ID) values(8, 1, 7)
#INSERT INTO resultados_evaluaciones (ID, EVALUADOR_ID, EVALUADO_ID, FECHA, PROMEDIO, EVALUACION_ID, ESTADO) VALUES (1, 6, 8, to_date('2015/05/06', 'yyyy/mm/dd'), 5.1, 1, 'completo');
