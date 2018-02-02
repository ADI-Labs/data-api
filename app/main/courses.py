from flask import Flask, render_template, Response, redirect, url_for, request, session, abort
from flask_restful import Resource, Api
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from . import main

class Courses(Resource):
    def get(self, dept_id, course_id):
        return {course_id: todos[course_id]}

api.add_resource(Courses, '/Courses/<string:dept_id>/<string:course_id>')