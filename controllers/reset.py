import web

render = web.template.render('templates/', base="base")


class Reset:
	def GET(self):
		web.ctx.session.login = 0
		web.ctx.session.privilege = 0
		web.ctx.session.kill()
		return render.index(None)