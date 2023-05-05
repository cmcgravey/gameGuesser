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
        msg = flask.request.json
        for winner in msg['winners']:
            print(winner)
            cur = connection.execute(
                "UPDATE guesses "
                "SET outcome = TRUE "
                "WHERE date = ? AND team = ? "
                "RETURNING * ",
                (msg['date'], winner, ) 
            )
            updated = cur.fetchall()
            print(f"updated {str(len(updated))} rows")

        return flask.jsonify({"message": "winners"})
    elif type == 'matchups':

        msg = flask.request.json
        for matchup in msg["matchups"]:
            connection.execute(
                "INSERT OR IGNORE INTO games(home, away, time, date) "
                "VALUES (?, ?, ?, ?)", 
                (matchup['home'], matchup['away'], matchup['time'], msg['date'], )
            )
        
        return flask.jsonify({"message": "matchups"})