import os
from datetime import datetime
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
#from settings import DB_NAME, DB_USER, DB_PASSWORD


database_path = 'postgresql://postgres:Kepman123@localhost:5432/attendance_db'
#"postgresql://{}:{}@{}/{}".format(DB_USER, DB_PASSWORD, "localhost:5432", DB_NAME)
db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

# Student table
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    college = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    level = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    #courses = db.relationship('Course', backref='student', lazy=True)


    def __init__(self, name, email, college, department, level, password):
        self.name = name
        self.email = email
        self.college = college
        self.department = department
        self.level = level
        self.password = password
        
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<Student %r>' % self.name

# Lecturer table
class Lecturer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    courses = db.relationship('Course', backref='lecturer', lazy=True)
    attendance = db.relationship('Attendance', backref='lecturer', lazy=True)



    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def insert_l(self):
        db.session.add(self)
        db.session.commit()

    def update_l(self):
        db.session.commit()

    def delete_l(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<Lecturer %r>' % self.name


# Course table
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    code = db.Column(db.String(50), nullable=False, unique=True)
    lecturer_id = db.Column(db.Integer(), db.ForeignKey('lecturer.id'),  nullable=False)
    student_id = db.Column(db.ARRAY(db.Integer), nullable=False)
    attendance = db.relationship('Attendance', backref='course', lazy=True)
    mark_attendance = db.relationship('MarkAttendance', backref='course', lazy=True)


    def __init__(self, name, code, lecturer_id, student_id):
        self.name = name
        self.code = code
        self.lecturer_id = lecturer_id
        self.student_id = student_id

    def insert_c(self):
        db.session.add(self)
        db.session.commit()

    def update_c(self):
        db.session.commit()

    def delete_c(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<Course %r>' % self.name

# Attendance table
class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    time = db.Column(db.Time, nullable=False, default=datetime.utcnow().strftime('%H:%M:%S'))
    timeframe = db.Column(db.String(50), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    lecturer_id = db.Column(db.Integer, db.ForeignKey('lecturer.id'), nullable=False)


    def __init__(self, date, time, timeframe, course_id, lecturer_id):
        self.date = date
        self.time = time
        self.timeframe = timeframe
        self.course_id = course_id
        self.lecturer_id = lecturer_id

    def insert_at(self):
        db.session.add(self)
        db.session.commit()


    def __repr__(self):
        return '<Attendance %r>' % self.id

# Mark Attendance table
class MarkAttendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)


    def __init__(self, date, course_id, student_id):
        self.date = date
        self.course_id = course_id
        self.student_id = student_id

    def insert_mk(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<MarkAttendance %r>' % self.id



class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)

    
    def __init__(self, username, password, full_name):
        self.username = username
        self.password = password
        self.full_name = full_name

    def insert_ad(self):
        db.session.add(self)
        db.session.commit()

    def update_ad(self):
        db.session.commit()

    def delete_ad(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<Admin %r>' % self.full_name