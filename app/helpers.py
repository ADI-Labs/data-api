import scrapy
import os
from scrapy.crawler import CrawlerProcess
import hashlib
import json
from . import db
from .models import Course
# --------------------------------------------------------

ITEM_PIPELINES = {'scrapy.pipelines.files.FilesPipeline': 1}
FILES_STORE = './data'
COURSES_URL = "http://opendataservice.columbia.edu/api/9/json/download"
config = json.load(open("./app/config.json"))


class JSON(scrapy.Item):
    title = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()


class CourseSpider(scrapy.Spider):
    name = 'coursespider'
    start_urls = ["https://cas.columbia.edu/cas/login?service=" +   
                  "ias-qmss&destination=http://opendataservice." +
                  "columbia.edu/user/wind"]

    custom_settings = {
        "ITEM_PIPELINES": {'scrapy.pipelines.files.FilesPipeline': 1},
        "FILES_STORE": FILES_STORE,
        "MEDIA_ALLOW_REDIRECTS": True,
        "REACTOR_THREADPOOL_MAXSIZE": 20
    }

    def parse(self, response):
        print("Existing settings: %s" % self.settings.attributes.keys()) 
        uni = str(config["login"]["uni"])
        password = str(config["login"]["password"])
        if uni is None or password is None:
            raise Exception('you must give a uni and password')
        return [scrapy.FormRequest.from_response
                (response,
                 formdata={'username': uni, 'password': password},
                 formxpath='//form[@id="fm1"]',
                 callback=self.after_login,
                 dont_filter=True)]

    def after_login(self, response):
        yield JSON(file_urls=[COURSES_URL])

def remove_hidden_attr(d):
    return {key: value for key, value in d.items() if key[0] != '_'}


def get_courses(date):
    # for some reason flask shell chooses python 2.7 by default
    # sha = hashlib.sha1()
    # sha.update(COURSES_URL.encode('utf-8'))
    # name = sha.hexdigest()
    name = 'test.json'

    filepath = os.path.join(FILES_STORE, "full", name)
    if os.path.isfile('app/data.sqlite') and os.path.isfile(filepath):
        print("course data is downloaded and DB has data")
        print("updating...\n")
    else:
        print("scraping and storing course data...\n")
        db.drop_all()
        db.create_all()

        crwl = CrawlerProcess(
            {'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})
        # Downloads data from courses
        crwl.crawl(CourseSpider)
        crwl.start()

    parse_and_store(filepath)

    # rename to keep old files     
    # os.rename(filepath,os.path.join(FILES_STORE, "full",f"courses-{date}.json"))

def parse_and_store(path):
    '''
    Needs to run within an app_context!

    :param path:
    :return:
    '''
    data = json.load(open(path))
    for datum in data:
        new_course = Course(course_id=datum["Course"],
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
        
        existing_course = Course.query.get((new_course.course_id, new_course.term))

        if existing_course:   
            print(new_course, datum["NumEnrolled"])
            print(existing_course, existing_course.num_enrolled) 
            # check for differences objects and then update 
            existing_course = check_differences(existing_course, new_course)
            # db.session.delete(existing_course) 
        else: 
            print('new course!')
            db.session.add(new_course)
        db.session.commit() 

        existing_course = Course.query.get((datum["Course"], datum["Term"]))
        print(existing_course, existing_course.num_enrolled)
    print("database created and up to date!")


def check_differences(existing_course, new_course):
    existing_data = remove_hidden_attr(existing_course.__dict__)
    new_data = remove_hidden_attr(new_course.__dict__)
    # print(existing_data)
    # print(new_data)
    for key in existing_data.keys():
        print(key)
        if existing_data[key] != new_data[key]:
            print('There is a difference!')
            print((getattr(existing_course, key)))
            setattr(existing_course, key, new_data[key])
            print((getattr(existing_course, key)))
    db.session.flush()
