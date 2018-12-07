from flask import jsonify
from flask_restful import Api, Resource, abort, reqparse
from ..models import Course, User
from . import api_bp

api = Api(api_bp)


def remove_hidden_attr(d):
    return {key: value for key, value in d.items() if key[0] != '_'}


class Courses(Resource):
    def process_args(args):
        final_args = {}
        del args['key']

        for k in args.keys():
            if args[k] is not None:
                final_args[k] = args[k]

        return final_args

    def get(self, typ):
        # print(dir(Resource))
        # adding parameters to api

        # select api requires the primary keys: course id and term, and api key
        if typ == 'select':
            parser = reqparse.RequestParser()
            # note that an error in passing in arguments here will not result
            # in 400 error
            parser.add_argument(
                'course_id',
                required=True,
                help="course_id cannot be blank for select api")
            parser.add_argument("term", required=True,
                                help="term cannot be blank for select api !")
            parser.add_argument("key", required=True,
                                help="key cannot be blank!")

        # search api can accept any number and combination of prameters
        # requires api key
        elif typ == 'search':
            parser = reqparse.RequestParser()
            parser.add_argument('term')
            parser.add_argument("course_id")
            parser.add_argument("prefix_name")
            parser.add_argument("prefix_long_name")
            parser.add_argument("division_code",)
            parser.add_argument('division_name')
            parser.add_argument("campus_code")
            parser.add_argument("campus_name",)
            parser.add_argument('school_code')
            parser.add_argument('school_name')
            parser.add_argument('department_code')
            parser.add_argument('department_name')
            parser.add_argument('subterm_code')
            parser.add_argument('subterm_name')
            parser.add_argument('call_number')
            parser.add_argument('num_enrolled')
            parser.add_argument('max_size')
            parser.add_argument('enrollment_status')
            parser.add_argument('num_fixed_units')
            parser.add_argument('min_units')
            parser.add_argument('max_units')
            parser.add_argument('course_name')
            parser.add_argument('type_code')
            parser.add_argument('type_name')
            parser.add_argument('approval')
            parser.add_argument('bulletin_flags')
            parser.add_argument('class_notes')
            parser.add_argument('meeting_times')
            parser.add_argument('instructor_name')
            parser.add_argument("key", required=True,
                                help="key cannot be blank!")

        else:
            abort(
                400,
                status=400,
                message=f"Bad Request. GET api/courses/select?"
                f"or api/courses/search?")

        args = parser.parse_args(strict=True)
        key = args["key"]
        datum = {}

        # verify the API key
        if User.verify(key):
            # will return processed arguments, if there is an incorrect
            # argument then it will return the first incorrect argument
            args = Courses.process_args(args)
            if isinstance(args, str):
                abort(
                    400,
                    status=400,
                    message=f"Invalid parameter: {args}")

            elif isinstance(args, dict):
                if typ == 'select':
                    # if select api, then use get method by passing in primary
                    # keys
                    result = Course.query.get(
                        (args['term'], args['course_id']))
                    if not result:
                        abort(
                            404,
                            status=404,
                            message=f"Course with course_id = "
                                    f"{args['course_id']} and term = "
                                    f"{args['term']} does not exist")
                    else:
                        datum['status'] = 200
                        datum['data'] = remove_hidden_attr(result.__dict__)

                elif typ == 'search':
                    # for seach api, then use filter through db
                    print(args)
                    result = Course.query.filter_by(**args).all()
                    if not result:
                        abort(404, status=404,
                              message=f'No courses with parameters {args}')

                    else:
                        datum['data'] = [
                            remove_hidden_attr(
                                i.__dict__) for i in result]
                return jsonify(datum)
            # if API key was not verified
        else:
            abort(403, status=403,
                  message="User couldn't be verified")


# api/courses/search dynamically searches by whatever parameters they input
# api/courses/term/course_id passes a specific course
api.add_resource(Courses, '/courses/<typ>')
