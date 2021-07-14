from flask import jsonify, request
from flask_restful import Resource, abort
from flask_pymongo import pymongo
from bson.json_util import ObjectId
import db_config as database


class Posts(Resource):

    def get(self, by, data):
        response = list(database.db.posts.find(self.abort_if_not_exist(by, data)))
        for doc in response:
            doc['_id'] = str(doc['_id'])

        return jsonify(response)

    def post(self):
        _id = str(database.db.posts.insert_one({
            'profile_id': request.json['profile_id'],
            'color': request.json['color'],
            'alarm_activation': request.json['alarm_activation'],
            'send_notification': request.json['send_notification'],
            'appears_on_feed': request.json['appears_on_feed'],
            'description': request.json['description'],
            'location': request.json['location'],
            'created_at': request.json['created_at'],
            'type_id': request.json['type_id'],
        }).inserted_id)

        return jsonify({"_id": _id})

    def put(self, by, data):
        response = self.abort_if_not_exist(by, data)

        for key, value in request.json.items():
            response[key] = value

        database.db.posts.update_one({'_id':ObjectId(response['_id'])},
        {'$set':{
            'profile_id': response['profile_id'],
            'color': response['color'],
            'alarm_activation': response['alarm_activation'],
            'send_notification': response['send_notification'],
            'appears_on_feed': response['appears_on_feed'],
            'description': response['description'],
            'location': response['location'],
            'created_at': response['created_at'],
            'type_id': response['type_id'],
        }})

        response['_id'] = str(response['_id'])
        return jsonify(response)

    def delete(self, by, data):
        response = self.abort_if_not_exist(by, data)
        database.db.posts.delete_one({"_id":response['_id']})
        response['_id'] = str(response['_id'])
        return jsonify({"deleted":response})


    def abort_if_not_exist(self,by,data):
        if by == "_id":
            response = database.db.posts.find_one({"_id":ObjectId(data)})
        else:
            response = database.db.posts.find_one({f"{by}": data})

        if response:
            return response
        else:
            abort(jsonify({"status":404, f"{by}": f"{data} not found"}))