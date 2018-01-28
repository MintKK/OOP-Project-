from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.functions import func
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/database.db'

sqldb = SQLAlchemy(app)
migrate = Migrate(app, sqldb)


class Organisations(sqldb.Model):
    id = sqldb.Column(sqldb.Integer, primary_key=True)
    name = sqldb.Column(sqldb.String())
    email = sqldb.Column(sqldb.String())
    address = sqldb.Column(sqldb.String())
    phone = sqldb.Column(sqldb.String())

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
