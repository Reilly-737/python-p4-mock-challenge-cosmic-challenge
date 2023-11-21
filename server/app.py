#!/usr/bin/env python3

from models import db, Scientist, Mission, Planet
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def home():
    return ''
@app.route("/scientists")
def scientists():
    scientists = [scientist.to_dict(rules=("-missions",)) for scientist in Scientist.query]
    return make_response(scientists, 200)

@app.route("/scientists/<int:id>")
def scientist_id(id):
    if scientist:= db.session.get(Scientist, id):
        return make_response(scientist.to_dict(), 200)
    return make_response({"error": "Scientist not found"}, 404)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
