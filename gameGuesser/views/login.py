"""
GameGuesser index route.
URLs include:
/accounts/login GET
/accounts/login POST
"""
import flask
import gameGuesser
import hashlib
import uuid

@gameGuesser.app.route('/accounts/login/', methods=['GET'])
def show_login():
    if 'username' not in flask.session:
        return flask.render_template('login.html')
    return flask.redirect(flask.url_for('show_index'))

@gameGuesser.app.route('/accounts/create/', methods=['GET'])
def show_create():
    if 'username' not in flask.session:
        return flask.render_template('create.html')
    return flask.redirect(flask.url_for('show_edit'))


@gameGuesser.app.route('/accounts/', methods=['POST'])
def account_form():
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_login'))
    
    connection = gameGuesser.model.get_db()

    if flask.request.form['operation'] == 'login':
        login_user(connection)
    elif flask.request.form['operation'] == 'create':
        create_user(connection)

    
    if 'target' not in flask.request.args:
        return flask.redirect(flask.url_for('show_index'))
    return flask.redirect(flask.request.args['target'])


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

def hash_password(password):
    """Hash user's password."""
    algorithm = 'sha512'
    salt = uuid.uuid4().hex
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])
    return password_db_string

def create_user(connection):
    logname = flask.request.form['username']
    password = flask.request.form['password']
    fullname = flask.request.form['fullname']
    fav_team = flask.request.form['favorite-team']

    if logname == '' or password == '' or fullname == '' or fav_team == '':
        flask.abort(400, "Missing one or more fields")

    cur = connection.execute(
        "SELECT username "
        "FROM users "
        "WHERE username = ?",
        (logname, )
    )
    check = cur.fetchall()
    if check != []:
        flask.abort(400, "username is already in use")

    password = hash_password(password)

    connection.execute(
        "INSERT "
        "INTO users(username, fullname, password, favorite) "
        "VALUES (?, ?, ?, ?, ?)",
        (logname, fullname, password, fav_team, )
    )
    flask.session['username'] = logname

