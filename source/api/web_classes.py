"""
Contains all the classes required to create and launch an application server.

@author: Elias Gabriel, Duncan Mazz
@revision: v1.0
"""
from flask import Flask
from redis import Redis, ConnectionError
from flask_session import Session
import subprocess
import os



def launch_redis():
	""" Retrieves the running Redis server, or launches one if nothing is running. """
	rs = Redis('localhost')

	try:
		# Pings the Redis server. If there is an error, we know there isn't a server running
		rs.ping()
		return rs
	except ConnectionError:
		# Spawn a new process and launch a new Redis server
		subprocess.Popen(["redis-server"])
		# Run this function again to return the new server
		return launch_redis()



class WebApplication(Flask):
	"""
	A wrapper for a Flask application to simplify app configuration and launching.
	"""

	def __init__(self, app_name=None, debug=False):
		# Call __init__ from the Flask superclass
		super().__init__(app_name or __name__)

		# Set configuration variables
		self.debug = debug
		self.config['SESSION_TYPE'] = 'redis'
		self.config['SESSION_REDIS'] = launch_redis()
		self.config['SECRET_KEY'] = os.urandom(16)
		Session(self)

	def listen(self, **options):
		""" Asks Flask to begin listening to HTTP requests, with options if given. """
		# If a host is not given, assume localhost
		self.run(options.get('host', "127.0.0.1"), options.get('port', 3000), options)


	def route(self, routes):
		""" Registers each URL rule in routes to its specificed endpoint and response function. """
		for url, func in routes.items():
			self.add_url_rule(url, func.__name__, func, methods=['GET', 'POST'])
