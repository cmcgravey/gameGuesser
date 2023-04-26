"""API development configuration."""

import pathlib

SECRET_KEY = b'}\x9eVO\x9c\xa12\xcb\xfc*\x16.\x88(\xb7\xd3d\xb9=iG\xb9\xa7\xe9'
SESSION_COOKIE_NAME = 'login'

# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent

# Path of sqlite database
DATABASE_FILENAME = PROJECT_ROOT/'var'/'scoresapi.sqlite3'