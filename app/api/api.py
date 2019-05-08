from flask import jsonify
from flask_restful import Api, Resource, abort, reqparse
from ..models import Course, User, Student, Residence
from ..models import get_column_names, get_primary_key_names
from . import api_bp

api = Api(api_bp)
API_KEY_TERM = ["key"]


def remove_hidden_attr(d):
    return {key: value for key, value in d.items() if key[0] != '_'}


class Courses(Resource):
    def get(self, typ):
        # select api requires the primary keys: course id and term, and api key
        if typ == 'select':
            parser = reqparse.RequestParser()
            # note that an error in passing in arguments here will not result
            # in 400 error
            required_terms = get_primary_key_names(Course)
            required_terms.append("key")
            print(required_terms)
            add_required_to_parser(parser, required_terms)

        # search api can accept any number and combination of parameters
        # requires api key
        elif typ == 'search':
            parser = reqparse.RequestParser()
            search_terms = get_column_names(Course)
            add_all_to_parser(parser, search_terms)
            add_required_to_parser(parser, API_KEY_TERM)

        else:
            abort(
                400,
                status=400,
                message=f"Bad Request. GET api/courses/select?"
                f"or api/courses/search?")

        args = parser.parse_args(strict=True)
        key = args["key"]
        response = {}

        # verify the API key
        if User.verify(key):
            # will return processed arguments, if there is an incorrect
            # argument then it will return the first incorrect argument
            args = process_args(args)
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
                        response['status'] = 200
                        response['data'] = remove_hidden_attr(result.__dict__)

                elif typ == 'search':
                    # for seach api, then use filter through db
                    print(args)
                    result = Course.query.filter_by(**args).all()
                    if not result:
                        abort(404, status=404,
                              message=f'No courses with {args}')

                    else:
                        response['data'] = [
                            remove_hidden_attr(
                                i.__dict__) for i in result]
                return jsonify(response)
            # if API key was not verified
        else:
            abort(403, status=403,
                  message="User couldn't be verified")


class Students(Resource):
    def get(self, typ):
        # select api requires the primary key: uni
        if typ == 'select':
            parser = reqparse.RequestParser()
            # note that an error in passing in arguments here will not result
            # in 400 error
            required_terms = get_primary_key_names(Student)
            required_terms.append("key")
            add_required_to_parser(parser, required_terms)

        # search api can accept any number and combination of prameters
        # requires api key
        elif typ == 'search':
            parser = reqparse.RequestParser()
            search_terms = get_column_names(Student)
            add_all_to_parser(parser, search_terms)
            add_required_to_parser(parser, API_KEY_TERM)

        else:
            abort(
                400,
                status=400,
                message=f"Bad Request. GET api/students/select?"
                f"or api/students/search?")

        args = parser.parse_args(strict=True)
        key = args["key"]
        response = {}

        # verify the API key
        if User.verify(key):
            # will return processed arguments, if there is an incorrect
            # argument then it will return the first incorrect argument
            args = process_args(args)
            if isinstance(args, str):
                abort(
                    400,
                    status=400,
                    message=f"Invalid parameter: {args}")

            elif isinstance(args, dict):
                if typ == 'select':
                    # if select api, then use get method by passing in primary
                    # keys
                    result = Student.query.get(args['uni'])
                    if not result:
                        abort(
                            404,
                            status=404,
                            message=f"Student with uni = "
                            f"{args['uni']} does not exist")
                    else:
                        response['status'] = 200
                        response['data'] = remove_hidden_attr(result.__dict__)

                elif typ == 'search':
                    # for seach api, then use filter through db
                    result = Student.query.filter_by(**args).all()
                    if not result:
                        abort(404, status=404,
                              message=f'No students with {args}')

                    else:
                        response['data'] = [
                            remove_hidden_attr(
                                i.__dict__) for i in result]
                return jsonify(response)
        # if API key was not verified
        else:
            abort(403, status=403,
                  message="User couldn't be verified")


SEARCHABLE_ATTRIBUTES = [
    'name',
    "residential_area",
    "building_type",
    "room_type",
    "class_make_up",
    "bathroom",
    "kitchen",
    "bike_storage",
    "print_station",
    "fitness_room",
    "computer_lab",
    "ac",
    "piano",
    "expand_special"
]


class Residences(Resource):
    def set_expand_group(self, args):
        if args.get('expand_special', False):
            args["_expand_category"] = "expand"
        else:
            args["_expand_category"] = "group"
        if args.get('expand_special'):
            del args['expand_special']

    def get(self, typ):
        # select api requires the primary key: name
        if typ == 'select':
            parser = reqparse.RequestParser()
            # note that an error in passing in arguments here will not result
            # in 400 error
            required_terms = get_primary_key_names(Residence)
            required_terms.append("key")
            add_required_to_parser(parser, required_terms)

        # search api can accept any number and combination of prameters
        # requires api key
        elif typ == 'search':
            parser = reqparse.RequestParser()
            add_all_to_parser(parser, SEARCHABLE_ATTRIBUTES)
            add_required_to_parser(parser, API_KEY_TERM)

        else:
            abort(
                400,
                status=400,
                message=f"Bad Request. GET api/residences/select?"
                f"or api/residences/search?")

        args = parser.parse_args(strict=True)
        key = args["key"]
        response = {}

        # verify the API key
        if User.verify(key):
            # will return processed arguments, if there is an incorrect
            # argument then it will return the first incorrect argument
            args = process_args(args)

            if isinstance(args, str):
                abort(
                    400,
                    status=400,
                    message=f"Invalid parameter: {args}")

            elif isinstance(args, dict):
                if typ == 'select':
                    # if select api, then use get method by passing in primary
                    # keys
                    result = Residence.query.get(args['name'])
                    if not result:
                        abort(
                            404,
                            status=404,
                            message=f"Residence with name \""
                            f"{args['name']}\" does not exist")
                    else:
                        response['status'] = 200
                        response['data'] = remove_hidden_attr(result.__dict__)

                elif typ == 'search':
                    self.set_expand_group(args)
                    # for search api, use filter through db
                    result = Residence.query
                    for key, val in args.items():
                        col = getattr(Residence, key)
                        if type(val) == str:
                            s = "%" + val + "%"
                            result = result.filter(col.like(s))
                        else:
                            result = result.filter(col == val)
                    result = result.all()
                    if not result:
                        abort(404, status=404,
                              message=f'No residence with {args}')

                    else:
                        print(result)
                        response['data'] = [
                            remove_hidden_attr(
                                i.__dict__) for i in result]
                return jsonify(response)
        # if API key was not verified
        else:
            abort(403, status=403,
                  message="User couldn't be verified")


# api/courses/search dynamically searches by whatever parameters they input
# api/courses/term/course_id passes a specific course
api.add_resource(Courses, '/courses/<typ>')
api.add_resource(Students, '/students/<typ>')
api.add_resource(Residences, '/residences/<typ>')


def add_all_to_parser(parser, terms):
    """
    Adds all search or select terms in terms to the parser
    """
    for term in terms:
        parser.add_argument(term)


def add_required_to_parser(parser, terms):
    """
    Adds a list of required terms to the parser
    """
    for term in terms:
        help_text = term + " can't be blank"
        parser.add_argument(term, required=True, help=help_text)


def process_args(args):
    """
    Cleans raw arguments from the request
    """
    final_args = {}
    del args['key']

    for k in args.keys():
        if args[k] is not None:
            if args[k].lower() == "false":
                final_args[k] = False
            elif args[k].lower() == "true":
                final_args[k] = True
            else:
                final_args[k] = args[k]
    return final_args
