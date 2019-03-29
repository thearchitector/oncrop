"""
Contains all the classes required to create and launch an application server.

@author: Elias Gabriel, Duncan Mazz
@revision: v1.0
"""
from flask import Flask


class WebApplication(Flask):
		"""
		A wrapper for a Flask application to simplify app configuration and launching.
		"""


		def __init__(self, app_name=None, debug=False):
				super().__init__(app_name or __name__)
				self.debug = debug


		def listen(self, **options):
				""" Asks Flask to begin listening to HTTP requests, with options if given. """
				# If a host is not given, assume localhost
				self.run(options.get('host', "127.0.0.1"), options.get('port', 3000), options)


		def route(self, routes):
				""" Registers each URL rule in routes to its specificed endpoint and response function. """
				for url, func in routes.items():
						self.add_url_rule(url, func.__name__, func)
