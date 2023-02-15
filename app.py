from crypt import methods
import json
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS , cross_origin #ARREGLAR CORS

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost/pythonreactdb'
mongo = PyMongo(app) #es la conexion para la base de datos

CORS(app, support_credentials=True) #front end

#colecciones
db = mongo.db.users #coleccion #1


#crear usuario
@app.route('/users', methods=['POST'])
@cross_origin(supports_credentials=True)
def createUser():
    id = db.insert_one({
        "name": request.json['name'],
        "email": request.json['email'],
        "password": request.json['password']
    })
    return jsonify(str(ObjectId(id)))

#listar TODOS los usuarios
@app.route('/users', methods=['GET']) #obtener usuario
def getUsers():
    users = []
    for doc in db.find():
        users.append({
            '_id' : str(ObjectId(doc['_id'])),
            'name': doc['name'],
            'email': doc['email'],
            'password': doc['password']
        })
    return jsonify(users)



#listar solo un usuario
@app.route('/user/<id>', methods=['GET']) #solo uno
def getUser(id):
    user = db.find_one({'_id': ObjectId(id)})
    print(user)
    return jsonify({
        '_id': str(ObjectId(user['_id'])),
        'name': user['name'],
        'email': user['email'],
        'password': user['password']
    })



#eliminar un usuario
@app.route('/users/<id>', methods=['DELETE']) #delete user
def deleteUser(id):
    db.delete_one({'_id': ObjectId(id)})
    return jsonify({'msg': 'user deleted'})



#actualizar un usuario
@app.route('/users/<id>', methods=['PUT']) #update use
def updateUser(id):
    db.update_one({'_id': ObjectId(id)}, {'$set': {
        'name': request.json['name'],
        'email': request.json['email'],
        'password': request.json['password']
    }})
    return jsonify({'msg': 'user updated'})



if __name__ == "__main__":
    app.run(debug=True)
