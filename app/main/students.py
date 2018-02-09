from flask import Flask
from flask_restful import Resource, Api
from . import main

class Students(Resource):
    def get(self, student_id):
        return {student_id: todos[student_id]}

api.add_resource(Student, '/Students/<string:student_id>')