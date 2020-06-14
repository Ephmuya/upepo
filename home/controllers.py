from flask import Blueprint, jsonify, request
home = Blueprint("home", __name__)

upepo_apis = {
    "readings": "/upepo/v1/readings",
    "meters": "/upepo/v1/meters",
    "latest": "/upepo/v1/latest",
}


@home.route("/")
def index():
    return jsonify(status=200 ,apis =upepo_apis)
