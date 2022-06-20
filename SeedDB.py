import sqlite3
from crypt import methods
from flask import Flask, jsonify,request
app = Flask(__name__)


conn = sqlite3.connect('seeding.sqlite3')
cur = conn.cursor()

## conn.commit()
## conn.commit()



## post request  store 
@app.route('/store',methods = ['POST'])
def create_store():
    new_store = request.get_json()
    return jsonify(new_store)
    


## get a store 
@app.route('/api/public/product/search?keyword=<string:productname>', methods=['GET'])
def get_store(productname):
    cur.execute("SELECT  * FROM Product where product_name = '{}' JOIN Category ON Category.category_id = Product.category_id").__format__(productname)


# ## get all stores 
# @app.route('/store')
# def get_stores():
#     return jsonify({'stores':stores})

# ## add item to store 
# @app.route('/store/<string:name>/item', methods= ['POST'])
# def create_item_in_store(name):
#     pass


# ## get item from a store 
# @app.route('/store/<string:name>/item')
# def get_item_in_store():
#     pass






if __name__=='__main__':
    app.run(port=5000) 