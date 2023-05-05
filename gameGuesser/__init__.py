"""API package initializer."""
import flask

app = flask.Flask(__name__)

app.config.from_object('gameGuesser.config')

app.config.from_envvar('GAMEGUESSER_SETTINGS', silent=True)

import gameGuesser.api
import gameGuesser.model
import gameGuesser.views