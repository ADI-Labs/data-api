from flask import jsonify
from flask_restful import Api, Resource, abort
from ..models import Course
from . import api_bp

api = Api(api_bp)


def remove_hidden_attr(d):
    return {key: value for key, value in d.items() if key[0] != '_'}


class Courses(Resource):
    def get(self, cid, term):
        result = Course.query.filter_by(course_id=cid, term=term).first()
        datum = {}

        if result is None:
            abort(404, status=400, message=f'Course {cid} for term {term} does not exist')

        datum['status'] = 200
        datum['data'] = [remove_hidden_attr(result.__dict__)]
        return jsonify(datum)

    """we are not going to have sets and deletes"""


api.add_resource(Courses, '/courses/<term>/<cid>')
