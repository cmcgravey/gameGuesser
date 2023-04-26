"""
Scoresapi update route.
URLs include:
/v1/api/update/ POST
"""
import flask
import gameGuesser

@gameGuesser.app.route('/v1/api/update/', methods=['POST'])
def update_db():

    connection = gameGuesser.model.get_db()

    type = flask.request.args['type']
    if type == 'winners':
        print(flask.request.json)
        return flask.jsonify({"message": "winners"})
    elif type == 'matchups':

        msg = flask.request.json

        for matchup in msg["matchups"]:
            connection.execute(
                "INSERT INTO games(home, away, date) "
                "VALUES (?, ?, ?)", 
                (matchup[1], matchup[0], msg['date'], )
            )
        
        return flask.jsonify({"message": "matchups"}), 201