from flask import jsonify
from flask_restful import Api, Resource, abort, reqparse
from ..models import Course, User
from . import api_bp

api = Api(api_bp)
parser = reqparse.RequestParser()
parser.add_argument("key")


def remove_hidden_attr(d):
    return {key: value for key, value in d.items() if key[0] != '_'}


class Courses(Resource):
    def get(self, cid, term):
        key = parser.parse_args()["key"]
        datum = {}
        if User.verify(self, key):
            result = Course.query.filter_by(course_id=cid, term=term).first()

            if result is None:
                abort(404, status=400,
                      message=f'Course {cid} for term {term} does not exist')

            datum['status'] = 200
            datum['data'] = [remove_hidden_attr(result.__dict__)]
        else:
            datum['status'] = 400
            datum['error'] = "User couldn't be verified"
            datum['data'] = {}
        return jsonify(datum)


api.add_resource(Courses, '/courses/<term>/<cid>/<key>')
