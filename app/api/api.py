from flask import jsonify
from flask_restful import Api, Resource, abort
from .. import db
from ..models import Course
from . import api_bp

api = Api(api_bp)


class Courses(Resource):
    def get(self, cid, term):
        result = db.session.query(Course).filter_by(term
                =term).filter_by(course_id=cid).scalar()
        if result is None:
            abort(404,
                  message=
                  "Course {} for term {} doesn't exist".format(cid, term))
        return jsonify(result)

    """we are not going to have sets and deletes"""


api.add_resource(Courses, '/courses/<term>/<cid>')
