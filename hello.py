import cherrypy

class HelloWorld(object):
    def index(self):
	return "Week5 Assignment" 
    index.exposed = True


cherrypy.config.update({'server.socket_host':'0.0.0.0',#listen on all IPS
			'server.socket_port':8088,#change port
			})
cherrypy.quickstart(HelloWorld())
