import bookdb, cherrypy, html
from cgi import escape

start_html = '''
<html><body>
         Hello
         Welcome to your very own !!
</body></html>
'''

#def index(environ,start_response):
#	start response ('200 OK', [('Content-Type', 'text/html')])
#return ['''Hello World Application
#This is the Hello World application:
#
#`continue <hello/>`_
#''']



def test_list_books():
    books = bookdb.BookDB()
    titles = books.titles()
    assert len(titles) > 1
    print titles
    for title in titles:
        assert 'title' in title
        assert 'id' in title
    return start_html

def test_get_book_info():
    books = bookdb.BookDB()
    titles = books.titles()
    id = titles[0]['id']
    print id
    info = books.title_info(id)
    print info
    assert 'title' in info
    assert info['title'] == titles[0]['title']
    assert 'publisher' in info
    assert 'isbn' in info
    assert 'author' in info

cherrypy.config.update({'server.socket_host':'0.0.0.0',#listen on all IPS
                        'server.socket_port':8080,#change port
                        })
cherrypy.quickstart((test_list_books))

