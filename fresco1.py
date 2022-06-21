
import requests


payload = {"username":"apple",
"password":"pass_word"
}
r = requests.post('http://127.0.0.1:5000/api/public/login', json = payload)
print(r.text)
# data = 'crocin'
# r = requests.get('http://127.0.0.1:5000/api/public/product/search/')
# print(r.json())
# class user(db.Model):
#     user_id = db.Column(db.Integer, primary_key=True , unique= True)
#     user_name = db.Column(db.String)
    
#     #role_id = db.relationship(Role, backref='user',UserList=False)