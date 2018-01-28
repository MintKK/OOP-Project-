from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import func

sqldb = SQLAlchemy()

class Organisations(sqldb.Model):
    id = sqldb.Column(sqldb.Integer, primary_key=True)
    name = sqldb.Column(sqldb.String())
    email = sqldb.Column(sqldb.String())
    address = sqldb.Column(sqldb.String())
    phone = sqldb.Column(sqldb.String())
