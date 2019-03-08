#!/usr/bin/env python
import json
import time
import os
import sys
from robobrowser import RoboBrowser
from . import db
from .models import Student
from .helpers import check_differences

# URLs that are used to scrape.
login_url = 'https://cas.columbia.edu/cas/login?TARGET=' + \
    'https%3A%2F%2Fdirectory.columbia.edu%2Fpeople%2F' + \
    'browse%2Fstudents%3Ffilter.lnameFname%3D2%26filter.initialLetter%3DA'
url_base = 'https://directory.columbia.edu'
browse_url = url_base + '/people/browse/students'

direct_url = "https://directory-dev.cc.columbia.edu/people/browse/students" + \
    "?filter.lnameFname=1&filter.initialLetter=A"
people_url = "https://directory.columbia.edu/people/"

headers = {
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) " +
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/" +
    "webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9"
}

# get login information from config file in root directory
file = open('./app/config.json')
config = json.load(file)
file.close()


LOGIN = config['login']
uni = LOGIN['uni']
password = LOGIN['password']

FILEPATH = '../data/student_data.json'
TWO_WEEKS = 60

# 1209600 seconds in 2 weeks
'''
    This is the driver function which scrapes the Columbia directory
    for student data
    Parameters:
        None
'''


def get_students():
    """
    CURRENTLY BROKEN - to fix once CUIT fixes their internal server errors
    """
    global FILEPATH
    browser = RoboBrowser()

    browser.open(people_url, headers=headers)
    printPage(browser, "Main directory")
    login(browser)

    pages = browser.find(class_='name_form_az').find_all('a')

    # This gets the links to each intial web page (i.e page 0)
    # that contains a query for an alphabetical character
    web_pages = []
    web_pages.append(login_url)
    for page in pages:
        if page.has_attr('href'):
            web_pages.append(page['href'])

    query = getCurrPage(web_pages)
    isStart = (query == web_pages[0])
    if os.path.isfile(FILEPATH):
        current_time = time.time()
        last_modified = os.path.getmtime(FILEPATH)
        elapsed = current_time - last_modified
        if elapsed < TWO_WEEKS and isStart:
            sys.exit()
        if elapsed >= TWO_WEEKS:
            FILEPATH = '../data/temp.json'
    if isStart:
        url = query
    else:
        url = browse_url + query
    writeNextPage(query, web_pages)
    browser.open(url)
    print('Getting data from ', url)

    if not os.path.isfile('app/data.sqlite'):
        db.create_all()
    getAndWriteData(browser)

    if url == web_pages[len(web_pages) - 1] \
            and FILEPATH == '../data/temp.json' \
            and os.path.isfile('../data/student_data.json'):
        newName = '../data/student_data.json'
        os.remove(newName)
        os.rename(FILEPATH, newName)


'''
    This function logs into the Columbia directory using the credentials file
    in project root directory

    Parameters:
        browser - RoboBrowser object

'''


def login(browser):
    # open login page
    browser.open(login_url, headers=headers)
    printPage(browser, "Before Login")
    submitLoginForm(browser)
    printPage(browser, "after login")


def submitLoginForm(browser):
    login = browser.get_form()

    # use credentials from file
    login['username'] = uni
    login['password'] = password
    browser.submit_form(login, headers=headers)


'''

    This function replaces breaks found in HTML text
    with a specified delimeter

    Parameters:

        item - BeautifulSoup object which contains HTML text
        delimiter - String to replace br

'''


def replaceBreaks(item, delimiter):
    for br in item.find_all('br'):
        br.replace_with(delimiter)
    return item


'''
    This gets all of the student information found on a particular
    web page

    Parameters:

        rows - Array of BeautifulSoup objects which represents table rows
        students - Array of dictionaries which represent students and their
            information
'''


def parseInfo(rows, file):

    student = {
        'Name': '',
        'UNI': '',
        'Email': '',
        'Department': '',
        'Title': '',
        'Address': '',
        'Home Addr': '',
        'Campus Tel': '',
        'Tel': '',
        'FAX': ''
    }

    for row in rows:
        if student['Name'] == '' or student['Name'] is None:
            name = row.find('th')
            student['Name'] = name.text

        else:

            items = row.find_all('td')
            field = None

            # Every other td is a data field
            count = 0

            for item in items:

                txt = item.text
                if txt != '\u00a0' and txt != '' and txt is not None:

                    if count == 0 and ':' in txt:
                        txt = txt.replace(':', '')
                        count += 1
                        if student[txt] == '':
                            field = txt
                        else:
                            continue

                    elif count == 1:

                        if field == 'Email':
                            addr = item.find_all('a')[0]
                            txt = addr.text
                        elif field == 'Address':
                            txt = replaceBreaks(item, ' ').text
                        elif field == 'Campus Tel':
                            temp = ''
                            for index in range(len(txt)):
                                if txt[index] == '\xa0':
                                    break
                                temp += txt[index]

                            txt = temp
                        elif field is None:
                            continue

                        student[field] = txt
                        count -= 1

    append_to_json(student, file)
    upload_to_db(student)


"""
"""


def getAndWriteData(browser):
    if printPage(browser, "Before getting data") == "Login":
        submitLoginForm(browser)
        printPage(browser, "Extra login")

    pages = browser.find(class_='page_number_result').find_all('a')
    last_page = pages[len(pages) - 1]['href']
    last_page = last_page.split('=')

    num_pages = int(last_page[len(last_page) - 1])
    query_format = '?page='

    # open data json file
    file = open(FILEPATH, 'ab+')

    for pageNumber in range(0, num_pages + 1):
        url = browse_url + query_format + str(pageNumber)
        browser.open(url)
        table = browser.find(class_='table_results')
        people = table.find_all('tr')
        links = []
        for integer in range(1, len(people)):
            link = people[integer].find_all('a')
            if len(link) > 0:
                links.append(url_base + link[0]['href'])

        while len(links) != 0:
            link = links.pop(0)
            browser.open(link)
            rows = browser.find(class_='table_results_indiv').find_all('tr')
            parseInfo(rows, file)

    file.close()


'''
'''


def append_to_json(dict, file):

    # Checks to see if file has already be written to. If so, append json data
    file.seek(0, 2)
    if file.tell() == 0:
        file.write(json.dumps([dict], indent=4).encode())

    else:
        file.seek(-1, 2)
        file.truncate()
        file.write(' , '.encode())
        file.write(json.dumps(dict, indent=4).encode())
        file.write(']'.encode())


"""
"""


def upload_to_db(student):
    new_student = Student(
        name=student['Name'],
        uni=student['UNI'],
        email=student['Email'],
        department=student['Department'],
        title=student['Title'],
        address=student['Address'],
        home_addr=student['Home Addr'],
        campus_tel=student['Campus Tel'],
        tel=student['Tel'],
        fax=student['FAX']
    )
    existing_student = Student.query.get(new_student.uni)
    if existing_student:
        # check for differences objects and then update
        existing_student = check_differences(existing_student, new_student)
    else:
        db.session.add(new_student)

    db.session.commit()


def upload_to_db_from_file(filepath):
    students = json.load(open(filepath))
    for student in students:
        new_student = Student(
            name=student['Name'],
            uni=student['UNI'],
            email=student['Email'],
            department=student['Department'],
            title=student['Title'],
            address=student['Address'],
            home_addr=student['Home Addr'],
            campus_tel=student['Campus Tel'],
            tel=student['Tel'],
            fax=student['FAX']
        )
        existing_student = Student.query.get(new_student.uni)
        if existing_student:
            # check for differences objects and then update
            existing_student = check_differences(existing_student, new_student)
        else:
            db.session.add(new_student)

    db.session.commit()


def writeNextPage(query, web_pages):
    newPage = 0
    for index in range(0, len(web_pages)):
        if web_pages[index] == query and index + 1 < len(web_pages):
            newPage = index + 1
            break

    with open('utils/current_page.txt', 'w') as f:
        f.write(web_pages[newPage])


"""
"""


def getCurrPage(web_pages):
    if not os.path.isfile('utils/current_page.txt'):
        return web_pages[0]

    else:
        with open('utils/current_page.txt', 'r') as f:
            url = f.read()

    return url


def printPage(browser, title):
    print("")
    print("Browser Page: " + title)
    print(browser.url)
    text = str(browser.parsed)
    req_type = ""
    if text.find("Central Authentication Service") > 0:
        req_type = "Login"
    elif text.find("The Directory Service is temporarily unavailable") > 0:
        req_type = "Unavailable"
    elif text.find("Internal Server Error") > 0:
        req_type = "Server Error"
    elif text.find("Find People and Departments") > 0:
        req_type = "Directory Home"
    else:
        req_type = "Other"
        writePage(browser, title+".txt")
    print("Type: " + req_type)
    print("\nRequest headers")
    print(browser.response.request.headers)
    for cookie in browser.response.request._cookies:
        print(cookie.name, cookie.value)
    print("\nResponse headers")
    print(browser.response.headers)
    print("\nCookies")
    for cookie in browser.session.cookies:
        print(cookie.name, cookie.value)
    print("\n-----")
    return req_type


def writePage(browser, title):
    with open("browser_pages/"+title, "w") as f:
        f.write(str(browser.parsed))