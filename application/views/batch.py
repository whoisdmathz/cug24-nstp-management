from flask import Blueprint, redirect, url_for, render_template, jsonify, session
from sqlalchemy import select
from flask_restful import request

import flask
import datetime
import random

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

view_name = "batches"
view_title = "Batches"

batch = Blueprint(view_name, __name__)

data = {}

# blueprint function
def batch_blueprint(app):
    # constructor
    @batch.before_request
    def before_request_func():
        # logout 
        if 'user' in session: 
            if session['user']['userTypeID']!=1: return redirect(url_for('logout.index'))
        else:
            return redirect(url_for('logout.index'))
            
        # initialize variable
        data['view'] = view_name
        data['title'] = view_title
        data['subtitle'] = ''

    return batch

# pages
@batch.route('/'+view_name+'/')
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
    model_batches = model_batches.order_by(Batch.schoolYear.desc())
    model_batches = model_batches.order_by(Batch.term.desc())
    model_batches = model_batches.order_by(Batch.nstpComponentID.asc())
    model_batches = model_batches.all()
    
    results = model_batches
    
    data['subtitle'] = ''
    data['results'] = results
    return render_template(view_name.replace("-", "_")+'/index.html', data=data)

@batch.route('/'+view_name+'/add/')
def add():
    
    model_users = db.session.query(User)
    model_users = model_users.outerjoin(Nstp_component, User.nstpComponentID==Nstp_component.nstpComponentID)
    model_users = model_users.with_entities(
        User.userID,
        Nstp_component.code.label('ncCode'),
        User.lname,
        User.fname,
        User.mname,
    )
    model_users = model_users.filter(User.userTypeID==2)
    model_users = model_users.all()
    
    instructors = []
    if model_users:
        for user in model_users:
            instructors.append({
                'userID': user.userID, 
                'name': user.ncCode+' - '+user.lname+', '+user.fname+' '+user.mname
            })
    
    data['subtitle'] = 'Add'
    data['instructors'] = instructors
    data['yearStart']   = 2000
    data['yearEnd']     = int(datetime.datetime.now().strftime('%Y'))
    return render_template(view_name.replace("-", "_")+'/add.html', data=data)

@batch.route('/'+view_name+'/view/<int:id>/')
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
                'name': student.lname+', '+student.fname+' '+student.mname, 
                'gender': 'Male' if student.gender==1 else 'Female', 
                'attendance': student.attendance, 
                'exam': student.exam, 
                'performance': student.performance, 
                'total': student.total, 
                'statusBg': student_bgs[int(student.status)+1], 
                'statusName': student_statuses[int(student.status)+1], 
            })
    
    data['subtitle'] = 'View'
    data['id'] = id
    data['row'] = row
    data['students'] = students
    data['statuses'] = ['Open', 'On Going', 'Done']
    return render_template(view_name.replace("-", "_")+'/view.html', data=data)

@batch.route('/'+view_name+'/edit/<int:id>/')
def edit(id):
    
    model_batch = db.session.query(Batch)
    model_batch = model_batch.outerjoin(Nstp_component, Batch.nstpComponentID==Nstp_component.nstpComponentID)
    model_batch = model_batch.outerjoin(User, Batch.userID==User.userID)
    model_batch = model_batch.with_entities(
        Batch.batchID,
        Batch.userID,
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
        row['userID'] = model_batch.userID
        row['ncCode'] = model_batch.ncCode
        row['schoolYear'] = model_batch.schoolYear
        row['term'] = model_batch.term
        row['code'] = model_batch.code
        row['studentCount'] = model_batch.studentCount
        row['fname'] = model_batch.fname
        row['mname'] = model_batch.mname
        row['lname'] = model_batch.lname
        row['status'] = model_batch.status
    
    model_users = db.session.query(User)
    model_users = model_users.outerjoin(Nstp_component, User.nstpComponentID==Nstp_component.nstpComponentID)
    model_users = model_users.with_entities(
        User.userID,
        Nstp_component.code.label('ncCode'),
        User.lname,
        User.fname,
        User.mname,
    )
    model_users = model_users.filter(User.userTypeID==2)
    model_users = model_users.all()
    
    instructors = []
    if model_users:
        for user in model_users:
            instructors.append({
                'userID': user.userID, 
                'name': user.ncCode+' - '+user.lname+', '+user.fname+' '+user.mname
            })
            
    data['subtitle'] = 'Edit'
    data['id'] = id
    data['instructors'] = instructors
    data['row'] = row
    data['yearStart']   = 2000
    data['yearEnd']     = int(datetime.datetime.now().strftime('%Y'))
    return render_template(view_name.replace("-", "_")+'/edit.html', data=data)

def generate_random_code():
    nums = random.randint(100000, 999999)
    
    model_b = db.session.query(Batch)
    model_b = model_b.filter(Batch.code==nums)
    model_b = model_b.filter(Batch.status!=2)
    model_b = model_b.first()
    
    if model_b:
        return generate_random_code()  
    else:
        return nums

# api 
@batch.route('/'+view_name+'/api/', methods=['POST'])
def post():
    
    requests = {
        "userID"        : request_form("userID"), 
        "schoolYear"    : request_form("schoolYear"), 
        "term"          : request_form("term"), 
    }
    
    data = {} 
    res = status_response(200) 
    
    hasError = False
        
    # required fields
    errors = ''
    required_fields = {
        'userID'        : 'Instructor', 
        'schoolYear'    : 'School Year', 
        'term'          : 'Term', 
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
        
        nstpComponentID = 0
        code            = generate_random_code()
        studentCount    = 0
        
        model_user = db.session.query(User).filter_by(userID=requests.get("userID")).first()
        if model_user:
            nstpComponentID = model_user.nstpComponentID
        
        # Batch already exist 
        model_batch = db.session.query(Batch)
        model_batch = model_batch.filter(Batch.nstpComponentID==nstpComponentID)
        model_batch = model_batch.filter(Batch.schoolYear==requests.get("schoolYear"))
        model_batch = model_batch.filter(Batch.term==requests.get("term"))
        model_batch = model_batch.first()
        if model_batch is None:
            # insert data
            model_batch = Batch(
                userID = requests.get("userID"), 
                nstpComponentID = nstpComponentID, 
                schoolYear = requests.get("schoolYear"), 
                term = requests.get("term"), 
                code = code, 
                studentCount = studentCount, 
                status = 0, 
            )
            db.session.add(model_batch)
            db.session.commit()
        else:
            res = status_response(409, 'Batch already exist.')
    
    data["response"] = res
    return jsonify(data) 

@batch.route('/'+view_name+'/api/<int:id>/', methods=['PUT']) 
def put(id):
    
    requests = {
        "userID"        : request_form("userID"), 
        "schoolYear"    : request_form("schoolYear"), 
        "term"          : request_form("term"), 
        "status"        : request_form("status"), 
    }
    
    data = {} 
    res = status_response(200) 
    
    hasError = False
        
    # required fields
    errors = ''
    required_fields = {
        'status'        : 'Status', 
        'userID'        : 'Instructor', 
        'schoolYear'    : 'School Year', 
        'term'          : 'Term', 
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
        
        nstpComponentID = 0
        code            = generate_random_code()
        
        model_user = db.session.query(User).filter_by(userID=requests.get("userID")).first()
        if model_user:
            nstpComponentID = model_user.nstpComponentID
        
        # Batch already exist 
        model_batch = db.session.query(Batch)
        model_batch = model_batch.filter(Batch.nstpComponentID==nstpComponentID)
        model_batch = model_batch.filter(Batch.schoolYear==requests.get("schoolYear"))
        model_batch = model_batch.filter(Batch.term==requests.get("term"))
        model_batch = model_batch.filter(Batch.batchID!=id)
        model_batch = model_batch.first()
        if model_batch is None:
            
            # update data
            model_batch = db.session.query(Batch).filter_by(batchID=id).first()
            if model_batch: 
                model_batch.nstpComponentID = nstpComponentID
                model_batch.userID = requests.get("userID") 
                model_batch.schoolYear = requests.get("schoolYear") 
                model_batch.term = requests.get("term") 
                if int(requests.get("status"))==0: model_batch.code = code 
                model_batch.status = requests.get("status") 
                db.session.commit()
                
                if int(requests.get("status")) == 2:
                    
                    # passing
                    model_config = db.session.query(Configuration)
                    model_config = model_config.filter(Configuration.name=='Passing')
                    model_config = model_config.first()
                    
                    passing = 0
                    if model_config:
                        passing = int(model_config.value) if model_config.value else 0
                    
                    # students
                    model_student = db.session.query(Batch_student)
                    model_student = model_student.filter(Batch_student.batchID==id)
                    model_student = model_student.all()
                    
                    if model_student:
                        for student in model_student:
                            
                            model_student = db.session.query(Batch_student).filter_by(batchStudentID=student.batchStudentID).first()
                            if model_student:
                                status = -1
                                if int(model_student.total) >= passing: status = 1
                                model_student.status = status
                                db.session.commit()
                
        else:
            res = status_response(409, 'Batch already exist.')
        
    data["response"] = res
    return jsonify(data)
