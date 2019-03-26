"""
Contains all the classes required to create and launch this CV web application.

@author: Elias Gabriel
@revision: v1.0
"""
from flask import Flask


class Application(Flask):
    """ A wrapper for a Flask application to simplify app configuration and launching. """


    def __init__(self, app_name=__name__, debug=False):
        super(__name__)
        self.debug = debug


    def listen(self, ip="127.0.0.1", port=8080):
        """ Asks Flask to begin listening to HTTP requests on the given IP and port number. """
        self.run(ip=ip, port=port)


    def route(self, routes):
        """ Registers each URL rule in routes to its specificed endpoint and response function. """
        for url, func in routes.items():
            self.add_url_rule(url, func.__name__, func)
