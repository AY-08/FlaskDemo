import base64
from ctypes.wintypes import DOUBLE
from dataclasses import fields
from ntpath import join
from operator import and_
from pydoc import cli
import sqlite3
from unicodedata import category
from urllib import response
from wsgiref import headers
from click import password_option
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.security import generate_password_hash,check_password_hash
from crypt import methods
from flask import Flask, jsonify,request,make_response
from flask_migrate import Migrate 
from flask_marshmallow import Marshmallow
from functools import wraps
import jwt

app =Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'password'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///seeding.sqlite3'
db = SQLAlchemy(app)
ma = Marshmallow(app)

# migrate = Migrate(app,db)


# @app.cli.command('db_create')
# def db_create():
#     db.create_all()
#     print("Database Created")

# @app.cli.command('db_seed')
# def db_seed():
#     ## Round 1
#     role1=Role(role_id=1,role_name='CONSUMER')  
#     user1=User(user_id=1,user_name='jack',password='pass_word',role=role1)
#     user2=User(user_id=2,user_name='bob',password='pass_word',role=role1)
#     category1 = Category(category_id =1,category_name = 'Fashion')
#     db.session.add(role1)
#     db.session.add(user1)
#     db.session.add(user2)
#     db.session.add(category1)
#     db.session.commit()
#     print("db seeded with first round ")
    
#     # round2
#     role2=Role(role_id=2,role_name='SELLER')
#     user3 = User(user_id=3,user_name='apple',password='pass_word',role=role2)
#     user4= User(user_id=4,user_name='glaxo',password='pass_word',role=role2)
#     category2= Category(category_id =2,category_name = 'Electronics')
#     product = Product(product_id=1,product_name='ipad',price ='29190',user=user3,category=category2)
    
#     category3= Category(category_id =3,category_name = 'Books')
#     category4= Category(category_id =4,category_name = 'Groceries')
#     category5= Category(category_id =5,category_name = 'Medicines')


#     db.session.add(role2)
#     db.session.add(user3)
#     db.session.add(user4)
    
#     db.session.add(category2)
#     db.session.add(category3)
#     db.session.add(category4)
#     db.session.add(category5)
#     db.session.add(product)
#     db.session.commit()

#     print("db seeded with 2nd  round ")


#     ##round3
#     product2 = Product(product_id=2,product_name='crocin',price ='10',user=user4,category=category5)
#     cart1=Cart(cart_id=1,totalamount=20,user=user1)
#     cart2=Cart(cart_id=2,totalamount=0,user=user2)
#     cartproduct1= CartProduct(cp_id=1,cart=cart1,product=product2)
#     db.session.add(product2)
#     db.session.add(cart1)
#     db.session.add(cart2)
#     db.session.add(cartproduct1)
#     db.session.commit()
    
  
    
#     print("db seeded with 3rd  round ")


#     print("Database seeded")



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
    price = db.Column(db.Float)
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

### marshmallow schema 


# class RoleSchema(ma.Schema):
#     role_id = fields.Int(dump_only=True)
#     role_name = fields.Str()
#     class meta:
#         fields = ("role_id","role_name")


# role_schema = RoleSchema()
# roles_schema = RoleSchema(many=True)


class UserSchema(ma.Schema):
    class meta:
        model = User

class CategorySchema(ma.Schema):
    class meta:
        model = Category


class ProductSchema(ma.Schema):
    class meta:
        model = Product


class CartSchema(ma.Schema):
    class meta:
        model = Cart        

class CartProductSchema(ma.Schema):
    class meta:
        model = CartProduct

# product_nqae = 'crocin'

# result = db.session.query(Product,Category).join(Product).filter(Product.product_name==product_nqae).all()
# for pro, cat in result:
#     print(pro.product_name)
#     print(cat.category_name)



# @app.route('/')
# def products():

#     users = Product.query.all()
#     output = []
#     for user in users:
#         output.append({
#             'product_id':user.product_id
#         })
	
    
#     return jsonify({'users': output})


# @app.route('/productjoins')
# def products_join():


#### product join 

@app.route('/api/public/product/search/<string:productname>', methods= ['GET'])
def search_product(productname):
    # productname = '"{}"'.format('crocin')
    print("productname",productname)
    result  = db.session.query(Product,Category,User).\
        select_from(Product).join(Category).join(User).filter(Product.product_name==productname).all()

    if not result:
        return make_response('Product not found',400)
    else:
        output = []
    for prod,cat,usr in result:
        output.append({
        'category':{
            'category_id':cat.category_id,
            'category_name':cat.category_name
        },
        'price':prod.price,
        'product_id':prod.product_id,
        'product_name':prod.product_name,
        'seller_id':usr.user_id
        

    })
    print(prod.product_id)
    print(cat.category_name)
    print(usr.user_name)

    
    return make_response(jsonify(output), 200)

 #### authenticate and response with status code and  JWT

 ##decorator for verifying the JWT
def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		token = None
		# jwt is passed in the request header
		if 'x-access-token' in request.headers:
			token = request.headers['x-access-token']
		# return 401 if token is not passed
		if not token:
			return jsonify({'message' : 'Token is missing !!'}), 401

		try:
			# decoding the payload to fetch the stored details
			data = jwt.decode(token, app.config['SECRET_KEY'])
			current_user = User.query.filter_by(user_id = data['id']).first()
        
            
                

                
		except:
			return jsonify({
				'message' : 'Token is invalid !!'
			}), 401
		# returns the current logged in users contex to the routes
		return f(current_user, *args, **kwargs)

	return decorated





@app.route('/api/public/login',methods=['POST'])
def getjwttoken():
    keyjson = {'username':request.json['username'],'password':request.json['password']}
   
    for k , v in keyjson.items():
        if k == 'username':
            username = v
        elif k=='password':
            password = v  

    print(username)
    print(password)          
    user = db.session.query(User).select_from(User).filter(and_(User.user_name==username, User.password==password)).all()

    if not user:
        return make_response('User not found',401)

    for usr in user:
        print("printing user data from db")
        dbuser=usr.user_name
        dbpassword =usr.password
    print(dbpassword,"::",password)

    token  =  jwt.encode ({
            'id':usr.user_id,
            'username':usr.user_name,
            'password':usr.password
           },app.config['SECRET_KEY']
           ) 

    return make_response(jsonify({'token':token.decode('UTF-8')}),200)
 





# @app.route('/api/auth/consumer/cart',methods=['GET']) 
# @token_required
# def getcart_asjack(currentuser):
#     print(currentuser.user_id)
#     print(currentuser.user_name)
#     if currentuser.user_name == 'jack':


#         return jsonify("welcome jack")
#     else:
#         return jsonify("Sorry !!!Only jack have rights")




# @app.route('/api/auth/seller/product/<int:productid>',methods=['GET']) 
# @token_required
# def getproductid(currentuser,productid):
#     print(currentuser.user_id)
#     print(currentuser.user_name)
#     if currentuser.user_name == 'jack':


#         return jsonify("welcome jack")
#     else:
#         return jsonify("Sorry !!!Only jack have rights")


@app.route('/api/auth/seller/product',methods=['GET']) 
@token_required
def getproducts(currentuser):
    #print(currentuser.user_role)
    if currentuser.user_role == 2:
        # print(currentuser.user_id)
        # print(currentuser.user_name)
    # return str(currentuser.user_name)


# # result  = db.session.query(Product,Category,User).\
# #         select_from(Product).join(Category).join(User).filter(Product.product_name==productname).all()

        products = db.session.query(Product,Category,User).select_from(Product).join(Category).join(User).\
            filter(Product.seller_id==currentuser.user_id).all()

        if not products:
            return make_response('Product not found ',404)
        productlist =[]
        for prod, cat,usr in products:
            print(prod.category_id)
            productlist.append({
                'Category':{
                    'category_id':prod.category_id,
                    'category_name':cat.category_name
                },
                'price':prod.price,
                'product_id':prod.product_id,
                'seller_id':prod.seller_id

                
            })

        return make_response(jsonify(productlist),200) 

    return make_response(jsonify("Invalid seller Check with seller token"))    

# def test(self):
#     url='/api/public/login'
#     user_credentials ='apple:pass_word'
#     valid_credentials= base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
#     response = self.client.get(url,headers={'Authorization':'Basic'+valid_credentials})
#     assert response.status_code==200
#     token=response.json['token']
#     print(token)



# url='/api/public/login'
# user_credentials ='apple:pass_word'
# valid_credentials= base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
# print(valid_credentials)









# @app.route('/user', methods =['GET'])
# @token_required
# def get_all_users(current_user):
# 	# querying the database
# 	# for all the entries in it
# 	users = User.query.all()
# 	# converting the query objects
# 	# to list of jsons
# 	output = []
# 	for user in users:
# 		# appending the user data json
# 		# to the response list
# 		output.append({
# 			'name' : user.name,
# 			'email' : user.email
# 		})

# 	return jsonify({'users': output})

# @app.route('/api/public/product/', methods= ['GET'])
# def search_product():
#     # productname = '"{}"'.format('crocin')
#     # print("productname",productname)
#     # products = db.session.query(Product,Category).join(Product).filter(Product.product_name==productname).all()
#     products = db.session.query(Product).join(Category).all()
#     output = []
#     for out in products:
#         output.append({
#             'Category': [{
#                 'category_id': out.category_id
#             }]
            
#         })
#     return jsonify(output)

 


# result = db.session.query(Product).join(Category).join(User).filter(Product.product_name=='crocin').all()
# for re in result:
#   print(re)




#app.route('/api/public/product/search?keyword=<string:productname>', methods = ['GET'])
# app.route('/api/public/product/search', methods = ['GET'])
# def search_product(productname):
  
    
# @app.route('/api/public/login', methods=['POST'])
# @token_required
# def authenticate():

#     user = User.query.all()
#     username = user.user_name
#     password = user.password

#     if not user:
#         return make_response('User entry not found ',401)
    

#     url = "/api/public/login"
#     data = {
# 	"username": username,
# 	"password": password
	
#       } 



#     response = request.post(url, json=data)

#     print("Status Code", response.status_code)
#     print("JSON Response ", response.json())


if __name__=='__main__':
    app.run(port=5000,debug=True) 