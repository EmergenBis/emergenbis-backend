from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse, abort
from flask_pymongo import pymongo
from flask_cors import CORS
from bson.json_util import dumps, ObjectId
import db_config as database

#Resources
from res.user import User
#from res.users import Users
from res.profile import Profile
from res.post import Posts
from res.post_type import Post_type
from res.arduino import Arduino


app = Flask(__name__)
api = Api(app)

CORS(app)

@app.route('/all/users/')
def get_all_users():
    response = list(database.db.users.find())

    for document in response:
        document["_id"] = str(document['_id'])

    return jsonify(response)

@app.route('/all/profiles/')
def get_all_profiles():
    response = list(database.db.profiles.find())

    for document in response:
        document["_id"] = str(document['_id'])

    return jsonify(response)

@app.route('/all/posts/')
def get_all_posts():
    response = list(database.db.posts.find())

    for document in response:
        document["_id"] = str(document['_id'])

    return jsonify(response)

@app.route('/all/post_types/')
def get_all_post_types():
    response = list(database.db.post_types.find())

    for document in response:
        document["_id"] = str(document['_id'])

    return jsonify(response)

@app.route('/all/arduinos/')
def get_all_arduinos():
    response = list(database.db.arduino.find())

    for document in response:
        document["_id"] = str(document['_id'])

    return jsonify(response)


api.add_resource(User, '/new_user/', '/<string:_id>', '/<string:by>:<string:data>')
api.add_resource(Profile, '/new_profile/',  '/<string:_id>', '/<string:by>:<string:data>')
api.add_resource(Posts, '/new_post/', '/<string:_id>', '/<string:by>:<string:data>')
api.add_resource(Post_type, '/new_post_type/', '/<string:_id>','/<string:by>:<string:data>')
api.add_resource(Arduino, '/new_arduino/', '/<string:_id>', '/<string:by>:<string:data>')



if __name__ == '__main__':
    app.run(load_dotenv = True)