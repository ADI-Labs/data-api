from flask import Flask
from flask_restful import Resource, Api
from . import main

class Dining(Resource):
    def get(self, dininghall_id):
        return {dorm_id: todos[dininghall_id]}

api.add_resource(Dining, '/Dining/<string:dininghall_id>/<string:day>')