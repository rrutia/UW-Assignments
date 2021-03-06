from setuptools import setup, find_packages

version = '0.7.4'

setup(name='Beaker',
      version=version,
      description="A Session and Caching library with WSGI Middleware",
      long_description="""\
Cache and Session Library
+++++++++++++++++++++++++

About
=====

Beaker 0.7 is a new and refactored update to Beaker built on code from the
package MyghtyUtils, originally used in the Myghty project. It implements a
full set of cache functionality along with sessions that can utilize the 
caches.

Beaker includes Cache and Session WSGI middleware to ease integration with
WSGI capable frameworks, and is automatically used by `Pylons 
<http://pylonshq.com/>`_.

Features
========

* Fast, robust performance
* Multiple reader/single writer lock system to avoid duplicate simultaneous 
  cache creation
* Cache back-ends include dbm, file, memory, memcached, and database (Using
  SQLAlchemy for multiple-db vendor support)
* Signed cookie's to prevent session hijacking/spoofing
* Extensible Container object to support new back-ends
* Cache's can be divided into namespaces (to represent templates, objects, 
  etc.) then keyed for different copies
* Create functions for automatic call-backs to create new cache copies after
  expiration
* Fine-grained toggling of back-ends, keys, and expiration per Cache object

Usage
=====

Caching
-------

Basic Example::
    
    from beaker.cache import CacheManager
    cm = CacheManager(type='dbm', data_dir='./cache')
    
    cache = cm.get_cache('mytemplate')
    
    def somethingslow():
        # slow stuff
        db_lookups()
    
    # Get the value, this will create the cache copy the first time
    # and any time it expires (in seconds, so 3600 = one hour)
    result = mycache.get_value(day, createfunc=somethingslow, expiretime=3600)

Using WSGI::
    
    from beaker.middleware import CacheMiddleware
    
    def simple_app(environ, start_response):
        cache = environ['beaker.cache'].get_cache('testcache')
        try:
            value = cache.get_value('value')
        except KeyError:
            value = 0
        cache.set_value('value', value+1)
        start_response('200 OK', [('Content-type', 'text/plain')])
        return ['The current value is: %s' % cache.get_value('value')]
    
    app = CacheMiddleware(simple_app, type='dbm', data_dir='./cache')

Sessions
--------

Using WSGI::
    
    from beaker.middleware import SessionMiddleware
    
    def simple_app(environ, start_response):
        session = environ['beaker.session']
        if not session.has_key('value'):
            session['value'] = 0
        session['value'] += 1
        session.save()
        start_response('200 OK', [('Content-type', 'text/plain')])
        return ['The current value is: %d' % session['value']]
    
    wsgi_app = SessionMiddleware(simple_app, type='dbm', data_dir='./cache')

Source
======

The latest developer version is available in a `Subversion repository
<http://beaker.groovie.org/svn/trunk#egg=Beaker-dev>`_.
""",
      classifiers=[
      'Development Status :: 5 - Production/Stable',
      'Environment :: Web Environment',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python',
      'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
      ],
      keywords='wsgi myghty session web cache middleware',
      author='Ben Bangart, Mike Bayer, Philip Jenvey',
      author_email='ben@groovie.org, pjenvey@groovie.org',
      url='http://beaker.groovie.org',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      zip_safe=False,
      install_requires=[],
      entry_points="""
          [paste.filter_factory]
          beaker_session = beaker.middleware:session_filter_factory
          [paste.filter_app_factory]
          beaker_session = beaker.middleware:session_filter_app_factory
      """,
)
