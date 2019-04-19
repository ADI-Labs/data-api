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
4. HTML/CSS/JavaScript
        - Data@CU’s information is presented via a website - [data2.adicu.com](data2.adicu.com)
5. TravisCI
        - Project continuous integration managed in collaboration with Github and Slack.
  
## Deployment:
git remote add dokku dokku@208.68.37.106:data-api
git push dokku master

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
