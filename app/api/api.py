from flask import jsonify
from flask_restful import Api, Resource, abort
from .. import db
from ..models import Course
from . import api_bp

api = Api(api_bp)


class Courses(Resource):
    def get(self, cid, term, key):
        result = db.session.query(Course)\
            .filter_by(term=term).filter_by(course_id=cid).scalar()
        datum = {}

        if result is None:
            abort(404, message="Course {} for term {} doesn't exist"
                  .format(cid, term))

        for course in result.__mapper__.columns.keys():
            datum[course] = getattr(result, course)

        response={"status": "200", "reason": "OK", "data": datum}

        return jsonify(response)

    """we are not going to have sets and deletes"""


api.add_resource(Courses, '/courses/<term>/<cid>/<key>')
