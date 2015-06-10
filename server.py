import web
web.config.debug = False
from controllers.plantilla_controller import *
from controllers.usuario_controller import *
from controllers.index_controller import *
from controllers.evaluacion_controller import *
from controllers.login import *
from controllers.reset import *


# Aca se definen las URLs (url, nombre controlador)
urls = (
    '/', 'IndexController',
    '/index', 'IndexController',
    '/login','Login',
    '/reset','Reset',
    '/plantilla/crear/.*', 'CrearPlantilla',
    '/plantilla/listar/.*', 'ListarPlantilla',
    '/plantilla/ver/.*', 'VerPlantilla',
    '/evaluacion/crear/.*', 'CrearEvaluacion',
    '/evaluacion/listar/.*', 'ListarEvaluacion',
    '/evaluar/.*', 'ListarEvaluacionesUsuario', 
)

render = web.template.render('templates/', base="base")


app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'login': 0, 'privilege': 0})

def session_hook():
    web.ctx.session = session
    web.template.Template.globals['session'] = session

app.add_processor(web.loadhook(session_hook))
app.run()





