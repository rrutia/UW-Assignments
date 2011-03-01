# Import the cherrypy and mako modules. If everything
# went ok in the install these should be
# available on your system

import cherrypy
from mako.template import Template
from mako.lookup import TemplateLookup


# TemplateLookup is a Mako object that specifies where mako
# is to find the html files you want to render. I recommend
# going through the Basic usage of Mako docs to get started:
# http://www.makotemplates.org/docs/usage.html. Mako does not
# need a full physical path and is able to understand a
# relative path from the location of the python file it has
# been imported into. Therefore specifying 'arjunhtml' below
# is enough and 'arjunhtml' is the subdirectory. So the
# python file sits in ..../arjunapyfiles then the 'arjunahtml'
# directory sits in ..../arjunapyfiles/arjunahtml for the
# below to work. You need to change this to suit your own
# directory structure. Or for a quick start, just create a
# subdirectory below where you put this python file and put
# the sub directory name instead of 'arjunahtml'

mylookup = TemplateLookup(directories=['html'])

# The website. Remember, where ever you see the word 'arjuna...'
# you can put your own names.

class SampleApplication:

    # The @cherrypy.expose tells the server that this
    # method can be accessed from a webpage. We need to
    # put this before any method that we want to access
    # from a webpage
    
    @cherrypy.expose
    def index(self):
        # mylookup.get_template is mako functionality that
        # specifies the file you want to render. In this case
        # it pulls the file 'arjunaTest.html' from '/html'
        
        mytemplate = mylookup.get_template("Test.html")
        
        # 'mytemplate.render()' is for rendering the file i.e.
        # doing any substitutions in it, and in this case,
        # creating a straight html file
        
        return mytemplate.render()

    @cherrypy.expose
    def OutputPage(self):
        # The 2 lines below get the page 'arjunaTestOutput.html'
        # and render it in the browser while passing the two
        # variables arjunaName and arjunaWorld
        # to the html file
        
        mytemplate=mylookup.get_template("TestOutput.html")
        return mytemplate.render(Name="Daniel",
                                 World="planet of cherries")

# Everything below this is standard CherryPy-speak for getting things
# configured and started. You can safely put all this at the bottom of
# your python file and have it startup CherryPy correctly. However,
# remember that when you create your own application, you do have to
# change any keywords with the words 'arjuna...'  to point to your
# files or variables. All the non-'arjuna...' words are CherryPy-speak.


# Set up the site
cherrypy.config.update("Global.conf")

# Set up the application
root = SampleApplication()
cherrypy.tree.mount(root, '/', "App.conf")

#start the server
cherrypy.server.quickstart()
cherrypy.engine.start()

