from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

student_lessons = db.Table('student_lessons',
    db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
    db.Column('lesson_id', db.Integer, db.ForeignKey('lesson.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin, teacher, student

    student = db.relationship("Student", back_populates="user", uselist=False)
    teacher = db.relationship("Teacher", back_populates="user", uselist=False)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    grade_level = db.Column(db.String(20))
    user = db.relationship("User", back_populates="student")
    lessons = db.relationship("Lesson", secondary=student_lessons, back_populates="students")

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    department = db.Column(db.String(100))
    user = db.relationship("User", back_populates="teacher")
    lessons = db.relationship("Lesson", back_populates="teacher")

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    teacher = db.relationship("Teacher", back_populates="lessons")
    students = db.relationship("Student", secondary=student_lessons, back_populates="lessons")

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'))
    value = db.Column(db.Float, nullable=False)

class Diary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow)
    student = db.relationship('Student', backref=db.backref('diaries', lazy=True))
