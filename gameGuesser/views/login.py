"""
GameGuesser index route.
URLs include:
/accounts/login GET
/accounts/login POST
"""
import flask
import gameGuesser
import hashlib

@gameGuesser.app.route('/accounts/login', methods=['GET'])
def show_login():
    if 'username' not in flask.session:
        return flask.render_template('login.html')
    return flask.redirect(flask.url_for('show_index'))


@gameGuesser.app.route('/accounts/', methods=['POST'])
def account_form():
    connection = gameGuesser.model.get_db()
    if flask.request.form['operation'] == 'login':
        login_user(connection)


def login_user(connection):
    if 'password' not in flask.request.form or 'username' not in flask.request.form:
        flask.abort(400, "Username or password fields empty")
    
    password = flask.request.form['password']
    logname = flask.request.form['username']

    cur = connection.execute(
        "SELECT username, password "
        "FROM users "
        "WHERE username = ?",
        (logname, )
    )
    correct = cur.fetchall()
    if correct == []:
        flask.abort(403, "Username doesn't exist in database")
    elif verify_password(correct[0]['password'], password) is False:
        flask.abort(403, 'Incorrect password')
    else:
        flask.session['username'] = logname


def verify_password(password, userinput):
    """Verify user's password."""
    password = password.split('$')
    algorithm = password[0]
    salt = password[1]
    hash_obj = hashlib.new(algorithm)
    input_w_salt = salt + userinput
    hash_obj.update(input_w_salt.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    if password_hash == password[2]:
        print('True')
        return True
    return False