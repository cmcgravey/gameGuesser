"""API package initializer."""
import flask

app = flask.Flask(__name__)

app.config.from_object('gameGuesser.config')

import gameGuesser.api
import gameGuesser.model
import gameGuesser.views