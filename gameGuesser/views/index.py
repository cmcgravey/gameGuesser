"""
GameGuesser index route.
URLs include:
/ GET
"""
import flask
import gameGuesser
from datetime import date

@gameGuesser.app.route('/', methods=['GET'])
def show_index():
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_login'))
    
    connection = gameGuesser.model.get_db()
    context = {}
    game_list = []
    
    day = date.today()
    day = day.strftime("%d/%m/%Y")

    cur = connection.execute(
        "SELECT home, away "
        "FROM games G "
        "WHERE G.date = ?",
        (day, ) 
    )
    games = cur.fetchall()

    for game in games:
        game_list.append({"home": game['home'], "away": game['away']})
    
    context['games'] = game_list
    context['logname'] = flask.session['username']


    return flask.render_template('index.html', **context)
