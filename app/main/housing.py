from flask import Flask, render_template, Response, redirect, url_for, request, session, abort
from flask_restful import Resource, Api
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from . import main

class Housing(Resource):
    def get(self, dorm_id):
        return {dorm_id: todos[dorm_id]}

api.add_resource(Housing, '/Housing/<string:dorm_id>')