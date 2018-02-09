from flask import Flask
from flask_restful import Resource, Api
from . import main

class Housing(Resource):
    def get(self, dorm_id):
        return {dorm_id: todos[dorm_id]}

api.add_resource(Housing, '/Housing/<string:dorm_id>')