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

view_name = "users"
view_title = "Users"

user = Blueprint(view_name, __name__)

data = {}

# blueprint function
def user_blueprint(app):
    # constructor
    @user.before_request
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

    return user

# pages
@user.route('/'+view_name+'/')
def index():
    
    results = db.session.query(User)
    results = results.outerjoin(User_type, User.userTypeID==User_type.userTypeID)
    results = results.outerjoin(Nstp_component, User.nstpComponentID==Nstp_component.nstpComponentID)
    results = results.with_entities(
        User.userID,
        User_type.name.label('utName'),
        Nstp_component.code.label('ncCode'),
        User.lname,
        User.fname,
        User.mname,
        User.username,
        User.gender,
        User.phone,
        User.status,
    )
    results = results.filter(User.userTypeID!=3)
    results = results.order_by(User.lname.asc())
    results = results.order_by(User.fname.asc())
    results = results.all()
    
    data['subtitle'] = ''
    data['results'] = results
    return render_template(view_name.replace("-", "_")+'/index.html', data=data)

@user.route('/'+view_name+'/add/')
def add():
    data['subtitle'] = 'Add'
    data['user_types'] = db.session.query(User_type).filter(User_type.userTypeID!=3).order_by(User_type.name.asc()).all()
    data['nstp_components'] = db.session.query(Nstp_component).order_by(Nstp_component.code.asc()).all()
    data['today'] = datetime.datetime.today().strftime('%Y-%m-%d')
    return render_template(view_name.replace("-", "_")+'/add.html', data=data)

@user.route('/'+view_name+'/view/<int:id>/')
def view(id):
    
    item = db.session.query(User)
    item = item.outerjoin(User_type, User.userTypeID==User_type.userTypeID)
    item = item.outerjoin(Nstp_component, User.nstpComponentID==Nstp_component.nstpComponentID)
    item = item.with_entities(
        User.userID,
        User_type.name.label('utName'),
        Nstp_component.code.label('ncCode'),
        User.lname,
        User.fname,
        User.mname,
        User.username,
        User.birthDate,
        User.gender,
        User.phone,
        User.status,
    )
    item = item.filter(User.userID==id)
    item = item.first()
    
    row = {}
    if item:
        row['userID'] = item.userID
        row['utName'] = item.utName
        row['ncCode'] = item.ncCode
        row['lname'] = item.lname
        row['fname'] = item.fname
        row['mname'] = item.mname
        row['username'] = item.username
        row['birthDate'] = item.birthDate.strftime('%m/%d/%Y') if item.birthDate else ''
        row['gender'] = item.gender
        row['phone'] = item.phone
        row['status'] = item.status
    
    data['subtitle'] = 'View'
    data['id'] = id
    data['row'] = row
    data['statuses'] = ['Deactivated', 'Active']
    return render_template(view_name.replace("-", "_")+'/view.html', data=data)

@user.route('/'+view_name+'/edit/<int:id>/')
def edit(id):
    
    item = db.session.query(User)
    item = item.outerjoin(User_type, User.userTypeID==User_type.userTypeID)
    item = item.outerjoin(Nstp_component, User.nstpComponentID==Nstp_component.nstpComponentID)
    item = item.with_entities(
        User.userID,
        User.userTypeID,
        User.nstpComponentID,
        User_type.name.label('utName'),
        Nstp_component.code.label('ncCode'),
        User.lname,
        User.fname,
        User.mname,
        User.username,
        User.birthDate,
        User.gender,
        User.phone,
        User.status,
    )
    item = item.filter(User.userID==id)
    item = item.first()
    
    row = {}
    if item:
        row['userID'] = item.userID
        row['userTypeID'] = item.userTypeID
        row['nstpComponentID'] = item.nstpComponentID
        row['utName'] = item.utName
        row['ncCode'] = item.ncCode
        row['lname'] = item.lname
        row['fname'] = item.fname
        row['mname'] = item.mname
        row['username'] = item.username
        row['birthDate'] = item.birthDate.strftime('%Y-%m-%d') if item.birthDate else None
        row['gender'] = item.gender
        row['phone'] = item.phone
        row['status'] = item.status
    
    data['subtitle'] = 'Edit'
    data['id'] = id
    data['row'] = row
    data['user_types'] = db.session.query(User_type).filter(User_type.userTypeID!=3).order_by(User_type.name.asc()).all()
    data['nstp_components'] = db.session.query(Nstp_component).order_by(Nstp_component.code.asc()).all()
    data['today'] = datetime.datetime.today().strftime('%Y-%m-%d')
    return render_template(view_name.replace("-", "_")+'/edit.html', data=data)

# api 
@user.route('/'+view_name+'/api/', methods=['POST'])
def post():
    
    requests = {
        "userTypeID"        : request_form("userTypeID"), 
        "nstpComponentID"   : request_form("nstpComponentID"), 
        "username"          : request_form("username"), 
        "password"          : request_form("password"), 
        "cpassword"         : request_form("cpassword"), 
        "fname"             : request_form("fname"), 
        "mname"             : request_form("mname"), 
        "lname"             : request_form("lname"), 
        "gender"            : request_form("gender"), 
        "birthDate"         : request_form("birthDate"), 
        "phone"             : request_form("phone"), 
    }
    
    data = {} 
    res = status_response(200) 
    
    hasError = False
        
    # required fields
    errors = ''
    required_fields = {
        'userTypeID'        : 'User Type', 
        'username'          : 'Username', 
        'password'          : 'Password', 
        'cpassword'         : 'Confirm Password', 
        'fname'             : 'First Name', 
        'lname'             : 'Last Name', 
        'gender'            : 'Gender', 
        'birthDate'         : 'Birthday', 
    }
    if int(requests.get('userTypeID'))==2: required_fields['nstpComponentID'] = 'Component'
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
    model_user = model_user.filter(User.userTypeID!=3)
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
            userTypeID = requests.get("userTypeID"), 
            nstpComponentID = requests.get("nstpComponentID") if int(requests.get("userTypeID")) == 2 else 0, 
            courseID = 0, 
            yearLevel = 0, 
            studentNo = '', 
            username = requests.get("username"), 
            password = bcrypt.generate_password_hash(requests.get("password")).decode('utf-8'), 
            lname = requests.get("lname").upper(), 
            fname = requests.get("fname").upper(), 
            mname = requests.get("mname").upper(), 
            ename = '', 
            gender = requests.get("gender"), 
            birthDate = requests.get("birthDate"), 
            birthPlace = '', 
            religion = '', 
            citizenship = '', 
            phone = requests.get("phone"), 
            email = '', 
            addressHomeStreet = '', 
            addressHomeMunicipality = '', 
            addressHomeProvince = '', 
            addressHomePhone = '', 
            addressTemporaryStreet = '', 
            addressTemporaryMunicipality = '', 
            addressTemporaryProvince = '', 
            addressTemporaryPhone = '', 
            fatherName = '', 
            fatherOccupation = '', 
            motherName = '', 
            motherOccupation = '', 
            emergencyContactName = '', 
            emergencyContactPhone = '', 
            emergencyContactRelationship = '', 
            emergencyContactAddress = '', 
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

@user.route('/'+view_name+'/api/<int:id>/', methods=['PUT']) 
def put(id):
    
    requests = {
        "userTypeID"        : request_form("userTypeID"), 
        "nstpComponentID"   : request_form("nstpComponentID"), 
        "password"          : request_form("password"), 
        "cpassword"         : request_form("cpassword"), 
        "fname"             : request_form("fname"), 
        "mname"             : request_form("mname"), 
        "lname"             : request_form("lname"), 
        "gender"            : request_form("gender"), 
        "birthDate"         : request_form("birthDate"), 
        "phone"             : request_form("phone"), 
        "status"            : request_form("status"), 
    }
    
    data = {} 
    res = status_response(200) 
    
    hasError = False
        
    # required fields
    errors = ''
    required_fields = {
        'userTypeID'        : 'User Type', 
        'status'            : 'Status', 
        'fname'             : 'First Name', 
        'lname'             : 'Last Name', 
        'gender'            : 'Gender', 
        'birthDate'         : 'Birthday', 
    }
    if int(requests.get('userTypeID'))==2: required_fields['nstpComponentID'] = 'Component'
    if requests.get('password') or requests.get('cpassword'): 
        required_fields['password'] = 'New Password'
        required_fields['cpassword'] = 'Confirm Password'
    for key, value in required_fields.items():
        if requests.get(key) == '' or requests.get(key) is None:
            hasError = True
            if errors != '':
                errors += ', '+value 
            else:
                errors += value 
    if hasError is True: res = status_response(409, errors, 'Required field(s):')
    
    # User already exist 
    model_user = db.session.query(User)
    model_user = model_user.filter(User.fname==requests.get("fname"))
    model_user = model_user.filter(User.lname==requests.get("lname"))
    model_user = model_user.filter(User.userID!=id)
    model_user = model_user.filter(User.userTypeID!=3)
    model_user = model_user.first()
    if hasError is False and model_user is not None:
        hasError = True
        res = status_response(409, 'User already exist.')
    
    # Password does not match
    if hasError is False and requests.get("password") and requests.get("password") != requests.get("cpassword"):
        hasError = True
        res = status_response(401, 'Password does not match.')
    
    if hasError is False:
        # update data
        model_user = db.session.query(User).filter_by(userID=id).first()
        if model_user: 
            
            nstpComponentID = 0
            if int(requests.get("userTypeID"))!=1: nstpComponentID = requests.get("nstpComponentID") 
            
            model_user.userTypeID = requests.get("userTypeID") 
            model_user.nstpComponentID = nstpComponentID
            model_user.status = requests.get("status") 
            if requests.get("password"): model_user.password = bcrypt.generate_password_hash(requests.get("password")).decode('utf-8') 
            model_user.fname = requests.get("fname") 
            model_user.mname = requests.get("mname") 
            model_user.lname = requests.get("lname") 
            model_user.gender = requests.get("gender") 
            model_user.birthDate = requests.get("birthDate") 
            model_user.phone = requests.get("phone") 
            db.session.commit()
    
    data["response"] = res
    return jsonify(data)
