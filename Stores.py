

from crypt import methods
from flask import Flask, jsonify,request
app = Flask(__name__)









stores = [
    {
        'name': 'My Store',
        'item':[
            {
                'itemname':'My Item',
                'price':50
            }
        ]

    }
]



## post request  store 
@app.route('/store',methods = ['POST'])
def create_store():
    new_store = request.get_json()
    return jsonify(new_store)
    


## get a store 
@app.route('/store/<string:name>')
def get_store(name):
    pass


## get all stores 
@app.route('/store')
def get_stores():
    return jsonify({'stores':stores})

## add item to store 
@app.route('/store/<string:name>/item', methods= ['POST'])
def create_item_in_store(name):
    pass


## get item from a store 
@app.route('/store/<string:name>/item')
def get_item_in_store():
    pass






if __name__=='__main__':
    app.run(port=5000) 