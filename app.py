from flask import Flask, render_template
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

todos = {}

#validate form data inputs
parser = reqparse.RequestParser()
parser.add_argument('task')

def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))

class Housing(Resource):
    def get(self, dorm_id):
        return {dorm_id: todos[dorm_id]}

api.add_resource(Housing, '/Housing/<string:dorm_id>')

#endpoint would be /Housing/<DormName>
#info about dorm cost, address, info
#reviews about each dorm

class Dining(Resource):
    def get(self, dininghall_id):
        return {dorm_id: todos[dininghall_id]}

api.add_resource(Dining, '/Dining/<string:dininghall_id>/<string:day>')

#endpoint would be /Dining/<DiningHall>/<Date>
#info about menus

class Courses(Resource):
    def get(self, dept_id, course_id):
        return {course_id: todos[course_id]}

api.add_resource(Courses, '/Courses/<string:dept_id>/<string:course_id>')

#endpoint would be Courses/Dept/CourseID
#info about each course
#reviews about courses

class Students(Resource):
    def get(self, student_id):
        return {student_id: todos[student_id]}

api.add_resource(Student, '/Students/<string:student_id>')

#info about each student

if __name__ == '__main__':
    app.run()
