from flask_login import UserMixin
from . import login_manager, db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash


@login_manager.user_loader
def load_user(userid):
    try:
        return User.query.get(int(userid))
    except Exception:
        return None


@login_manager.request_loader
def load_user_from_request(request):
    token = request.headers.get('Authorization')
    if token is None:
        token = request.args.get('token')

    if token is not None:
        username, password = token.split(":")  # naive token
        user_entry = User.get(username)
        if user_entry is not None:
            user = User(user_entry[0], user_entry[1])
            if user.password == password:
                return user
    return None


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uni = db.Column(db.String(120), unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), unique=False, nullable=False)
    school = db.Column(db.String(120), unique=False, nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer('xxx', expiration)
        token = s.dumps({'id': self.id})
        return token

    @staticmethod
    def verify(token):
        s = Serializer('xxx')
        try:
            data = s.loads(token)
        except Exception:
            return None
        return User.query.get(data['id'])

    def confirm(self, token):
        s = Serializer('xxx')
        try:
            data = s.loads(token)
        except Exception:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def __repr__(self):
        return f'<User {self.uni} {self.email}>'


profs = db.Table('profs',
                 db.Column('course_id', db.String,
                           db.ForeignKey('courses.course_id'),
                           primary_key=True),
                 db.Column('uni', db.String,
                           db.ForeignKey('teachers.uni'),
                           primary_key=True))


# this can include a search function
class Course(db.Model):
    __tablename__ = 'courses'
    course_name = db.Column(db.String(120))
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


class Student(db.Model):
    __tablename__ = 'students'
    name = db.Column(db.String(64), nullable=False)
    uni = db.Column(db.String(8), unique=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    department = db.Column(db.String(128), nullable=True)
    title = db.Column(db.String(128), nullable=True)
    address = db.Column(db.String(512), nullable=False)
    home_addr = db.Column(db.String(64), nullable=True)
    campus_tel = db.Column(db.String(32), nullable=True)
    tel = db.Column(db.String(32), nullable=True)
    fax = db.Column(db.String(32), nullable=True)

    def __repr__(self):
        return f'<Student {self.uni}>'


class Residence(db.Model):
    __tablename__ = 'residences'
    _expand_category = db.Column(db.String(16), nullable=True)
    name = db.Column(db.String(64), nullable=True, primary_key=True)
    street_address = db.Column(db.String(128), nullable=True)
    residential_area = db.Column(db.String(32), nullable=True)
    building_type = db.Column(db.String(32), nullable=True)
    room_type = db.Column(db.String(64), nullable=True)
    class_make_up = db.Column(db.String(64), nullable=True)
    rate = db.Column(db.String(64), nullable=True)
    entrance_info = db.Column(db.String(256), nullable=True)
    num_res_floors = db.Column(db.Integer, nullable=True)
    num_singles = db.Column(db.Integer, nullable=True)
    num_doubles = db.Column(db.Integer, nullable=True)
    bathroom = db.Column(db.String(128), nullable=True)
    laundry = db.Column(db.String(128), nullable=True)
    flooring = db.Column(db.String(128), nullable=True)
    kitchen = db.Column(db.String(128), nullable=True)
    lounge = db.Column(db.String(128), nullable=True)
    cleaning_schedule = db.Column(db.String(256), nullable=True)
    bike_storage = db.Column(db.Boolean, nullable=True)
    print_station = db.Column(db.Boolean, nullable=True)
    fitness_room = db.Column(db.Boolean, nullable=True)
    computer_lab = db.Column(db.Boolean, nullable=True)
    ac = db.Column(db.Boolean, nullable=True)
    piano = db.Column(db.Boolean, nullable=True)
    description = db.Column(db.Text, nullable=True)
    features = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Residence {self.name}>'


"""
    Currently unused models
"""


class Teacher(db.Model):
    __tablename__ = 'teachers'
    name = db.Column(db.String(100))
    uni = db.Column(db.String(7), primary_key=True)

    def __repr__(self):
        return f'<Teacher {self.name}>'


class Dining(db.Model):
    __tablename__ = 'dining'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    def __repr__(self):
        return f'<Dining {self.name}>'


# Methods

def get_column_names(model):
    """
    Returns a list of the column names for the specified model
    """
    return [i.name for i in list(model.__table__.columns)]


def get_primary_keys(model, obj):
    """
    Returns an ordered list of the primary keys for the given object
    """
    key_names = [pk.name for pk in model.__table__.primary_key]
    keys = list(map(lambda key: getattr(obj, key), key_names))
    return keys


def get_primary_key_names(model):
    """
    Returns an ordered list of the names of the primary keys
    """
    return [pk.name for pk in model.__table__.primary_key]
