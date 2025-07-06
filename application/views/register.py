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

view_name = "register"
view_title = "Register"

register = Blueprint(view_name, __name__)

data = {}

# blueprint function
def register_blueprint(app):
    # constructor
    @register.before_request
    def before_request_func():
        # logout 
        if 'user' in session: 
            module = 'dashboard'
            if session['user']['userTypeID']==1: module = 'dashboard'
            if session['user']['userTypeID']==2: module = 'head-batches'
            if session['user']['userTypeID']==3: module = 'student-home'
            return redirect(url_for(module+'.index'))
        # initialize variable
        data['view'] = view_name
        data['title'] = view_title
        data['subtitle'] = ''

    return register

# starting
@register.route('/'+view_name+'/')
def index():
    data['subtitle'] = ''
    data['courses'] = db.session.query(Course).order_by(Course.code.asc()).all()
    return render_template(view_name.replace("-", "_")+'/index.html', data=data)

# apis 
@register.route('/'+view_name+'/authenticate/', methods=['POST'])
def authenticate():
    
    requests = {
        "username": request_form("username"), 
        "password": request_form("password"), 
        "cpassword": request_form("cpassword"), 
        "fname": request_form("fname"), 
        "mname": request_form("mname"), 
        "lname": request_form("lname"), 
        "ename": request_form("ename"), 
        "birthDate": request_form("birthDate"), 
        "birthPlace": request_form("birthPlace"), 
        "gender": request_form("gender"), 
        "email": request_form("email"), 
        "phone": request_form("phone"), 
        "religion": request_form("religion"), 
        "addressHomeStreet": request_form("addressHomeStreet"), 
        "addressHomeMunicipality": request_form("addressHomeMunicipality"), 
        "addressHomeProvince": request_form("addressHomeProvince"), 
        "citizenship": request_form("citizenship"), 
        "courseID": request_form("courseID"), 
        "yearLevel": request_form("yearLevel"), 
        "emergencyContactName": request_form("emergencyContactName"), 
        "emergencyContactPhone": request_form("emergencyContactPhone"), 
        "emergencyContactRelationship": request_form("emergencyContactRelationship"), 
        "emergencyContactAddress": request_form("emergencyContactAddress"), 
    }
    
    data = {} 
    res = status_response(200) 
    
    hasError = False
        
    # required fields
    errors = ''
    required_fields = {
        'username'                      : 'Username', 
        'password'                      : 'Password', 
        'cpassword'                     : 'Confirm Password', 
        'fname'                         : 'First Name', 
        'lname'                         : 'Last Name', 
        'birthDate'                     : 'Birthday', 
        'gender'                        : 'Gender', 
        'phone'                         : 'Contact Number', 
        'religion'                      : 'Religion', 
        'addressHomeStreet'             : 'Home Address Street/brgy.', 
        'addressHomeMunicipality'       : 'Home Address Municipality', 
        'addressHomeProvince'           : 'Home Address Province', 
        'citizenship'                   : 'Citizenship', 
        'courseID'                      : 'Course', 
        'yearLevel'                     : 'Year Level', 
        'emergencyContactName'          : 'Emergency Contact', 
        'emergencyContactPhone'         : 'Contact Number', 
        'emergencyContactRelationship'  : 'Relationship', 
        'emergencyContactAddress'       : 'Address', 
    }
    for key, value in required_fields.items():
        if requests.get(key) == '' or requests.get(key) is None:
            hasError = True
            if errors != '':
                errors += ', '+value 
            else:
                errors += value 
    if hasError is True: res = status_response(409, errors, 'Required field(s):')
    
    # Username already exist 
    model_user = db.session.query(User)
    model_user = model_user.filter(User.username==requests.get("username"))
    model_user = model_user.first()
    if hasError is False and model_user is not None:
        hasError = True
        res = status_response(409, 'Username already exist.')
    
    # User already exist 
    model_user = db.session.query(User)
    model_user = model_user.filter(User.fname==requests.get("fname"))
    model_user = model_user.filter(User.lname==requests.get("lname"))
    model_user = model_user.filter(User.userTypeID==3)
    model_user = model_user.first()
    if hasError is False and model_user is not None:
        hasError = True
        res = status_response(409, 'User already exist.')
    
    # Password does not match
    if hasError is False and requests.get("password") != requests.get("cpassword"):
        hasError = True
        res = status_response(401, 'Password does not match.')
    
    if hasError is False:
        # insert data
        model_user = User(
            userTypeID = 3, 
            nstpComponentID = 0, 
            courseID = requests.get("courseID"), 
            yearLevel = requests.get("yearLevel"), 
            studentNo = '', 
            username = requests.get("username"), 
            password = bcrypt.generate_password_hash(requests.get("password")).decode('utf-8'), 
            lname = requests.get("lname").upper(), 
            fname = requests.get("fname").upper(), 
            mname = requests.get("mname").upper(), 
            ename = requests.get("ename").upper(), 
            gender = requests.get("gender"), 
            birthDate = requests.get("birthDate"), 
            birthPlace = requests.get("birthPlace"), 
            religion = requests.get("religion"), 
            citizenship = requests.get("citizenship"), 
            phone = requests.get("phone"), 
            email = requests.get("email"), 
            addressHomeStreet = requests.get("addressHomeStreet"), 
            addressHomeMunicipality = requests.get("addressHomeMunicipality"), 
            addressHomeProvince = requests.get("addressHomeProvince"), 
            addressHomePhone = '', 
            addressTemporaryStreet = '', 
            addressTemporaryMunicipality = '', 
            addressTemporaryProvince = '', 
            addressTemporaryPhone = '', 
            fatherName = '', 
            fatherOccupation = '', 
            motherName = '', 
            motherOccupation = '', 
            emergencyContactName = requests.get("emergencyContactName"), 
            emergencyContactPhone = requests.get("emergencyContactPhone"), 
            emergencyContactRelationship = requests.get("emergencyContactRelationship"), 
            emergencyContactAddress = requests.get("emergencyContactAddress"), 
            height = '', 
            weigh = '', 
            complexion = '', 
            bloodTypeID = 0, 
            takeAdvanceCourse = 0, 
            picExt = '', 
            status = 1, 
        )
        db.session.add(model_user)
        db.session.commit()
    
    data["response"] = res
    return jsonify(data) 
