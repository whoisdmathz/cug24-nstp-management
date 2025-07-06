from flask import Blueprint, redirect, url_for, render_template, jsonify, session
from sqlalchemy import select
from flask_restful import request

import flask
import datetime
import random
import math

from application.services import db, bcrypt
from application.libraries.status_response import status_response
from application.libraries.request_input import request_header, request_form, request_arg

from application.models.batch_attendance_log import Batch_attendance_log
from application.models.batch_attendance import Batch_attendance
from application.models.batch_student import Batch_student
from application.models.batch import Batch
from application.models.blood_type import Blood_type
from application.models.configuration import Configuration
from application.models.course import Course
from application.models.nstp_component import Nstp_component
from application.models.user_military_science import User_military_science
from application.models.user_type import User_type
from application.models.user import User

view_name = "head-batches"
view_title = "Batches"

head_batch = Blueprint(view_name, __name__)

data = {}

# blueprint function
def head_batch_blueprint(app):
    # constructor
    @head_batch.before_request
    def before_request_func():
        # logout 
        if 'user' in session: 
            if session['user']['userTypeID']!=2: return redirect(url_for('logout.index'))
        else:
            return redirect(url_for('logout.index'))
            
        # initialize variable
        data['view'] = view_name
        data['title'] = view_title
        data['subtitle'] = ''

    return head_batch

# pages
@head_batch.route('/'+view_name+'/')
def index():
    
    model_batches = db.session.query(Batch)
    model_batches = model_batches.outerjoin(Nstp_component, Batch.nstpComponentID==Nstp_component.nstpComponentID)
    model_batches = model_batches.outerjoin(User, Batch.userID==User.userID)
    model_batches = model_batches.with_entities(
        Batch.batchID,
        Nstp_component.code.label('ncCode'),
        Batch.schoolYear,
        Batch.term,
        Batch.code,
        Batch.studentCount,
        User.fname.label('fname'),
        User.mname.label('mname'),
        User.lname.label('lname'),
        Batch.status,
    )
    model_batches = model_batches.filter(Batch.userID==session['user']['userID'])
    model_batches = model_batches.order_by(Batch.schoolYear.desc())
    model_batches = model_batches.order_by(Batch.term.desc())
    model_batches = model_batches.order_by(Batch.nstpComponentID.asc())
    model_batches = model_batches.all()
    
    results = model_batches
    
    data['subtitle'] = ''
    data['results'] = results
    return render_template(view_name.replace("-", "_")+'/index.html', data=data)

@head_batch.route('/'+view_name+'/attendances/<int:batchID>/')
def attendances(batchID):
    
    # students
    model_students = db.session.query(Batch_student)
    model_students = model_students.outerjoin(User, Batch_student.userID==User.userID)
    model_students = model_students.with_entities(
        Batch_student.batchStudentID,
        Batch_student.userID,
        User.lname,
        User.fname,
        User.mname,
    )
    model_students = model_students.filter(Batch_student.batchID==batchID)
    model_students = model_students.order_by(User.lname.asc())
    model_students = model_students.order_by(User.fname.asc())
    model_students = model_students.all()
    
    students = []
    if model_students:
        for student in model_students:
            students.append({
                'batchStudentID': student.batchStudentID, 
                'userID': student.userID, 
                'name': student.lname+', '+student.fname+' '+student.mname, 
            })
    
    # dates 
    model_attendances = db.session.query(Batch_attendance)
    model_attendances = model_attendances.filter(Batch_attendance.batchID==batchID)
    model_attendances = model_attendances.order_by(Batch_attendance.date.asc())
    model_attendances = model_attendances.all()
    
    attendance_dates = {}
    attendances = {}
    if model_attendances:
        for attendance in model_attendances:
            date = attendance.date.strftime('%m/%d/%y')
            attendance_dates[date] = attendance.batchAttendanceID
            
            # logs 
            model_logs = db.session.query(Batch_attendance_log)
            model_logs = model_logs.filter(Batch_attendance_log.batchAttendanceID==attendance.batchAttendanceID)
            model_logs = model_logs.all()
            
            logs = []
            if model_logs:
                for log in model_logs:
                    logs.append(log.batchStudentID)
                
            attendances[date] = logs
            
    data['subtitle'] = 'Attedance'
    data['students'] = students
    data['attendance_dates'] = attendance_dates
    data['attendances'] = attendances
    data['id'] = batchID
    return render_template(view_name.replace("-", "_")+'/attendances.html', data=data)

@head_batch.route('/'+view_name+'/attendance/<int:batchID>/', methods=['POST'])
def attendance_post(batchID):
    
    requests = {
        "date" : request_form("date"), 
    }
    
    data = {} 
    res = status_response(200) 
    
    hasError = False
        
    # required fields
    errors = ''
    required_fields = {
        'date' : 'Date', 
    }
    for key, value in required_fields.items():
        if requests.get(key) == '' or requests.get(key) is None:
            hasError = True
            if errors != '':
                errors += ', '+value 
            else:
                errors += value 
    if hasError is True: res = status_response(409, errors, 'Required field(s):')
    
    if hasError is False:
        
        model_attendance = db.session.query(Batch_attendance)
        model_attendance = model_attendance.filter(Batch_attendance.batchID==batchID)
        model_attendance = model_attendance.filter(Batch_attendance.date==requests.get('date'))
        model_attendance = model_attendance.first()
        if model_attendance is None:
            # insert data
            model_attendance = Batch_attendance(
                batchID = batchID, 
                date = requests.get("date"), 
                dateInserted = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
            )
            db.session.add(model_attendance)
            db.session.commit()
            
            # calculate grades
            calculate_grades(batchID)
    
    data["response"] = res
    return jsonify(data) 

@head_batch.route('/'+view_name+'/attendance/<int:batchAttendanceID>/', methods=['DELETE'])
def attendance_delete(batchAttendanceID):
    
    data = {} 
    res = status_response(200) 
    
    db.session.query(Batch_attendance_log).filter(Batch_attendance_log.batchAttendanceID==batchAttendanceID).delete()
    db.session.commit()
    
    model_attendance = db.session.query(Batch_attendance).filter(Batch_attendance.batchAttendanceID==batchAttendanceID).first()
    # id
    batchID = model_attendance.batchID
    # delete
    db.session.delete(model_attendance)
    db.session.commit()
    
    # calc gardes
    calculate_grades(batchID)
    
    data["response"] = res
    return jsonify(data) 

@head_batch.route('/'+view_name+'/attendance-log/', methods=['POST'])
def attendance_log_post():
    
    requests = {
        "batchStudentID" : request_form("batchStudentID"), 
        "batchAttendanceID" : request_form("batchAttendanceID"), 
        "status" : request_form("status"), 
    }
    
    data = {} 
    res = status_response(200) 
    
    model_attendance = db.session.query(Batch_attendance)
    model_attendance = model_attendance.filter(Batch_attendance.batchAttendanceID==requests.get('batchAttendanceID'))
    model_attendance = model_attendance.first()
    
    batchID = 0
    if model_attendance:
        batchID = model_attendance.batchID
    
    if int(requests.get('status')) == 1:
        model_log = Batch_attendance_log(
            batchAttendanceID = requests.get('batchAttendanceID'), 
            batchStudentID = requests.get('batchStudentID'), 
        )
        db.session.add(model_log)
        db.session.commit()
    else:
        db.session.query(Batch_attendance_log).filter(Batch_attendance_log.batchStudentID==requests.get('batchStudentID'), Batch_attendance_log.batchAttendanceID==requests.get('batchAttendanceID')).delete()
        db.session.commit()
        
    # calculate grades
    calculate_grades(batchID)
    
    data["response"] = res
    return jsonify(data) 

@head_batch.route('/'+view_name+'/view/<int:id>/')
def view(id):
    
    model_batch = db.session.query(Batch)
    model_batch = model_batch.outerjoin(Nstp_component, Batch.nstpComponentID==Nstp_component.nstpComponentID)
    model_batch = model_batch.outerjoin(User, Batch.userID==User.userID)
    model_batch = model_batch.with_entities(
        Batch.batchID,
        Nstp_component.code.label('ncCode'),
        Batch.schoolYear,
        Batch.term,
        Batch.code,
        Batch.studentCount,
        User.fname.label('fname'),
        User.mname.label('mname'),
        User.lname.label('lname'),
        Batch.status,
    )
    model_batch = model_batch.filter(Batch.batchID==id)
    model_batch = model_batch.first()
    
    row = {}
    if model_batch:
        row['batchID'] = model_batch.batchID
        row['ncCode'] = model_batch.ncCode
        row['schoolYear'] = model_batch.schoolYear
        row['term'] = model_batch.term
        row['code'] = model_batch.code
        row['studentCount'] = model_batch.studentCount
        row['fname'] = model_batch.fname
        row['mname'] = model_batch.mname
        row['lname'] = model_batch.lname
        row['status'] = model_batch.status
        
    # students 
    model_students = db.session.query(Batch_student)
    model_students = model_students.outerjoin(User, Batch_student.userID==User.userID)
    model_students = model_students.with_entities(
        Batch_student.batchStudentID,
        Batch_student.userID,
        User.fname.label('fname'),
        User.mname.label('mname'),
        User.lname.label('lname'),
        User.gender,
        Batch_student.attendance,
        Batch_student.exam,
        Batch_student.performance,
        Batch_student.total,
        Batch_student.status,
    )
    model_students = model_students.filter(Batch_student.batchID==id)
    model_students = model_students.order_by(User.lname.asc())
    model_students = model_students.order_by(User.fname.asc())
    model_students = model_students.all()
        
    students = []
    student_bgs = ['danger', 'info', 'success']
    student_statuses = ['Failed', 'On Going', 'Passed']
    if model_students:
        for student in model_students:
            students.append({
                'batchStudentID': student.batchStudentID, 
                'userID': student.userID, 
                'lname': student.lname, 
                'fname': student.fname, 
                'mname': student.mname, 
                'gender': 'Male' if student.gender==1 else 'Female', 
                'attendance': student.attendance, 
                'exam': student.exam, 
                'performance': student.performance, 
                'total': student.total, 
                'status': student.status, 
                'statusBg': student_bgs[int(student.status)+1], 
                'statusName': student_statuses[int(student.status)+1], 
            })
            
    maxExam = 0
    maxPerformance = 0
    passingGrade = 0
    
    model_config = db.session.query(Configuration)
    model_config = model_config.filter_by(name='Exam')
    model_config = model_config.first()
    if model_config:
        maxExam = model_config.value
    
    model_config = db.session.query(Configuration)
    model_config = model_config.filter_by(name='Performance')
    model_config = model_config.first()
    if model_config:
        maxPerformance = model_config.value
    
    model_config = db.session.query(Configuration)
    model_config = model_config.filter_by(name='Passing')
    model_config = model_config.first()
    if model_config:
        passingGrade = model_config.value
    
    data['subtitle'] = 'View'
    data['id'] = id
    data['row'] = row
    data['students'] = students
    data['statuses'] = ['Open', 'On Going', 'Done']
    data['maxExam'] = maxExam
    data['maxPerformance'] = maxPerformance
    data['passingGrade'] = passingGrade
    return render_template(view_name.replace("-", "_")+'/view.html', data=data)

@head_batch.route('/'+view_name+'/student-info/<int:batchID>/<int:batchStudentID>/')
def student_info(batchID, batchStudentID):
    
    model_user = db.session.query(User)
    model_user = model_user.outerjoin(Course, User.courseID==Course.courseID)
    model_user = model_user.outerjoin(Nstp_component, User.nstpComponentID==Nstp_component.nstpComponentID)
    model_user = model_user.outerjoin(Blood_type, User.bloodTypeID==Blood_type.bloodTypeID)
    model_user = model_user.outerjoin(Batch_student, User.userID==Batch_student.userID)
    model_user = model_user.with_entities(
        User.userID,
        User.username,
        User.studentNo,
        User.lname,
        User.fname,
        User.mname,
        User.ename,
        Course.code.label('cCode'),
        User.yearLevel,
        Nstp_component.code.label('ncCode'),
        Blood_type.name.label('btName'),
        User.gender,
        User.phone,
        User.birthDate,
        User.birthPlace,
        User.email,
        User.religion,
        User.citizenship,
        User.addressHomeStreet,
        User.addressHomeMunicipality,
        User.addressHomeProvince,
        User.addressHomePhone,
        User.addressTemporaryStreet,
        User.addressTemporaryMunicipality,
        User.addressTemporaryProvince,
        User.addressTemporaryPhone,
        User.fatherName,
        User.fatherOccupation,
        User.motherName,
        User.motherOccupation,
        User.emergencyContactName,
        User.emergencyContactPhone,
        User.emergencyContactRelationship,
        User.emergencyContactAddress,
        User.height,
        User.weigh,
        User.complexion,
        User.takeAdvanceCourse,
        User.nstpComponentID,
    )
    model_user = model_user.filter(Batch_student.batchStudentID==batchStudentID)
    model_user = model_user.first()
    
    data['subtitle'] = 'Student Info'
    data['id'] = batchID
    data['row'] = model_user
    return render_template(view_name.replace("-", "_")+'/student_info.html', data=data)

@head_batch.route('/'+view_name+'/update-exam/<int:batchStudentID>/', methods=['PUT'])
def update_exam(batchStudentID):
    
    requests = {
        "score" : request_form("score"), 
    }
    
    bg = 'danger'
    total = 0
    data = {}
    res = status_response(200)

    # code here...
    model_stud = Batch_student.query.filter_by(batchStudentID=batchStudentID).first()
    if model_stud:
        
        total = int(requests.get('score'))+int(model_stud.performance)+int(model_stud.attendance)
        
        model_stud.exam = requests.get('score')
        model_stud.total = total
        db.session.commit()
        
    model_config = db.session.query(Configuration)
    model_config = model_config.filter_by(name='Passing')
    model_config = model_config.first()
    if model_config:
        passingGrade = model_config.value
        
        if int(total)>=int(passingGrade): bg = 'success'
    
    model_student = db.session.query(Batch_student)    
    model_student = model_student.filter(Batch_student.batchStudentID==batchStudentID)
    model_student = model_student.first()
    
    batchID = 0
    if model_student:
        batchID = model_student.batchID
    
    # calculate grade 
    calculate_grades(batchID)
        
    data["total"] = total
    data["bg"] = bg
    data["response"] = res
    return jsonify(data)

@head_batch.route('/'+view_name+'/update-performance/<int:batchStudentID>/', methods=['PUT'])
def update_performance(batchStudentID):
    
    requests = {
        "score" : request_form("score"), 
    }
    
    bg = 'danger'
    total= 0
    data = {}
    res = status_response(200)

    # code here...
    model_stud = Batch_student.query.filter_by(batchStudentID=batchStudentID).first()
    if model_stud:
        
        total = int(requests.get('score'))+int(model_stud.exam)+int(model_stud.attendance)
        
        model_stud.performance = requests.get('score')
        model_stud.total = total
        db.session.commit()
        
    model_config = db.session.query(Configuration)
    model_config = model_config.filter_by(name='Passing')
    model_config = model_config.first()
    if model_config:
        passingGrade = model_config.value
        
        if int(total)>=int(passingGrade): bg = 'success'
        
    model_student = db.session.query(Batch_student)    
    model_student = model_student.filter(Batch_student.batchStudentID==batchStudentID)
    model_student = model_student.first()
    
    batchID = 0
    if model_student:
        batchID = model_student.batchID
    
    # calculate grade 
    calculate_grades(batchID)
        
    data["total"] = total
    data["bg"] = bg
    data["response"] = res
    return jsonify(data)

@head_batch.route('/'+view_name+'/student-remove/<int:batchStudentID>/', methods=['DELETE'])
def student_remove(batchStudentID):
    data = {}
    res = status_response(200)

    # code here...
    model_stud = Batch_student.query.filter_by(batchStudentID=batchStudentID).first()
    db.session.delete(model_stud)
    db.session.commit()
        
    data["response"] = res
    return jsonify(data)

def calculate_grades(batchID):
    
    # rating 
    model_config = db.session.query(Configuration)
    model_config = model_config.filter(Configuration.name=='Attendance')
    model_config = model_config.first()
    
    attendance_rating = 0
    if model_config:
        attendance_rating = int(model_config.value) if model_config.value else 0
    
    # attendances 
    model_attendances = db.session.query(Batch_attendance)
    model_attendances = model_attendances.filter(Batch_attendance.batchID==batchID)
    model_attendances = model_attendances.order_by(Batch_attendance.date.asc())
    model_attendances = model_attendances.all()
    
    attendance_total = 0
    if model_attendances:
        for attendance in model_attendances:
            attendance_total+=1
            
    # students
    model_students = db.session.query(Batch_student)
    model_students = model_students.filter(Batch_student.batchID==batchID)
    model_students = model_students.all()
    
    if model_students:
        for student in model_students:
            
            attendance_student = 0
            
            if model_attendances:
                for attendance in model_attendances:
                    
                    # log
                    model_log = db.session.query(Batch_attendance_log)
                    model_log = model_log.filter(Batch_attendance_log.batchAttendanceID==attendance.batchAttendanceID)
                    model_log = model_log.filter(Batch_attendance_log.batchStudentID==student.batchStudentID)
                    model_log = model_log.first()
                    
                    if model_log:
                        attendance_student+=1
            
            attendance_grade = (attendance_rating*attendance_student) / attendance_total
            attendance_grade = math.floor(attendance_grade)
            
            model_student = Batch_student.query.filter_by(batchStudentID=student.batchStudentID).first()
            if model_student is not None:
                
                total = attendance_grade + int(model_student.exam) + int(model_student.performance)
                
                model_student.attendance = attendance_grade
                model_student.total = total
                db.session.commit()
                        