from flask import Flask, request
from flask_restful import Resource,Api

app = Flask(__name__)
api = Api(app)
items =[]
class Student(Resource):
    def get(self, name):
        for item in items:
            if item['name'] == name:
                return item
        return {'item':None}, 404        

    def post(self, name):
        data = request.get_json(silent=True)
        item = {'name':name, 'price': data['price']}
        items.append(item)
        return item ,201

class ItemList(Resource):
     def get(self):
        
        return {'item':items}
api.add_resource(Student, '/student/<string:name>')
api.add_resource(ItemList, '/items')

if __name__ == '__main__':
    app.run(port = 5000)