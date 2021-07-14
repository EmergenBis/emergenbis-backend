from flask import jsonify, request
from flask_restful import Resource, abort
from flask_pymongo import pymongo
from bson.json_util import ObjectId
import db_config as database


class Profile(Resource):

    def get(self, by, data):
        response = list(database.db.profiles.find(self.abort_if_not_exist(by, data)))
        for doc in response:
            doc['_id'] = str(doc['_id'])

        return jsonify(response)

    def post(self):
        _id = str(database.db.profiles.insert_one({
            'user_id': request.json['user_id'],
            'university_id': request.json['university_id'],
            'group': request.json['group'],
            'verified': request.json['verified'],
        }).inserted_id)

        return jsonify({"_id": _id})

    def put(self, by, data):
        response = self.abort_if_not_exist(by, data)

        for key, value in request.json.items():
            response[key] = value

        database.db.profiles.update_one({'_id':ObjectId(response['_id'])},
        {'$set':{
            'user_id': response['user_id'],
            'university_id': response['university_id'],
            'group': response['group'],
            'verified': response['verified'],
        }})

        response['_id'] = str(response['_id'])
        return jsonify(response)

    def delete(self, by, data):
        response = self.abort_if_not_exist(by, data)
        database.db.profiles.delete_one({"_id":response['_id']})
        response['_id'] = str(response['_id'])
        return jsonify({"deleted":response})


    def abort_if_not_exist(self,by,data):
        if by == "_id":
            response = database.db.profiles.find_one({"_id":ObjectId(data)})
        else:
            response = database.db.profiles.find_one({f"{by}": data})

        if response:
            return response
        else:
            abort(jsonify({"status":404, f"{by}": f"{data} not found"}))