from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime
from models import Course, Teacher, Student
from flask import Blueprint

main = Blueprint('main', __name__)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# MODELOS

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin, teacher, student

    student = db.relationship('Student', backref='user', uselist=False)
    teacher = db.relationship('Teacher', backref='user', uselist=False)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    grade_level = db.Column(db.String(20))

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    department = db.Column(db.String(100))

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))

class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    value = db.Column(db.Float, nullable=False)

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'))
    value = db.Column(db.Float, nullable=False)

class Diary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, nullable=False)
    category = db.Column(db.String(50))

# DECORADOR

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Lütfen önce giriş yapınız.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# RUTAS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['user_role'] = user.role
            flash(f"Hoşgeldiniz, {user.name}!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash('Geçersiz e-posta veya şifre.', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash("Başarıyla çıkış yaptınız.", "success")
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        role = request.form['role'].lower()

        if password != confirm_password:
            flash("Şifreler eşleşmiyor.", 'danger')
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash("Bu e-posta zaten kayıtlı.", "danger")
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        new_user = User(name=name, email=email, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()

        if role == 'student':
            new_student = Student(user_id=new_user.id, grade_level="Orta")
            db.session.add(new_student)
        elif role == 'teacher':
            new_teacher = Teacher(user_id=new_user.id, department="Genel")
            db.session.add(new_teacher)

        db.session.commit()
        flash(f'{role.capitalize()} olarak başarıyla kayıt oldunuz.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    user = User.query.get(session['user_id'])

    if user.role == 'admin':
        total_students = Student.query.count()
        total_teachers = Teacher.query.count()
        total_lessons = Lesson.query.count()
        total_notes = Note.query.count()
        return render_template('dashboard.html', user=user, role='admin',
                               total_students=total_students, total_teachers=total_teachers,
                               total_lessons=total_lessons, total_notes=total_notes)

    elif user.role == 'teacher':
        teacher = Teacher.query.filter_by(user_id=user.id).first()
        lessons = Lesson.query.filter_by(teacher_id=teacher.id).all()
        graded_students = Note.query.filter(Note.lesson_id.in_([l.id for l in lessons])).distinct(Note.student_id).count()
        return render_template('dashboard.html', user=user, role='teacher',
                               teacher_lessons=lessons, graded_students_count=graded_students)

    elif user.role == 'student':
        student = Student.query.filter_by(user_id=user.id).first()
        diaries = Diary.query.filter_by(student_id=student.id).all()
        total = len(diaries)
        this_month = sum(1 for d in diaries if d.date.month == datetime.now().month)
        last_date = max((d.date for d in diaries), default=None)
        avg = round(total / ((datetime.now() - min((d.date for d in diaries), default=datetime.now())).days + 1), 2) if diaries else 0
        return render_template('dashboard.html', user=user, role='student',
                               diaries=diaries, total_diaries=total,
                               diaries_this_month=this_month,
                               last_diary_date=last_date.strftime("%d/%m/%Y") if last_date else "Yok",
                               diary_avg_per_day=avg)

    else:
        flash("Yetkisiz erişim.", "danger")
        return redirect(url_for('login'))
    
@app.route('/students')
@login_required
def students_page():
    if session.get('user_role') not in ['admin', 'teacher']:
        flash("Yetkisiz erişim.", "danger")
        return redirect(url_for('dashboard'))
    students = Student.query.all()
    return render_template('students.html', students=students)


@app.route('/teachers')
@login_required
def teachers_page():
    if session.get('user_role') != 'admin':
        flash("Yetkisiz erişim.", "danger")
        return redirect(url_for('dashboard'))
    teachers = Teacher.query.all()
    return render_template('teachers.html', teachers=teachers)


@app.route('/lessons')
@login_required
def lessons_page():
    lessons = Lesson.query.all()
    return render_template('lessons.html', lessons=lessons)


@app.route('/notes')
@login_required
def notes_page():
    if session.get('user_role') not in ['admin', 'teacher']:
        flash("Yetkisiz erişim.", "danger")
        return redirect(url_for('dashboard'))
    notes = Note.query.all()
    return render_template('notes.html', notes=notes)


@app.route('/diaries')
@login_required
def diaries_page():
    if session.get('user_role') != 'student':
        flash("Yetkisiz erişim.", "danger")
        return redirect(url_for('dashboard'))
    student = Student.query.filter_by(user_id=session['user_id']).first()
    diaries = Diary.query.filter_by(student_id=student.id).all()
    return render_template('diaries.html', diaries=diaries)

@main.route("/courses")
def courses_page():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    courses = Course.query.outerjoin(Teacher).all()
    return render_template("courses.html", courses=courses)

app.register_blueprint(main)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

