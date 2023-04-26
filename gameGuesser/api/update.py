"""
Scoresapi update route.
URLs include:
/v1/api/update/ POST
"""
import flask
import gameGuesser

@gameGuesser.app.route('/v1/api/update/', methods=['POST'])
def update_db():
    # connection = scoresapi.model.get_db()

    type = flask.request.args['type']
    if type == 'winners':
        
        return flask.jsonify({"message": "winners"})
    elif type == 'matchups':
        
        return flask.jsonify({"message": "matchups"})