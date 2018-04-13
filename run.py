from app import create_app, db, mail
from app.models import Course, Dining, Student, User
import json
import os
import hashlib
import getpass
#import scrapy

app = create_app()

#ITEM_PIPELINES = {'scrapy.pipelinvimes.files.FilesPipeline': 1}

FILES_STORE = './data/'
uni = ""
pwd = ""
URL = "http://opendataservice.columbia.edu/api/9/json/download"


@app.shell_context_processor
def make_shell_context():
    return dict(app=app,
                db=db,
                User=User,
                mail=mail,
                Student=Student,
                Course=Course,
                Dining=Dining,
                clear=clear,
                sqlIt=parse_and_store,
                GetJson=GetJson,
                get_courses=get_courses
                )


@app.cli.command()
def test():
    """Run unit tests from command line"""
    from unittest import TestLoader, TextTestRunner
    suite = TestLoader().discover('tests')
    TextTestRunner(verbosity=2, buffer=False).run(suite)


def parse_and_store(path):
    db.drop_all()
    db.create_all()

    print(path)
    data = json.load(open(path))
    for datum in data:
        course = Course(course_id=datum["Course"],
                        call_number=datum["CallNumber"],
                        course_name=datum["CourseTitle"],
                        bulletin_flags=datum["BulletinFlags"],
                        division_code=datum["DivisionCode"],
                        class_notes=datum["ClassNotes"],
                        num_enrolled=datum["NumEnrolled"],
                        max_size=datum["MaxSize"],
                        min_units=datum["MinUnits"],
                        num_fixed_units=datum["NumFixedUnits"],
                        term=datum["Term"],
                        campus_name=datum["CampusName"],
                        campus_code=datum["CampusCode"],
                        school_code=datum["SchoolCode"],
                        school_name=datum["SchoolName"],
                        approval=datum["Approval"],
                        prefix_name=datum["PrefixName"],
                        prefix_long_name=datum["PrefixLongname"],
                        instructor_name=datum["Instructor1Name"],
                        type_name=datum["TypeName"],
                        type_code=datum["TypeCode"]
                        )

        db.session.add(course)
        db.session.commit()


def clear():
    os.system('clear')


def get_courses():
    # for some reason flask shell chooses python 2.7 by default
    uni = raw_input("Your UNI: ")
    pwd = getpass.getpass("Your PWD: ")
    #crwl = CrawlerProcess(
    #    {'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})
    #crwl.crawl(GetJson)
    #crwl.start()
    sha = hashlib.sha1()
    sha.update(URL)
    name = sha.hexdigest()
    parse_and_store(FILES_STORE+"full/"+name)

'''
class JSON(scrapy.Item):
    title = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
'''

'''
class GetJson(scrapy.Spider):
    name = 'getjson'
    start_urls = ["https://cas.columbia.edu/cas/login?service=" +
                  "ias-qmss&destination=http://opendataservice." +
                  "columbia.edu/user/wind"]

    custom_settings = {
        "ITEM_PIPELINES": {'scrapy.pipelines.files.FilesPipeline': 1},
        "FILES_STORE": FILES_STORE
    }

    def parse(self, response):
        print(uni)
        print(pwd)
        return [scrapy.FormRequest.from_response
                (response,
                 formdata={'username': uni, 'password': pwd},
                 formxpath='//form[@id="fm1"]',
                 callback=self.after_login,
                 dont_filter=True)]

    def after_login(self, response):
        yield JSON(file_urls=[URL])
'''
