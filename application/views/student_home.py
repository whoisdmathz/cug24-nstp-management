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

view_name = "student-home"
view_title = "Home"

student_home = Blueprint(view_name, __name__)

data = {}

# blueprint function
def student_home_blueprint(app):
    # constructor
    @student_home.before_request
    def before_request_func():
        # logout 
        if 'user' in session: 
            if session['user']['userTypeID']!=3: return redirect(url_for('logout.index'))
        else:
            return redirect(url_for('logout.index'))
            
        # initialize variable
        data['view'] = view_name
        data['title'] = view_title
        data['subtitle'] = ''

    return student_home

# pages
@student_home.route('/'+view_name+'/')
def index():
    
    model_user = db.session.query(User)
    model_user = model_user.outerjoin(Nstp_component, User.nstpComponentID==Nstp_component.nstpComponentID)
    model_user = model_user.with_entities(
        User.userID,
        User.nstpComponentID,
        User.fatherName,
        Nstp_component.code.label('nstpCode'),
        Nstp_component.description.label('nstpDescription'),
    )
    model_user = model_user.filter(User.userID==session['user']['userID'])
    model_user = model_user.first()
    
    row = {}
    if model_user:
        
        term_first  = []
        term_first_passed_or_ongoing = 0
        is_second_term = 0
        term_second = []
        term_second_passed_or_ongoing = 0
        is_done = 0
        
        # first term 
        model_first_term = db.session.query(Batch_student)
        model_first_term = model_first_term.outerjoin(Batch, Batch_student.batchID==Batch.batchID)
        model_first_term = model_first_term.with_entities(
            Batch_student.batchStudentID,
            Batch_student.total,
            Batch.schoolYear,
            Batch_student.status,
        )
        model_first_term = model_first_term.filter(Batch_student.userID==session['user']['userID'])
        model_first_term = model_first_term.filter(Batch.term==1)
        model_first_term = model_first_term.order_by(Batch_student.batchStudentID.asc())
        model_first_term = model_first_term.all()
        
        if model_first_term:
            for first_term in model_first_term:
                if int(first_term.status)==1: 
                    is_second_term = 1
                    term_first_passed_or_ongoing = 1
                if int(first_term.status)==0: 
                    term_first_passed_or_ongoing = 1
                    
                icon = 'x'
                if int(first_term.status)==0: icon = 'loader'
                if int(first_term.status)==1: icon = 'check'
                
                bgs = ['danger', 'info', 'success']
                statuses = ['Failed', 'On Going', 'Passed']
                term_first.append({
                    'Batch_student': first_term.batchStudentID, 
                    'icon': icon, 
                    'total': first_term.total, 
                    'schoolYear': first_term.schoolYear, 
                    'bg': bgs[int(first_term.status)+1], 
                    'status': statuses[int(first_term.status)+1], 
                })
        
        # second term 
        model_second_term = db.session.query(Batch_student)
        model_second_term = model_second_term.outerjoin(Batch, Batch_student.batchID==Batch.batchID)
        model_second_term = model_second_term.with_entities(
            Batch_student.batchStudentID,
            Batch_student.total,
            Batch.schoolYear,
            Batch_student.status,
        )
        model_second_term = model_second_term.filter(Batch_student.userID==session['user']['userID'])
        model_second_term = model_second_term.filter(Batch.term==2)
        model_second_term = model_second_term.order_by(Batch_student.batchStudentID.asc())
        model_second_term = model_second_term.all()
        
        if model_second_term:
            for second_term in model_second_term:
                if int(second_term.status)==1: 
                    is_done = 1
                    term_second_passed_or_ongoing = 1
                if int(second_term.status)==0: 
                    term_second_passed_or_ongoing = 1
                    
                icon = 'x'
                if int(second_term.status)==0: icon = 'loader'
                if int(second_term.status)==1: icon = 'check'
                
                bgs = ['danger', 'info', 'success']
                statuses = ['Failed', 'On Going', 'Passed']
                
                term_second.append({
                    'Batch_student': second_term.batchStudentID, 
                    'icon': icon, 
                    'total': second_term.total, 
                    'schoolYear': second_term.schoolYear, 
                    'bg': bgs[int(second_term.status)+1], 
                    'status': statuses[int(second_term.status)+1],
                })
                
        
        row['nstpComponentID'] = model_user.nstpComponentID
        row['fatherName'] = model_user.fatherName
        row['nstpCode'] = model_user.nstpCode
        row['nstpDescription'] = model_user.nstpDescription
        
        row['userID'] = model_user.userID
        row['term_first'] = term_first
        row['term_first_passed_or_ongoing'] = term_first_passed_or_ongoing
        row['is_second_term'] = is_second_term
        row['term_second'] = term_second
        row['term_second_passed_or_ongoing'] = term_second_passed_or_ongoing
        row['is_done'] = is_done
    
    data['subtitle'] = ''
    data['row'] = row
    data['blood_types'] = db.session.query(Blood_type).all()
    return render_template(view_name.replace("-", "_")+'/index.html', data=data)

# api 
@student_home.route('/'+view_name+'/update-component/', methods=['POST'])
def update_component():
    
    requests = {
        "nstpComponentID" : request_form("nstpComponentID"), 
    }
    
    data = {} 
    res = status_response(200) 
    
    hasError = False
        
    # required fields
    errors = ''
    required_fields = {
        'nstpComponentID' : 'Component', 
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
        # update data
        model_user = db.session.query(User).filter_by(userID=session['user']['userID']).first()
        if model_user: 
            model_user.nstpComponentID = requests.get('nstpComponentID')
            if int(requests.get('nstpComponentID')) != 3: model_user.fatherName = '.'
            db.session.commit()
    
    data["response"] = res
    return jsonify(data) 

@student_home.route('/'+view_name+'/rotc-registration/', methods=['POST'])
def rotc_registration():
    
    requests = {
        "studentNo": request_form("studentNo"), 
        "addressTemporaryStreet": request_form("addressTemporaryStreet"), 
        "addressTemporaryMunicipality": request_form("addressTemporaryMunicipality"), 
        "addressTemporaryProvince": request_form("addressTemporaryProvince"), 
        "addressTemporaryPhone": request_form("addressTemporaryPhone"), 
        "addressHomeStreet": request_form("addressHomeStreet"), 
        "addressHomeMunicipality": request_form("addressHomeMunicipality"), 
        "addressHomeProvince": request_form("addressHomeProvince"), 
        "addressHomePhone": request_form("addressHomePhone"), 
        "height": request_form("height"), 
        "weigh": request_form("weigh"), 
        "complexion": request_form("complexion"), 
        "bloodTypeID": request_form("bloodTypeID"), 
        "fatherName": request_form("fatherName"), 
        "fatherOccupation": request_form("fatherOccupation"), 
        "motherName": request_form("motherName"), 
        "motherOccupation": request_form("motherOccupation"), 
        "takeAdvanceCourse": 1 if request_form("takeAdvanceCourse") else 0, 
    }
    
    userID = session['user']['userID']
    
    data = { }
    res = status_response(200)
    
    hasError = False
    
    # required fields
    errors = ''
    rFields = {
        'studentNo'        : 'Student Number', 
        'addressTemporaryStreet'        : 'Temporary Address Street/Brgy.', 
        'addressTemporaryMunicipality'  : 'Temporary Address Municipality', 
        'addressTemporaryProvince'      : 'Temporary Address Province', 
        'addressTemporaryPhone'         : 'Temporary Address Phone', 
        'addressHomeStreet'             : 'Home Address Street/Brgy.', 
        'addressHomeMunicipality'       : 'Home Address Municipality', 
        'addressHomeProvince'           : 'Home Address Province', 
        'addressHomePhone'              : 'Home Address Phone', 
        'height'                        : 'Height', 
        'weigh'                         : 'Weigh', 
        'complexion'                    : 'Complexion', 
        'bloodTypeID'                   : 'Blood Type', 
        'fatherName'                    : 'Father Name', 
        'fatherOccupation'              : 'Father Occupation', 
        'motherName'                    : 'Mother Name', 
        'motherOccupation'              : 'Mother Occupation', 
    }
    for key, value in rFields.items():
        if requests.get(key) is '' or requests.get(key) is None:
            hasError = True
            if errors is not '':
                errors += ', '+value
            else:
                errors += value
    if hasError is True: res = status_response(409, errors, 'Required field(s):')
    
    
    if hasError is False:
        model_user = db.session.query(User).filter_by(userID=userID).first()
        if model_user is not None:
            model_user.studentNo = requests.get("studentNo")
            model_user.addressTemporaryStreet = requests.get("addressTemporaryStreet")
            model_user.addressTemporaryMunicipality = requests.get("addressTemporaryMunicipality")
            model_user.addressTemporaryProvince = requests.get("addressTemporaryProvince")
            model_user.addressTemporaryPhone = requests.get("addressTemporaryPhone")
            model_user.addressHomeStreet = requests.get("addressHomeStreet")
            model_user.addressHomeMunicipality = requests.get("addressHomeMunicipality")
            model_user.addressHomeProvince = requests.get("addressHomeProvince")
            model_user.addressHomePhone = requests.get("addressHomePhone")
            model_user.height = requests.get("height")
            model_user.weigh = requests.get("weigh")
            model_user.complexion = requests.get("complexion")
            model_user.bloodTypeID = requests.get("bloodTypeID")
            model_user.fatherName = requests.get("fatherName")
            model_user.fatherOccupation = requests.get("fatherOccupation")
            model_user.motherName = requests.get("motherName")
            model_user.motherOccupation = requests.get("motherOccupation")
            model_user.takeAdvanceCourse = requests.get("takeAdvanceCourse")
            db.session.commit()
        
    data["response"] = res
    return jsonify(data)

@student_home.route('/'+view_name+'/edit-profile/', methods=['GET'])
def edit_profile():
    
    data = {} 
    res = status_response(200) 
    
    model_user = db.session.query(User).filter_by(userID=session['user']['userID']).first()
    
    row = {}
    if model_user:
        
        pass
    
    data["response"] = res
    data["row"] = row
    return jsonify(data) 

@student_home.route('/'+view_name+'/insert-term-first/', methods=['POST'])
def insert_term_first():
    
    requests = {
        "nstpComponentID" : request_form("nstpComponentID"), 
        "code" : request_form("code"), 
    }
    
    data = {} 
    res = status_response(200) 
    
    hasError = False
        
    # required fields
    errors = ''
    required_fields = {
        'code' : 'Term code', 
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
        
        model_batch = db.session.query(Batch)
        model_batch = model_batch.filter(Batch.code==requests.get('code'))
        model_batch = model_batch.filter(Batch.term==1)
        model_batch = model_batch.filter(Batch.nstpComponentID==requests.get('nstpComponentID'))
        model_batch = model_batch.filter(Batch.status==0)
        model_batch = model_batch.first()
        
        if model_batch:
            
            batchID = model_batch.batchID
            
            model_batch_student = db.session.query(Batch_student)
            model_batch_student = model_batch_student.filter(Batch_student.batchID==batchID)
            model_batch_student = model_batch_student.filter(Batch_student.userID==session['user']['userID'])
            model_batch_student = model_batch_student.first()
            
            if model_batch_student is None:
                # insert data
                model_student = Batch_student(
                    batchID = batchID, 
                    userID = session['user']['userID'], 
                    attendance = 0, 
                    exam = 0, 
                    performance = 0, 
                    total = 0, 
                    status = 0, 
                )
                db.session.add(model_student)
                db.session.commit()
                
                studentCount = db.session.query(Batch_student).filter_by(batchID=batchID).count()
                
                # update batch student count 
                model_batch = db.session.query(Batch).filter_by(batchID=batchID).first()
                if model_batch: 
                    model_batch.studentCount = studentCount
                    db.session.commit()
                
        else:
            res = status_response(401, 'Invalid code.')
        
    data["response"] = res
    return jsonify(data) 

@student_home.route('/'+view_name+'/insert-term-second/', methods=['POST'])
def insert_term_second():
    
    requests = {
        "nstpComponentID" : request_form("nstpComponentID"), 
        "code" : request_form("code"), 
    }
    
    data = {} 
    res = status_response(200) 
    
    hasError = False
        
    # required fields
    errors = ''
    required_fields = {
        'code' : 'Term code', 
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
        
        model_batch = db.session.query(Batch)
        model_batch = model_batch.filter(Batch.code==requests.get('code'))
        model_batch = model_batch.filter(Batch.term==2)
        model_batch = model_batch.filter(Batch.nstpComponentID==requests.get('nstpComponentID'))
        model_batch = model_batch.filter(Batch.status==0)
        model_batch = model_batch.first()
        
        if model_batch:
            
            batchID = model_batch.batchID
            
            model_batch_student = db.session.query(Batch_student)
            model_batch_student = model_batch_student.filter(Batch_student.batchID==batchID)
            model_batch_student = model_batch_student.filter(Batch_student.userID==session['user']['userID'])
            model_batch_student = model_batch_student.first()
            
            if model_batch_student is None:
                # insert data
                model_student = Batch_student(
                    batchID = batchID, 
                    userID = session['user']['userID'], 
                    attendance = 0, 
                    exam = 0, 
                    performance = 0, 
                    total = 0, 
                    status = 0, 
                )
                db.session.add(model_student)
                db.session.commit()
        else:
            res = status_response(401, 'Invalid code.')
        
    data["response"] = res
    return jsonify(data) 
