from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import mapper, sessionmaker
import os

storedir = './'

#----------------------------------------------------------------------
def loadSession():
    """"""    
    database_uri = "sqlite:///" + os.path.join(storedir, 'data.sqlite')

    engine = create_engine(database_uri, echo=True)
 
    metadata = MetaData(engine)
    courses = Table('courses', metadata, autoload=True)
    mapper(Bookmarks, courses)
 
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

class Course():
    __tablename__ = 'courses'
    term = db.Column(db.String(64), primary_key=True)
    course_id = db.Column(db.String(64), primary_key=True, nullable=False)
    prefix_name = db.Column(db.String(64))
    prefix_long_name = db.Column(db.String(64))
    division_code = db.Column(db.String(4))
    division_name = db.Column(db.String(64))
    campus_code = db.Column(db.String(4))
    campus_name = db.Column(db.String(128))
    school_code = db.Column(db.String(4))
    school_name = db.Column(db.String(128))
    department_code = db.Column(db.String(256))
    department_name = db.Column(db.String(256))
    subterm_code = db.Column(db.String(4))
    subterm_name = db.Column(db.String(4))
    call_number = db.Column(db.String(120))
    num_enrolled = db.Column(db.String(120))
    max_size = db.Column(db.String(4))
    enrollment_status = db.Column(db.String(4))
    num_fixed_units = db.Column(db.String(120))
    min_units = db.Column(db.String(120))
    max_units = db.Column(db.String(120))
    course_name = db.Column(db.String(120))
    type_code = db.Column(db.String(4))
    type_name = db.Column(db.String(64))
    approval = db.Column(db.String(64))
    bulletin_flags = db.Column(db.String(10))
    class_notes = db.Column(db.String(256))
    meeting_times = db.Column(db.String(256))
    instructor_name = db.Column(db.String(64))

    profs = db.relationship('Teacher', secondary=profs,
                            backref=db.backref('courses'))

    def __repr__(self):
        return f'<Course {self.course_id} {self.course_name} {self.term}>'
if __name__ == "__main__":
    session = loadSession()
    res = session.query(Course).all()
    res[1].title