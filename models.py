import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.sqlite'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/book'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@dataclass
class Contacts(db.Model):
    id: int
    name: str
    surname: str
    email: str
    phone: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(200), nullable=True, unique=True)
    phone = db.Column(db.String(20), nullable=True, unique=False)

    def __init__(self, name, surname, email, phone):
        self.name = name
        self.surname = surname
        self.email = email
        self.phone = phone

    def __repr__(self):
        return '<Contacts %r>' % self.name