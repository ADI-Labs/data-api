from flask import Flask
from flask_restful import Resource, Api
from . import main

class Courses(Resource):
    def get(self, dept_id, course_id):
        return {course_id: todos[course_id]}

api.add_resource(Courses, '/Courses/<string:dept_id>/<string:course_id>')