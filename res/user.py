from flask import jsonify, request
from flask_restful import Resource, abort
from flask_pymongo import pymongo
from bson.json_util import ObjectId
import db_config as database


class User(Resource):

    def get(self, by, data):
        response = list(database.db.users.find(self.abort_if_not_exist(by, data)))
        for doc in response:
            doc['_id'] = str(doc['_id'])

        return jsonify(response)

    def post(self):
        _id = str(database.db.users.insert_one({
            'username': request.json['username'],
            'first_name': request.json['first_name'],
            'last_name': request.json['last_name'],
            'email': request.json['email'],
            'is_staff': request.json['is_staff'],
            'is_active': request.json['is_active'],
            'date_joined': request.json['date_joined'],
        }).inserted_id)

        return jsonify({"_id": _id})

    def put(self, by, data):
        response = self.abort_if_not_exist(by, data)

        for key, value in request.json.items():
            response[key] = value

        database.db.users.update_one({'_id':ObjectId(response['_id'])},
        {'$set':{
            'username': response['username'],
            'first_name': response['first_name'],
            'last_name': response['last_name'],
            'email': response['email'],
            'is_staff': response['is_staff'],
            'is_active': response['is_active'],
            'date_joined': response['date_joined'],
        }})

        response['_id'] = str(response['_id'])
        return jsonify(response)

    def delete(self, by, data):
        response = self.abort_if_not_exist(by, data)
        database.db.users.delete_one({"_id":response['_id']})
        response['_id'] = str(response['_id'])
        return jsonify({"deleted":response})


    def abort_if_not_exist(self,by,data):
        if by == "_id":
            response = database.db.users.find_one({"_id":ObjectId(data)})
        else:
            response = database.db.users.find_one({f"{by}": data})

        if response:
            return response
        else:
            abort(jsonify({"status":404, f"{by}": f"{data} not found"}))