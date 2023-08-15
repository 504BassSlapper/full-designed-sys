## pika use for rabbit mq
import os, gridfs, pika, json
from flask import Flask, request, send_file
from flask_pymongo import PyMongo
from auth import validate
from auth_svc import access
from storage import util

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/videos"

mongo = PyMongo(app)

fs = gridfs.GridFS(mongo.db)

# reference to rabbit mq host
connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))

channel = connection.channel()


@app.route("/login", mothods=["POST"])
def login():
    token, err = access.login(request)

    if not err:
        return token
    else:
        return err


@app.route("/upload", methods=["POST"])
def upload():
    access, err = validate.token(request)
    access = json.load(access)
    if access["admin"]:
        if len(request.files > 1) or len(request.files) < 1:
            return "exactly one file required", 400
        for _, f in request.files.items():
            err = util.upload(f, fs, channel, access)
            if err:
                return err
        return "success", 200
    else:
        return "not authorized", 401


@app.route("/dowload", methods=["GET"])
def download():
    pass


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
