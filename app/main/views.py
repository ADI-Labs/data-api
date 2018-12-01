from flask import render_template, request
from ..models import Course, Dining, Student
from . import main


def remove_hidden_attr(d):
    return {key: value for key, value in d.items() if key[0] != '_'}


def search(term, where):
    result = []

    # Very inefficient implementation
    # in the interest of "time" lol ironic

    alld = where.query.all()
    for one in alld:
        things = remove_hidden_attr(one.__dict__)
        for attr in things:
            s_able = str(things[attr]).lower()
            if s_able.find(term) != -1:
                # from here, ifs become essential since
                # returnables are very dependent on
                # model type

                if where == Course:
                    result.append({"course_id": things["course_id"],
                                   "term": things["term"],
                                   "name": things["course_name"]})
                # more ifs based on models here
                continue

    return result


@main.route('/')
def base():
    return render_template('main/home.html')


# having searching happen through the URL
# soon
@main.route('/courses', methods=['GET', 'POST'])
def courses():
    search_results = []
    if request.form:
        term = request.form["searchTerm"]
        print(term)
        search_results = search(term, Course)

    print(search_results)
    return render_template('main/courses.html', results=search_results)


# not implementable yet. Model hasn't been built
@main.route('/housing', methods=['GET', 'POST'])
def housing():
    search_results = []
    if request.form:
        term = request.form["searchTerm"]
        search_results = search(term, "Housing")

    return render_template('main/housing.html', results=search_results)


@main.route('/dining', methods=['GET', 'POST'])
def dining():
    search_results = []

    if request.form:
        term = request.form["searchTerm"]
        search_results = search(term, Dining)

    return render_template('main/dining.html', results=search_results)


@main.route('/students', methods=['GET', 'POST'])
def student():
    search_results = []

    if request.form:
        term = request.form["searchTerm"]
        search_results = search(term, Student)

    return render_template('main/students.html', results=search_results)


@main.route('/auth')
def auth():
    return render_template('main/authentication.html')


@main.route('/docs')
def docs():
    return render_template('main/students.html')


@main.route('/home')
def home():
    return render_template('main/home.html')
