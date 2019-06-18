# -*- coding: utf-8 -*-
from flask import Flask
from flask import abort
from flask import jsonify
from flask import request
from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

# app.config['MONGO_DBNAME'] = 'zhejiang'
# app.config['MONGO_URI'] = 'mongodb://127.0.0.1:27017/rest'  # 如果部署在本上，其中ip地址可填127.0.0.1
# mongo = PyMongo(app)

MONGO_HOST = '106.14.176.62'
MONGO_PORT = 27017

# 同时处理的最大线程数
executor = ThreadPoolExecutor(10)


def link():
    client = MongoClient(host=MONGO_HOST, port=MONGO_PORT)
    mo_db = client['zhejiang']
    coll = mo_db['sheng']
    return coll


@app.route('/search', methods=['POST'])
def add_user():
    name = request.json['name']
    output = {'name': name, 'status': 1}
    executor.submit(func(), name)
    return jsonify({'result': output})


def func(name):
    print(name)

    # pwd = request.json['pwd']
    # star_id = star.insert({'name': name})

    # coll = link()
    # new_star = coll.find_one({'corpNameBy': name})
    # if new_star:
    #     output = {'status': 1}
    #     return jsonify({'result': output})
    # else:
    #     output = {'status': 2}
    #     return jsonify({'result': output})


# @app.route('/login', methods=['GET'])
# def get_all_users():
#   star = mongo.db.userInfo.find()
#   output = []
#   for s in star:
#     output.append({'name' : s['name'], 'pwd' : s['pwd']})
#   return jsonify({'result' : output})


# @app.route('/modify/<string:name>', methods=['PUT'])
# def update_user(name):
#     user = mongo.db.userInfo.find({"name": name})
#     output = []
#     for s in user:
#       output.append({'name': s['name'], 'pwd': s['pwd']})
#     if len(output) == 0:
#       abort(404)
#     mongo.db.userInfo.update({"name": name}, {'$set': {"name": "LZ111"}})
#     return jsonify({'result': output})


# @app.route('/delete/<string:name>', methods=['DELETE'])
# def delete_user(name):
#     user = mongo.db.userInfo.find({"name": name})
#     output = []
#     for s in user:
#         output.append({'name': s['name'], 'pwd': s['pwd']})
#     if len(output) == 0:
#         abort(404)
#     mongo.db.userInfo.remove({'name': name})
#     return jsonify({'result': True})


if __name__ == '__main__':
    # app.run(host = '0.0.0.0', port = 80, debug = True)
    app.run()
