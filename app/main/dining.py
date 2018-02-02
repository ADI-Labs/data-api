from flask import Flask, render_template, Response, redirect, url_for, request, session, abort
from flask_restful import Resource, Api
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from . import main

class Dining(Resource):
    def get(self, dininghall_id):
        return {dorm_id: todos[dininghall_id]}

api.add_resource(Dining, '/Dining/<string:dininghall_id>/<string:day>')