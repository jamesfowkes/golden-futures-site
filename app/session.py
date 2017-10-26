import logging

from flask import Flask, session
from flask_session import Session

_session = Session()

def init_app(app):
	app.config['SESSION_TYPE'] = "filesystem"
	_session.init_app(app)

def get(key):
	return session.get(key, None)

def set(key, value):
	session[key] = value
	