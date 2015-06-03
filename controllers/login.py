import web
import hashlib
from models.usuario import Usuario



render = web.template.render('templates/', base="base")


def logged():
    if web.ctx.session.login==1:
        return True
    else:
        return False


def  create_render(privilege):
    if logged():
        if privilege == 0:
            render = web.template.render('templates/reader')
        elif privilege == 1:
            render = web.template.render('templates/user')
        elif privilege == 2:
            render = web.template.render('templates/admin')
        else:
            render = web.template.render('templates/communs')
    else:
        render = web.template.render('templates/communs')
    return render

render = web.template.render('templates/', base="base")

class Login:   


    def GET(self):
        if logged():
            #render = create_render(session.privilege)
            return render.login() # Redireccionar
        else:
            #render = create_render(session.privilege)
            return render.login()

    def POST(self):
        render = web.template.render('templates/', base="base")
        datos_in = web.input()
        name = datos_in['user']
        passwd = datos_in['passwd']
        usuario = Usuario.getAllWith("usuario",name)[0]
        try:
            #if hashlib.sha1("sAlT754-"+passwd).hexdigest() == usuario.contrasena
            if passwd == usuario.contrasena:
                web.ctx.session.login = 1
                web.ctx.session.privilege = usuario.id
                print web.ctx.session.privilege
                web.seeother('/catalogo/')# Cambiar por menu inicial
            else:
                web.ctx.session.login = 0
                web.ctx.session.privilege = 0
                render = create_render(web.ctx.session.privilege)
                return render.login_error()
        except Exception, e:
            print e
            web.ctx.session.login = 0
            web.ctx.session.privilege = 0
            web.ctx.session = create_render(web.ctx.session.privilege)
            return render.seeother()
