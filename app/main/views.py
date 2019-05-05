from flask import render_template, request
from ..models import Course, Dining, Student, Residence
from . import main
import os
from flask_cors import cross_origin


def remove_hidden_attr(d):
    return {key: value for key, value in d.items() if key[0] != '_'}


def search(term, where):
    result = []

    # Very inefficient implementation
    # in the interest of "time" lol ironic

    # FIX: for students.html, alld is empty list
    # FIX: for courses.html, alld is empty list too!
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
                    break
                # more ifs based on models here
                if where == Student:
                    result.append({"name": things["Name"],
                                   "uni": things["UNI"]})
                    break
                if where == Residence:
                    result.append({"name": things["name"],
                                   "street_address": things["street_address"],
                                   "class_make_up": things["class_make_up"],
                                   "room_type": things["room_type"]})
                    break
                continue
    return result


def get_parameters(filename):
    parameters = []

    path = './app/static/metadata/' + str(filename)
    new_path = os.path.abspath(path)

    f = open(new_path, "r")

    lines = f.readlines()
    for line in lines:
        line_data = line.split(", ")
        parameters.append({"name": line_data[0],
                           "type": line_data[1],
                           "description": line_data[2]})

    return parameters


@main.route('/')
def base():
    return render_template('main/home.html')


# having searching happen through the URL
# soon
@main.route('/courses', methods=['GET', 'POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def courses():
    search_results = []
    if request.form:
        term = request.form["searchTerm"]
        # print(term)
        search_results = search(term, Course)
    # print(search_results)

    return render_template(
        'main/courses.html',
        results=search_results,
        parameters=get_parameters('courses.txt'))


# not implementable yet. Model hasn't been built
@main.route('/residences', methods=['GET', 'POST'])
def residences():
    search_results = []
    if request.form:
        term = request.form["searchTerm"]
        # print(term)  # term = search query
        search_results = search(term, Residence)
    # print(search_results)

    return render_template(
        'main/residences.html',
        results=search_results,
        parameters=get_parameters('residences.txt'))


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
        # print(term)  # term = search query
        search_results = search(term, Student)
    # print(search_results)

    return render_template(
        'main/students.html',
        results=search_results,
        parameters=get_parameters('students.txt'))


@main.route('/auth')
def auth():
    return render_template('main/authentication.html')


@main.route('/docs')
def docs():
    return render_template('main/students.html')


@main.route('/home')
def home():
    return render_template('main/home.html')
