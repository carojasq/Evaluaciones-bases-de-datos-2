from models.usuario import Usuario
from models.evaluacion import Evaluacion
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
        evaluado = datos_in['evaluado']
        evaluador = datos_in['evaluador']
        evaluacion = Evaluacion.create(periodo, fecha_final, fecha_inicial, tiempo_maximo, plantilla)
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
        raise web.redirect('/plantilla/listar/')

class ListarEvaluacion:
    def GET(self):
        evaluaciones = Evaluacion.getAll()
        return render.listar_evaluacion(evaluaciones)

