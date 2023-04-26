"""
GameGuesser index route.
URLs include:
/ GET
"""
import flask
import gameGuesser

@gameGuesser.app.route('/', methods=['GET'])
def show_index():
    context = {}
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_login'))
    
    return flask.jsonify(context)
