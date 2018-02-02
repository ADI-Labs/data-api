from flask import request, url_for, render_template
from . import main


@main.route('/')
def base():
    return render_template('base.html')
# def mains():
#     url = request.url_rule
#     courses='not'
#     housing='not'
#     dining='not'
#     auth='not'
#     docs = 'not'
#
#     if('courses' in url.rule):
#         courses = "active"
#     elif('housing' in url.rule):
#         housing= "active"
#     elif('dining' in url.rule):
#         dining= "active"
#     elif('auth' in url.rule):
#         auth="active"
#     elif('docs' in url.rule):
#         docs="active"
#     state={'a':'a', 'b':'b', 'c':'d'}
#     return render_template("main/index.html", state=state)

@main.route('/courses')
def courses():
    return render_template('main/courses.html')

@main.route('/housing')
def housing():
    return render_template('main/housing.html')

@main.route('/dining')
def dining():
    return render_template('main/dining.html')

@main.route('/auth')
def auth():
    return render_template('main/authentication.html')

@main.route('/docs')
def docs():
    return render_template('main/docs.html')
