import os
#from typing import KeysView
from flask import Flask, flash, redirect, request, abort, jsonify, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import datetime
from datetime import datetime
from sqlalchemy import cast, func


from sqlalchemy import null
from model import setup_db, Attendance, MarkAttendance, Admin, Student, Course, Lecturer


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Kepman123@localhost:5432/attendance_db'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db = SQLAlchemy(app)
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    CORS(app)
    setup_db(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, DELETE,')
        return response

    # Add student  View endpoint
    @app.route('/', methods=['GET'])
    def home():
        return jsonify({'Welcome':'Success'})

    # Add student  View endpoint
    @app.route('/view_add_student', methods=['GET'])
    def view_add_student():
        return render_template('pages/add_student.html') 

    # Add lecturer  View endpoint
    @app.route('/view_add_lecturer', methods=['GET'])
    def view_add_lecturer():
        return render_template('pages/add_lecturer.html') 

    # Add Admin  View endpoint
    @app.route('/view_add_admin', methods=['GET'])
    def view_add_admin():
        return render_template('pages/add_admin.html')
        
    # Add Course  View endpoint
    @app.route('/view_add_course', methods=['GET'])
    def view_add_course():
        value = []
        value_1 = []
        '''try:'''
        data = Lecturer.query.order_by(Lecturer.id).all()
        data_1 = Student.query.order_by(Student.id).all()
        for lecturer in data:
            value.append(
                        {
                            'id': lecturer.id,
                            'name': lecturer.name,
                            'email': lecturer.email

                        }
                        )
        
        for student in data_1:
            value_1.append(
                        {
                            'id': student.id,
                            'name': student.name,
                            'email': student.email

                        }
                        )
        return render_template('pages/add_course.html', lecturers=value, students=value_1)
        
        '''except(Exception):
            abort(422)'''

    @app.route('/view_mark_attendance')
    def view_mark_attendance():
        return render_template('pages/student_dashboard.html', student=data)

    # Remove student endpoint
    @app.route('/remove_student/<int:id>', methods=['GET'])
    def remove_student(id):
        try:
            student = Student.query.filter(Student.id==id).one_or_none()  
            student.delete()
            flash('Success', 'Student removed successfully!')
            return render_template('pages/Admin_dashboard.html')
        except(Exception):
            abort(422)
    
    # View Edit student endpoint
    @app.route('/view_edit_student/<int:id>', methods=['GET'])
    def view_edit_student(id):
        
        student = Student.query.get(id)
        if not student:
            return jsonify({'error': 'Student not found!'}), 404

        try:
            data = {
                        'id':student.id,
                        'name':student.name,
                        'email':student.email,
                        'college':student.college,
                        'department':student.department,
                        'level':student.level
                    }
            return render_template('pages/edit_student_profile.html', student=data)
        except(Exception):
            abort(422)
        
    # Edit student endpoint
    @app.route('/view_edit_adstudent/<int:id>', methods=['GET'])
    def view_edit_adstudent(id):
        
        student = Student.query.get(id)
        if not student:
            return jsonify({'error': 'Student not found!'}), 404

        try:
            data = {
                        'id':student.id,
                        'name':student.name,
                        'email':student.email,
                        'college':student.college,
                        'department':student.department,
                        'level':student.level
                    }
            return render_template('pages/edit_admin_student.html', student=data)
        except(Exception):
            abort(422)
    
    # Edit Course  View endpoint
    @app.route('/view_edit_adcourse/<int:id>', methods=['GET'])
    def view_edit_adcourse(id):
        value = []
        value_1 = []

        course = Course.query.get(id)
        if not course:
            return jsonify({'error': 'Course not found!'}), 404

        try:
            data = Lecturer.query.order_by(Lecturer.id).all()
            data_1 = Student.query.order_by(Student.id).all()

            data_2 = {
                        'id':course.id,
                        'name':course.name,
                        'email':course.code
                    }

            for lecturer in data:
                value.append(
                            {
                                'id': lecturer.id,
                                'name': lecturer.name,
                                'email': lecturer.email

                            }
                            )
            
            for student in data_1:
                value_1.append(
                            {
                                'id': student.id,
                                'name': student.name,
                                'email': student.email

                            }
                            )
            return render_template('pages/edit_admin_course.html.html', course=data_2, lecturers=value, students=value_1)
         
        except(Exception):
            abort(422)


    # Edit Lecturer endpoint
    @app.route('/view_edit_adlecturer/<int:id>', methods=['GET'])
    def view_edit_adlecturer(id):
        
        lecturer = Lecturer.query.get(id)
        if not lecturer:
            return jsonify({'error': 'Lecturer not found!'}), 404

        try:
            data = {
                        'id':lecturer.id,
                        'name':lecturer.name,
                        'email':lecturer.email
                    }
            return render_template('pages/edit_admin_lecturer.html', lecturer=data)
        except(Exception):
            abort(422)
    
    # Edit Admin endpoint
    @app.route('/view_edit_adadmin/<int:id>', methods=['GET'])
    def view_edit_adadmin(id):
        
        admin = Admin.query.get(id)
        if not admin:
            return jsonify({'error': 'Admin not found!'}), 404

        try:
            data = {
                        'id':admin.id,
                        'full_name':admin.full_name,
                        'username':admin.username
                    }
            return render_template('pages/edit_admin_admin.html', admin=data)
        except(Exception):
            abort(422)


    # Edit student endpoint
    @app.route('/edit_student/<int:id>', methods=['POST'])
    def edit_student(id):
        student = Student.query.get(id)
        if not student:
            return jsonify({'error': 'Student not found!'}), 404
        student.name = request.form.get('name', None)
        student.email = request.form.get('email', None)
        student.college = request.form.get('college', None)
        student.department = request.form.get('department', None)
        student.level = request.form.get('level', None)
        student.password = request.form.get('password', None)

        if student.name =='' or student.email =='' or student.college =='' or student.department =='' or student.level =='' or student.password =='':
            abort(400)

        try:
            Student.update(self= (student.name, student.email, student.college, student.department, student.level, student.password,))
            flash('Success', 'Student updated successfully!')
            data = {
                        'id':student.id,
                        'name':student.name,
                        'email':student.email,
                        'college':student.college,
                        'department':student.department,
                        'level':student.level
                        

                    }
            return render_template('pages/student_dashboard.html', student=data)
        except(Exception):
            abort(422)

    # Edit student endpoint
    @app.route('/edit_adstudent/<int:id>', methods=['POST'])
    def edit_adstudent(id):
        value = []
        student = Student.query.get(id)
        if not student:
            return jsonify({'error': 'Student not found!'}), 404
        student.name = request.form.get('name', None)
        student.email = request.form.get('email', None)
        student.college = request.form.get('college', None)
        student.department = request.form.get('department', None)
        student.level = request.form.get('level', None)
        student.password = request.form.get('password', None)

        if student.name =='' or student.email =='' or student.college =='' or student.department =='' or student.level =='' or student.password =='':
            abort(400)

        try:
            Student.update(self= (student.name, student.email, student.college, student.department, student.level, student.password,))
            flash('Success', 'Student updated successfully!')
            data = Student.query.order_by(Student.id).all()
            for student in data:
                value.append(
                            {
                                'id':student.id,
                                'name':student.name,
                                'email':student.email,
                                'college':student.college,
                                'department':student.department,
                                'level':student.level

                            }
                            )
            return render_template('pages/Admin_dashboard.html', students=value)
        except(Exception):
            abort(422)

    # Edit Lecturer endpoint
    @app.route('/edit_adlecturer/<int:id>', methods=['POST'])
    def edit_adlecturer(id):
        value = []
        lecturer = Lecturer.query.get(id)
        if not lecturer:
            return jsonify({'error': 'Student not found!'}), 404
        lecturer.name = request.form.get('name', None)
        lecturer.email = request.form.get('email', None)
        lecturer.password = request.form.get('password', None)

        if lecturer.name =='' or lecturer.email =='' or lecturer.password =='' :
            abort(400)

        try:
            Lecturer.update_l(self= (lecturer.name, lecturer.email, lecturer.password))
            flash('Success', 'Lecturer updated successfully!')
            return render_template('pages/Admin_dashboard.html')
        except(Exception):
            abort(422)

    # Edit Admin endpoint
    @app.route('/edit_adadmin/<int:id>', methods=['POST'])
    def edit_adadmin(id):
        admin = Admin.query.get(id)
        if not admin:
            return jsonify({'error': 'Student not found!'}), 404
        admin.full_name = request.form.get('full_name', None)
        admin.username = request.form.get('username', None)
        admin.password = request.form.get('password', None)

        if admin.full_name =='' or admin.username =='' or admin.password =='' :
            abort(400)

        try:
            Admin.update_ad(self= (admin.username, admin.password, admin.full_name))
            flash('Success', 'Admin updated successfully!')
            return render_template('pages/Admin_dashboard.html')
        except(Exception):
            abort(422)

    # Edit Course endpoint
    @app.route('/edit_adcourse/<int:id>', methods=['POST'])
    def edit_adcourse(id):
        course = Course.query.get(id)
        if not course:
            return jsonify({'error': 'Course not found!'}), 404

        course.name = request.form.get('name', None)
        course.code = request.form.get('code', None)
        course.lecturer_id = request.form.get('lecturer_id', None)
        course.student_id = request.form.get('student_id', None)

        if course.name =='' or course.code =='' or  course.lecturer_id =='' or  course.student_id =='':
            abort(400)

        try:
            Course.update_c(self= (course.name, course.code, course.lecturer_id, course.student_id))
            flash('Success', 'Course updated successfully!')
            return render_template('pages/Admin_dashboard.html')
        except(Exception):
            abort(422)

    # View lecturer endpoint 
    @app.route('/view_lecturer', methods=['GET'])
    def view_lecturer():
        data = {'id':3}
        '''try:'''
        return render_template('pages/lecturer_dashboard.html', lecturer=data)
        ''' except(Exception):
            abort(422)'''

    # Add lecturer endpoint
    @app.route('/view_student')
    def view_student():
        data ={
        'id': 3,
        'name': 'John Doe',
        'email': 'johndoe@example.com',
        'password': 'password123',
        'courses': [
            {
                'id': 1,
                'name': 'Introduction to Computer Science',
                'description': 'An introductory course in computer science.',
                'lecturer': {
                    'id': 1,
                    'name': 'Jane Smith',
                    'email': 'janesmith@example.com'
                }
            },
            {
                'id': 2,
                'name': 'Database Management Systems',
                'description': 'A course in database management systems.',
                'lecturer': {
                    'id': 2,
                    'name': 'Bob Johnson',
                    'email': 'bobjohnson@example.com'
                            }
                        }
                    ]
                }
        return render_template('pages/student_dashboard.html', student=data)
        #return jsonify({'success': 'Lecturer added successfully!'})

    # Remove lecturer endpoint
    @app.route('/remove_lecturer/<int:id>', methods=['GET'])
    def remove_lecturer(id):
        try:
            lecturer = Lecturer.query.filter(Lecturer.id==id).one_or_none()  
            lecturer.delete_l()
            flash('Success', 'Lecturer removed successfully!')
            return render_template('pages/Admin_dashboard.html')
        except(Exception):
            abort(422)
       
    # Edit lecturer endpoint
    @app.route('/edit_lecturer/<int:id>', methods=['POST'])
    def edit_lecturer(id):
        lecturer = Lecturer.query.get(id)
        if not lecturer:
            return jsonify({'error': 'Lecturer not found!'}), 404
        name = request.form.get('name', lecturer.name)
        email = request.form.get('email', lecturer.email)
        password = request.form.get('password', lecturer.password)    
        update_record = lecturer.name = name, lecturer.email = email, lecturer.password = password 
        update_record.insert()
        return jsonify({'success': 'Lecturer updated successfully!'})

    # View admin endpoint navigation for Edit student
    @app.route('/view_admin_student', methods=['GET'])
    def view_admin_student():
        value = []
        try:
            data = Student.query.order_by(Student.id).all()
            for student in data:
                value.append(
                            {
                                'id': student.id,
                                'name': student.name,
                                'email': student.email

                            }
                            )
            return render_template('pages/Edit_student.html', students=value)
        except(Exception):
            abort(422)

    # View admin endpoint navigation for Edit lecturer
    @app.route('/view_admin_lecturer', methods=['GET'])
    def view_admin_lecturer():
        value = []
        try:
            data = Lecturer.query.order_by(Lecturer.id).all()
            for lecturer in data:
                value.append(
                            {
                                'id': lecturer.id,
                                'name': lecturer.name,
                                'email': lecturer.email

                            }
                            )
            return render_template('pages/Edit_lecturer.html', lecturers=value)
        except(Exception):
            abort(422)
    
    # View admin endpoint navigation for Edit admin
    @app.route('/view_admin_ad', methods=['GET'])
    def view_admin_ad():
        value = []
        try:
            data = Admin.query.order_by(Admin.id).all()
            for admin in data:
                value.append(
                            {
                                'id': admin.id,
                                'username': admin.username,
                                'full_name': admin.full_name

                            }
                            )
            return render_template('pages/Edit_admin.html', admins=value)
        except(Exception):
            abort(422)

    # View admin endpoint 
    @app.route('/view_admin', methods=['GET'])
    def view_admin():
        value = []
        try:
            return render_template('pages/Admin_dashboard.html')
        except(Exception):
            abort(422)
    
    # Add student endpoint
    @app.route('/add_student', methods=['POST'])
    def add_student():
        data = {}
        value = []
        name = request.form['name']
        email = request.form['email']
        college = request.form['college']
        department = request.form['department']
        level = request.form['level']
        password = request.form['password']
        
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Error', 'Password Mismatch!')
            return render_template('pages/add_student.html')

        try:
            student = Student(name=name, email=email, college=college, department=department, level=level, password=password)
            student.insert()
            flash('success', 'Student added successfully!')
            return render_template('pages/Admin_dashboard.html')
        except(Exception):
            flash('Existence', 'Email Already Exist!')
            print(data)
        return render_template('pages/add_student.html')        

    # Add Admin endpoint
    @app.route('/add_admin', methods=['POST'])
    def add_admin():
        data = {}
        value = []
    
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        full_name = request.form['full_name']
        

        if password != confirm_password:
            flash('Error', 'Password Mismatch!')
            return render_template('pages/add_admin.html')

        try:
            admin = Admin(username=username, password=password, full_name=full_name)
            admin.insert_ad()
            flash('success', 'Admin added successfully!')
            return render_template('pages/Admin_dashboard.html')
        except(Exception):
            flash('Existence', 'Email Already Exist!')
            print(data)
        return render_template('pages/add_admin.html')   


        
    
    # Add Lecturer endpoint
    @app.route('/add_lecturer', methods=['POST'])
    def add_lecturer():
        data = {}
        value = []
    
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
       
        if password != confirm_password:
            flash('Error', 'Password Mismatch!')
            return render_template('pages/add_admin.html')

        try:
            lecturer = Lecturer(name=name, email=email, password=password)
            lecturer.insert_l()
            flash('success', 'Lecturer added successfully!')
            return render_template('pages/Admin_dashboard.html')
        except(Exception):
            flash('Existence', 'Email Already Exist!')
            print(data)
        return render_template('pages/add_lecturer.html')   

    # Add Course endpoint
    @app.route('/add_course', methods=['POST'])
    def add_course():
        name = request.form['name']
        code = request.form['code']
        lecturer_id = request.form['lecturer_id']
        student_ids = request.form['student_id']
        
        print(student_ids)
        print(lecturer_id)
        try:
            course = Course(name=name, code=code, lecturer_id=lecturer_id, student_id=student_ids)
            course.insert_c()
            flash('success', 'Course added successfully!')
            return render_template('pages/Admin_dashboard.html')
        except(Exception):
            flash('Existence', 'Course Code Already Exist!')
        return render_template('pages/add_course.html')   
    
    # Remove Course endpoint
    @app.route('/remove_course/<int:id>', methods=['GET'])
    def remove_course(id):
        try:
            course = Course.query.filter(Course.id==id).one_or_none()  
            course.delete_c()
            flash('Success', 'Course removed successfully!')
            return render_template('pages/Admin_dashboard.html')
        except(Exception):
            abort(422)

    # Remove admin endpoint
    @app.route('/remove_admin/<int:id>', methods=['GET'])
    def remove_admin(id):
        try:
            admin = Admin.query.filter(Admin.id==id).one_or_none()  
            admin.delete_ad()
            flash('Success', 'Admin removed successfully!')
            return render_template('pages/Admin_dashboard.html')
        except(Exception):
            abort(422)
        
    
    # Edit admin endpoint
    @app.route('/edit_admin/<int:id>', methods=['POST'])
    def edit_admin(id):
        admin = Admin.query.filter_by(id=id).first()
        if not admin:
            return jsonify({'error': 'Admin not found!'})

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        admin.name = name
        admin.email = email
        admin.password = password

        admin.name.insert()
        admin.email.insert()
        admin.password.insert()

        return jsonify({'success': 'Admin updated successfully!'})


    #Generate attendance endpoint
    @app.route('/generate_attendance', methods=['POST'])
    def generate_attendance():
        course_id = request.form['course_id']
        lecturer_id = request.form['course.lecturer_id']
        date = request.form['date']
        time = request.form['time']
        timeframe = request.form['timeframe']


        #Validating if attendance already exist for the same course on the same day
        search_questions= '%' + date
        response = Attendance.query.filter(func.cast(Attendance.date, db.String).ilike(search_questions),
                                            Attendance.course_id == course_id
                                        ).all()

        if response == []:
            attendance = Attendance(date=date, time=time, timeframe=timeframe, course_id=course_id, lecturer_id=lecturer_id)
            attendance.insert_at()
            return jsonify({'success': 'Attendance generated successfully!'})
        else:
            return jsonify({'Existence': 'Attendance already exit for this course for today time frame!'})
    
        #response = Attendance.query.filter(Attendance.date.ilike(date), Attendance.course_id == course_id).all()
       
        # Create a new attendance record

        # Add the attendance record to the database
        
        # Return a success message


    #Generate attendance endpoint
    @app.route('/view_generate_attendance/<int:id>', methods=['GET'])
    def view_generate_attendance(id):
        lecturer = Course.query.filter(Course.lecturer_id==(id)).all()
        data = []

        for a in lecturer:
            data.append(
                        {
                            'id':a.id,
                            'name':a.name,
                            'code':a.code,
                            'lecturer_id':a.lecturer_id
                        })
        return render_template('pages/generate_attendance.html', courses=data)
            
            


        '''course = Course.query.get(id)
        if not course:
            return jsonify({'error': 'Student not found!'}), 404

        lecturers = course.lecturers.all()
        if not lecturers:
            return jsonify({'error': 'No lecturers found for the course!'})

        students = course.students.all()
        if not students:
            return jsonify({'error': 'No students found for the course!'})'''
        
        '''try'''
    
   



    #Mark attendance endpoint
    @app.route('/mark_attendance/<int:id>', methods=['GET'])
    def mark_attendance(id):
        '''if request.method == 'POST':
            date = request.form['date']
            time = request.form['time']
            ...
        else:'''
        now = datetime.now()
        date_str = now.strftime('%Y-%m-%d')
        time_str = now.strftime('%H:%M')

        return render_template('pages/mark_attendance.html', date=date_str, time=time_str)


    
    '''@app.route('/mark_attendance/<int:course_id>', methods=['POST'])
    def mark_attendance(course_id):
        course = Course.query.filter_by(id=course_id).first()
        if not course:
            return jsonify({'error': 'Course not found!'})

        student_id = request.form['student_id']
        student = course.students.filter_by(id=student_id).first()
        if not student:
            return jsonify({'error': 'Student not found for the course!'})

        date = datetime.now().date()
        mark_attendance = MarkAttendance.query.filter_by(course_id=course_id, student_id=student_id, date=date).first()

        if mark_attendance:
            return jsonify({'error': 'Attendance already marked for the student!'})

        mark_attendance = MarkAttendance(
            date=date,
            course_id=course_id,
            student_id=student_id
            
        )
        mark_attendance.insert_mk()

        return jsonify({'success': 'Attendance marked successfully!'})
'''
    # Login endpoint
    @app.route('/login', methods=['POST'])
    def login():
        email = request.form['email']
        password = request.form['password']

        # check if admin exists
        admin = Admin.query.filter_by(email=email).first()
        if admin and check_password_hash(admin.password, password):
            # login admin
            session['admin'] = admin.id
            return jsonify({'success': 'Admin logged in successfully!'})

        # check if student exists
        student = Student.query.filter_by(email=email).first()
        if student and check_password_hash(student.password, password):
            # login student
            session['student'] = student.id
            return jsonify({'success': 'Student logged in successfully!'})

        # check if lecturer exists
        lecturer = Lecturer.query.filter_by(email=email).first()
        if lecturer and check_password_hash(lecturer.password, password):
            # login lecturer
            session['lecturer'] = lecturer.id
            return jsonify({'success': 'Lecturer logged in successfully!'})

        # if login unsuccessful, return error message
        return jsonify({'error': 'Invalid credentials. Please try again.'})    

          
    @app.errorhandler(404)
    def Not_found(error):
        return jsonify({
        "success": False, 
        "error": 404,
        "message": "Resource Not Found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
        "success": False, 
        "error": 422,
        "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
        "success": False, 
        "error": 400,
        "message": "Bad Request"
        }), 400

    @app.errorhandler(405)
    def wrong_method(error):
        return jsonify({
        "success": False, 
        "error": 405,
        "message": "Method Not Allowed"
        }), 405
    return app
    
    

