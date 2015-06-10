import web
import hashlib
from models.usuario import Usuario



render = web.template.render('templates/', base="base")


class IndexController:

    def GET(self):
        print web.ctx.session.login 
        print web.ctx.session.privilege 
        render = web.template.render('templates/', base="base")
        print "In get"
        try:
        	usuario =  Usuario.getById(web.ctx.session.privilege[1])
        except:
        	usuario = None
        return render.index(usuario)
