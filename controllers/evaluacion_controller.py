from models.usuario import Usuario
from models.evaluacion import *
from models.plantilla import Plantilla
#from models.administrador import Administrador
import web


render = web.template.render('templates/', base="base")



class CrearEvaluacion:

    def GET(self):
        datos = web.input()
        plantillas_disponibles = Plantilla.getAll()
        #datos['ciudades'] = Ciudad.getAll()
        return render.crear_evaluacion(plantillas_disponibles) 

    def POST(self):
        datos_in = web.input()
        periodo = datos_in['periodo']
        fecha_final = datos_in['fecha_final']
        fecha_inicial = datos_in['fecha_inicial']
        tiempo_maximo = datos_in ['tiempo_maximo']
        plantilla_id= datos_in['plantilla_id']
        plantilla =  Plantilla.getById(plantilla_id)
        evaluado = datos_in['evaluado'].strip()
        evaluador = datos_in['evaluador'].strip()
        evaluacion = Evaluacion.create(periodo, fecha_final, fecha_inicial, tiempo_maximo, plantilla)
        evaluacion.asignarEvaluaciones(evaluador, evaluado)
        # Aca va el procedure 

        raise web.redirect('/evaluacion/listar/')


class VerEvaluacion:

    def GET(self):
        datos = web.input()
        #import ipdb; ipdb.set_trace()
        id_evaluacion = datos['id']
        evaluacion = Evaluacion.getById(id_evaluacion)

        plantillaid = datos['plantilla']
        preguntas = Plantilla.getPreguntas(plantillaid)
        return render.ver_evaluacion(evaluacion,preguntas)
    #Collect id plantilla
    def POST(self):
        datos_in = web.input()
        nombre = datos_in['id']
        # Guardar todas las preguntas
        #departamento = datos_in['departamento']
        #pais = datos_in['pais']
        #c = Ciudad.create(ciudad, departamento, pais)
        raise web.redirect('/evaluar/')

class ListarEvaluacion:
    def GET(self):
        evaluaciones = Evaluacion.getAll()
        return render.listar_evaluacion(evaluaciones)

class ListarEvaluacionesUsuario:
    def GET(self):
        datos = web.input()
        try:
            id_evaluacion = datos['id']
            id_evaluado = datos['evaluado_id']
            #import ipdb; ipdb.set_trace()
            evaluacion = Evaluacion.getById(id_evaluacion)
            evaluado = Usuario.getById(id_evaluado)
            return render.evaluar_concreto(evaluacion, evaluado)
        except:
            evaluaciones = Evaluacion.getAvailableForUser(Usuario.getById(web.ctx.session.privilege[1]))
            return render.evaluar(evaluaciones)

    def POST(self):
        datos = web.input()
        id_evaluacion = datos['evaluacion_id']
        id_evaluado = datos['evaluado_id']
        ev =  Evaluacion.getById(id_evaluacion)
        prs = ev.plantilla.preguntas
        i = 1
        res  = []
        for p in prs:
            res.append((datos["resultados%s" % str(p.id)], p.id))
        id_evaluador =  web.ctx.session.privilege[1]
        resultado  = Resultado.create(id_evaluacion, id_evaluado, id_evaluador, res )
        evaluaciones = Evaluacion.getAvailableForUser(Usuario.getById(web.ctx.session.privilege[1]))
        return render.evaluar(evaluaciones)



