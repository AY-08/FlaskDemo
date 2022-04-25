from ctypes.wintypes import DOUBLE
from pydoc import cli
import sqlite3
from unicodedata import category
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


app =Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir+'seeding.db')
db = SQLAlchemy(app)

@app.cli.command('db_create')
def db_create():
    db.create_all()
    print("Database Created")

@app.cli.command('db_seed')
def db_seed():
    role=Role(role_id=1,role_name='CONSUMER')
    user=User(user_id=1,user_name='jack',password='pass_word',role=role)
    user2=User(user_id=2,user_name='bob',password='pass_word',role=role)
    db.session.add(role)
    db.session.add(user)
    db.session.add(user2)
    db.session.commit()
    
    print("Database seeded")



class Role(db.Model):
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String)
    user = db.relationship('User',backref = 'role',uselist = False)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String)
    password = db.Column(db.String)
    user_role= db.Column(db.Integer, db.ForeignKey('role.role_id'))
    product= db.relationship('Product',backref = 'user')
    cart= db.relationship('Cart',backref = 'user')

class Category(db.Model):
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String)
    product= db.relationship('Product',backref = 'category')


class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Numeric)
    product_name = db.Column(db.String)
    category_id= db.Column(db.Integer, db.ForeignKey('category.category_id'))
    seller_id = db.Column(db.Integer,db.ForeignKey('user.user_id'))
    cartproduct= db.relationship('CartProduct',backref = 'product')

class Cart(db.Model):
    cart_id = db.Column(db.Integer, primary_key=True)
    totalamount = db.Column(db.Numeric)
    user_id=db.Column(db.Integer,db.ForeignKey('user.user_id'))
    cartproduct = db.relationship('CartProduct',backref = 'cart')


class CartProduct(db.Model):
    cp_id = db.Column(db.Integer, primary_key=True)
    cart_id= db.Column(db.String, db.ForeignKey('cart.cart_id'))
    product_id = db.Column(db.Integer,db.ForeignKey('product.product_id'))
    quantity=db.Column(db.Integer)


    