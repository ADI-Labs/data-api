#!/usr/bin/env python
import scrapy
import os
import re
from scrapy.crawler import CrawlerProcess
import json
from .models import Course
import hashlib
import datetime
from .helpers import upload_object_to_db

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
    start_urls = ["https://cas.columbia.edu/cas/login?service="
                  "ias-qmss&destination=http://opendataservice."
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


# if you want to test this function, create a test.json
# pass in parse_and_store directly, without scraping
def get_courses():
    sha = hashlib.sha1()
    sha.update(COURSES_URL.encode('utf-8'))
    savename = str(datetime.date.today())
    name = sha.hexdigest()
    # name = 'test.json'

    filepath = os.path.join(FILES_STORE, "full", name)
    savepath = os.path.join(FILES_STORE, "full", f"{savename}.json")

    crwl = CrawlerProcess(
        {'USER_AGENT': 'Mozilla/4.0'
            ' (compatible; MSIE 7.0; Windows NT 5.1)'})

    # Downloads data from courses and downloads to filepath
    crwl.crawl(CourseSpider)
    crwl.start()

    # rename to keep old files
    # comment this line if testing with test.json
    os.rename(filepath, savepath)

    print("updating courses...")
    upload_to_db_from_file(savepath)


def upload_to_db_from_file(filepath):
    """
    Uploads all json course objects at filepath to the database
    """
    courses = json.load(open(filepath))
    for course in courses:
        # map dictionary keys to column names
        course = {snake_case(k): v for k, v in course.items()}
        change_key(course, "course", "course_id")
        change_key(course, "prefix_longname", "prefix_long_name")
        change_key(course, "course_title", "course_name")
        change_key(course, "meets1", "meeting_times")
        change_key(course, "instructor1_name", "instructor_name")

        upload_object_to_db(Course, course)
    print("database up to date")


def change_key(dic, old_key, new_key):
    """
    Moves the value of the old key to the new key in a dictionary
    """
    dic[new_key] = dic[old_key]
    del dic[old_key]


def snake_case(string):
    """
    Converts CamelCase string to snake_case string
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
