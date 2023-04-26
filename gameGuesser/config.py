"""API development configuration."""

import pathlib

# Root of this application, useful if it doesn't occupy an entire domain
API_ROOT = '/'
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent

# Path of sqlite database
DATABASE_FILENAME = PROJECT_ROOT/'var'/'scoresapi.sqlite3'