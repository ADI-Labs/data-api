from flask import jsonify
from flask_restful import Api, Resource, abort
from .. import db
from ..models import Course, User, Dining
from . import api_bp

api = Api(api_bp)


def remove_hidden_attr(d):
    return {key: value for key, value in d.items() if key[0] != '_'}


class Courses(Resource):
    def get(self, cid, term, key):
        if User.verify(key) == None:
            return "invalid api key"

        result = Course.query.filter_by(course_id=cid, term=term).first()
        datum = {}

        if result is None:
            abort(404, status=400, message=f'Course {cid} for term {term} does not exist')

        datum['status'] = 200
        datum['data'] = [remove_hidden_attr(result.__dict__)]
        return jsonify(datum)

    """we are not going to have sets and deletes"""


class Dining(Resource):
    def get(self, term, key):
        if User.verify(key) == None:
            return "invalid api key"

        result = Dining.query.filter_by(term=term).first()
        datum = {}

        if result is None:
            abort(404, status=400, message=f'Dining for term {term} does not exist')

        datum['status'] = 200
        datum['data'] = [remove_hidden_attr(result.__dict__)]
        return jsonify(datum)


class Housing(Resource):
    def get(self, term, key):
        if User.verify(key) == None:
            return "invalid api key"

        result = Housing.query.filter_by(term=term).first()
        datum = {}

        if result is None:
            abort(404, status=400, message=f'Housing for term {term} does not exist')

        datum['status'] = 200
        datum['data'] = [remove_hidden_attr(result.__dict__)]
        return jsonify(datum)


api.add_resource(Courses, '/courses/<term>/<cid>/<key>')
