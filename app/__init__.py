from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
#from flask.ext.script import Manager
#from flask.ext.migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config.from_object( 'config' )

db = SQLAlchemy(app)
#migrate = Migrate(app, db)

from app import views, models
from app import viewOrganization
from app import viewIpAddress

#manager = Manager(app)
#manager.add_command('db', MigrateCommand)

# flask has a command line capability


