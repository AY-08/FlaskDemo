from collections import UserList
from enum import unique
from flask import Flask, jsonify,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///fresco.db'
app.config['SECRET_KEY']='thisissecretkey'

db = SQLAlchemy(app)

class user(db.Model):
    user_id = db.Column(db.Integer, primary_key=True , unique= True)
    user_name = db.Column(db.String)
    #role_id = db.relationship(Role, backref='user',UserList=False)