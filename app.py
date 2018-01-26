
from flask import Flask, render_template, Response, redirect, url_for, request, session, abort
from flask_restful import Resource, Api
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user


app = Flask(__name__)
api = Api(app)

todos = {}

#validate form data inputs
parser = reqparse.RequestParser()
parser.add_argument('task')

# config
app.config.update(
    DEBUG = True,
    SECRET_KEY = 'secret_xxx'
)

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# silly user model
class User(UserMixin):

    def __init__(self, id):
        self.id = id
        self.email = "email" + str(id)
        self.password = self.email + "_secret"

    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.email, self.password)


# create some users with ids 1 to 20
users = [User(id) for id in range(1, 21)]


# some protected url
@app.route('/')
@login_required
def home():
    return Response("Hello World!")


# somewhere to login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if password == username + "_secret":
            id = username.split('user')[0]
            user = User(id)
            login_user(user)
            return redirect(request.args.get("next"))
        else:
            return abort(401)
    else:
        return Response('''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=password name=password>
            <p><input type=submit value=Login>
        </form>
        ''')
        #return redirect(url_for('index'))


# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return Response('<p>Logged out</p>')


# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')


# callback to reload the user object
@login_manager.user_loader
def load_user(userid):
    return User(userid)


@login_manager.request_loader
def load_user(request):
    token = request.headers.get('Authorization')
    if token is None:
        token = request.args.get('token')

    if token is not None:
        username,password = token.split(":") # naive token
        user_entry = User.get(username)
        if (user_entry is not None):
            user = User(user_entry[0],user_entry[1])
            if (user.password == password):
                return user
    return None

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

if __name__ == "__main__":
    app.run()
