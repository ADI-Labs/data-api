from flask import Flask, render_template, Response, redirect, url_for, request, session, abort
from flask_restful import Resource, Api
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from . import main

class Students(Resource):
    def get(self, student_id):
        return {student_id: todos[student_id]}

api.add_resource(Student, '/Students/<string:student_id>')