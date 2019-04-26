# Data@CU

About DATA@CU: Data@CU is a project that aims to provide an API for all Columbia-related data and become the go-to source of data exclusively for student developers at Columbia through a RESTful API. It has been in development since Spring of 2018.

In addition to providing an API for available data, DATA@CU aims to perform data analytics where fit and provide that as part of the API as well.

## Technology:

Data@CU’s stack is currently as follows:

1. Python 3
        - Python dependencies are managed via Pipenv. Students will be encouraged to use the more modern aspects of the                 language, and will be expected to write clean, efficient code.
2. Flask
        - Flask is powerful micro web-framework that makes it easy to get a server-based Python app up and running quickly.
3. SQLite/pysqlite/SQLAlchemy
        - Data is saved and retreived using a SQL(SQLite dialect) database. To interact with the database, we will use                      SQLAlchemy, a     Python library that makes it easy for programmers to interact with SQL databases.
4. HTML/CSS/JavaScript with Jinja template engine
        - Data@CU’s information is presented via a website - [data2.adicu.com](data2.adicu.com).
5. TravisCI
        - Project continuous integration managed in collaboration with Github and Slack.
  
## Deployment:

Deployment to data2.adicu.com is an automatic process that occurs on every successful merge into the repository
The website is deployed as an extension to the ADI CU website.

## API endpoints:

All the APIs have two endpoints - Select and Search

Select returns one specific result
Search returns a list of relevant results

### Courses

##### SELECT

Requires course id, term, and key - returns a single result
/api/courses/select?course_id=<course_id>&term=<term>&key=<key> 

##### SEARCH

Accepts any combination of one or more parameters, requires key - returns a list
/api/courses/search?course_name=<course_name>&key=<key> 
        
##### PARAMETERS

['course_id', 'term', 'course_name', 'call_number', 'bulletin_flags', 'division_code', 'credit_amount', 'prefix_name', 'prefix_long_name', 'instructor_name', 'approval', 'school_code', 'school_name', 'campus_code', 'campus_name', 'type_code', 'type_name', 'num_enrolled', 'max_size', 'min_units', 'num_fixed_units', 'class_notes', 'meeting_times']


### Residences

##### SELECT

Requires name, and key - returns a single result
/api/courses/select?name=<name>&key=<key> 

##### SEARCH

Accepts any combination of one or more parameters, requires key - returns a list
/api/courses/search?name=<name>&key=<key> 
        
        Special residences: 
	        For each type (FSL and residential brownstones, SIC housing), a grouped entry and split entries both exist.                   Specify a “expand_special” option in the search api: if false, only returns grouped, if true, returns all                     relevant entries as usual

##### PARAMETERS
* - searchable

*name
street_address
*residential_area
*building_type
*room_type
*class_make_up
rate
entrance_info
num_res_floors
num_singles
num_doubles
*bathroom
laundry
flooring
*kitchen
lounge
cleaning_schedule
*bike_storage
*print_station
*fitness_room
*computer_lab
*ac
*piano
description
features

### Students

SELECT

SEARCH

### Notes

When querying, must replace each space with “%20”

## Contributors

### Current Contributors:
- Anavi Lohia (Product Manager)
- Colin Brown (Developer)
- Sharon Jin (Developer)

### Past Contributors: 
- Amanda Zong
- Kathy Lau
- James Xu
- Yishak Tofik Mohammed (Developer & Product Manager)
- Jonathan Zhang (TA)
- Kevin Mao (Developer)
- Anavi Lohia (Developer)
- Bruk Zewdie (Developer)
- Marcus Blake (Developer)
