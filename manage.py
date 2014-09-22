#!/usr/bin/env python 

# https://realpython.com/blog/python/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/

import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from app import app, db
app.config.from_object( 'config' )

migrate = Migrate(app,db)
manager =  Manager(app)

manager.add_command( 'db', MigrateCommand)

if __name__ == '__main__':
  manager.run()

# python manage.py db  --help
# python manage.py db init
# python manage.py db migrate
# python manage.py db upgrade

# https://github.com/miguelgrinberg/Flask-Migrate
# Alembic is currently unable to detect indexes
# Statements may therefore need to be manually edited in the version file
