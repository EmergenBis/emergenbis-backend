from flask import jsonify, request
from flask_restful import Resource, abort
from flask_pymongo import pymongo
from bson.json_util import ObjectId
import db_config as database


class Post_type(Resource):

    def get(self, by, data):
        response = list(database.db.post_types.find(self.abort_if_not_exist(by, data)))
        for doc in response:
            doc['_id'] = str(doc['_id'])

        return jsonify(response)

    def post(self):
        _id = str(database.db.post_types.insert_one({
            'name': request.json['name'],
            'arduino_id': request.json['arduino_id'],
        }).inserted_id)

        return jsonify({"_id": _id})

    def put(self, by, data):
        response = self.abort_if_not_exist(by, data)

        for key, value in request.json.items():
            response[key] = value

        database.db.post_types.update_one({'_id':ObjectId(response['_id'])},
        {'$set':{
            'name': response['name'],
            'arduino_id': response['arduino_id'],
        }})

        response['_id'] = str(response['_id'])
        return jsonify(response)

    def delete(self, by, data):
        response = self.abort_if_not_exist(by, data)
        database.db.post_types.delete_one({"_id":response['_id']})
        response['_id'] = str(response['_id'])
        return jsonify({"deleted":response})


    def abort_if_not_exist(self,by,data):
        if by == "_id":
            response = database.db.post_types.find_one({"_id":ObjectId(data)})
        else:
            response = database.db.post_types.find_one({f"{by}": data})

        if response:
            return response
        else:
            abort(jsonify({"status":404, f"{by}": f"{data} not found"}))