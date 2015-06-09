__author__ = 'null3d'
from models.plantilla import Plantilla
import web
render = web.template.render('templates/', base="base")

class ListarPlantilla:
    def GET(self):
        #import ipdb; ipdb.set_trace()
        plantillas = Plantilla.getAll()        
        return render.listar_plantillas(plantillas)


class CrearPlantilla:

    def GET(self):
        datos = web.input()
        plantillas = Plantilla.getAll()
        print plantillas
        if 'plantilla_base' in datos.keys():
            preguntas = Plantilla.getById(datos['plantilla_base']).preguntas
            return render.crear_plantilla(preguntas, plantillas)
        else:
            datos = None
            return render.crear_plantilla(datos, plantillas)

    def POST(self):
        #import ipdb; ipdb.set_trace()
        datos_in = web.input(preguntas = [])
        nombre = datos_in['nombre']
        p = Plantilla.create(nombre)
        for pregunta in datos_in['preguntas']:
            pre =  pregunta.strip()
            if pre != "":
                p.addPregunta(pre)
        raise web.redirect('/plantilla/listar/')


class VerPlantilla:

    def GET(self):
        datos = web.input()
        id_plantilla = datos['id']
        plantilla = Plantilla.getById(id_plantilla)        
        return render.ver_plantilla(plantilla)

