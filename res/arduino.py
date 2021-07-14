from flask import jsonify, request
from flask_restful import Resource, abort
from flask_pymongo import pymongo
from bson.json_util import ObjectId
import db_config as database


class Arduino(Resource):

    def get(self, by, data):
        response = list(database.db.arduino.find(self.abort_if_not_exist(by, data)))
        for doc in response:
            doc['_id'] = str(doc['_id'])

        return jsonify(response)

    def post(self):
        _id = str(database.db.arduino.insert_one({
            'zone': request.json['zone'],
            'activated': request.json['activated'],
        }).inserted_id)

        return jsonify({"_id": _id})

    def put(self, by, data):
        response = self.abort_if_not_exist(by, data)

        for key, value in request.json.items():
            response[key] = value

        database.db.arduino.update_one({'_id':ObjectId(response['_id'])},
        {'$set':{
            'zone': response['zone'],
            'activated': response['activated'],
        }})

        response['_id'] = str(response['_id'])
        return jsonify(response)

    def delete(self, by, data):
        response = self.abort_if_not_exist(by, data)
        database.db.arduino.delete_one({"_id":response['_id']})
        response['_id'] = str(response['_id'])
        return jsonify({"deleted":response})


    def abort_if_not_exist(self,by,data):
        if by == "_id":
            response = database.db.arduino.find_one({"_id":ObjectId(data)})
        else:
            response = database.db.arduino.find_one({f"{by}": data})

        if response:
            return response
        else:
            abort(jsonify({"status":404, f"{by}": f"{data} not found"}))