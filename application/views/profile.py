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

view_name = "profile"
view_title = "Profile"

profile = Blueprint(view_name, __name__)

data = {}

# blueprint function
def profile_blueprint(app):
    # constructor
    @profile.before_request
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

    return profile

# pages
@profile.route('/'+view_name+'/')
def index():
    
    model_user = db.session.query(User)
    model_user = model_user.filter(User.userID==session['user']['userID'])
    model_user = model_user.first()
    
    data['subtitle'] = 'Edit'
    data['row'] = model_user
    data['courses'] = db.session.query(Course).all()
    data['blood_types'] = db.session.query(Blood_type).all()
    return render_template(view_name.replace("-", "_")+'/index.html', data=data)

# api 

@profile.route('/'+view_name+'/api/<int:userID>/', methods=['PUT'])
def put(userID):
    requests = {
        "nstpComponentID": request_form("nstpComponentID"), 
        "studentNo": request_form("studentNo"), 
        "courseID": request_form("courseID"), 
        "yearLevel": request_form("yearLevel"), 
        "fname": request_form("fname"), 
        "mname": request_form("mname"), 
        "lname": request_form("lname"), 
        "ename": request_form("ename"), 
        "citizenship": request_form("citizenship"), 
        "birthDate": request_form("birthDate"), 
        "birthPlace": request_form("birthPlace"), 
        "gender": request_form("gender"), 
        "email": request_form("email"), 
        "phone": request_form("phone"), 
        "religion": request_form("religion"), 
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
        "emergencyContactName": request_form("emergencyContactName"), 
        "emergencyContactPhone": request_form("emergencyContactPhone"), 
        "emergencyContactRelationship": request_form("emergencyContactRelationship"), 
        "emergencyContactAddress": request_form("emergencyContactAddress"), 
    }
    
    data = { }
    res = status_response(200)
    
    hasError = False
    
    # required fields
    errors = ''
    rFields = {
        'courseID'                      : 'Course', 
        'yearLevel'                     : 'Year Level', 
        'fname'                         : 'First Name', 
        'lname'                         : 'Last Name', 
        'citizenship'                   : 'Citizenship', 
        'birthDate'                     : 'Birthday', 
        'gender'                        : 'Gender', 
        'phone'                         : 'Contact Number', 
        'religion'                      : 'Religion', 
        'addressHomeStreet'             : 'Home Address Street/Brgy.', 
        'addressHomeMunicipality'       : 'Home Address Municipality', 
        'addressHomeProvince'           : 'Home Address Province', 
        'addressHomePhone'              : 'Home Address Phone', 
        'emergencyContactName'          : 'Emergency Contact', 
        'emergencyContactPhone'         : 'Emergency Phone', 
        'emergencyContactRelationship'  : 'Emergency Relationship', 
        'emergencyContactAddress'       : 'Emergency Address', 
    }
    if int(requests.get('nstpComponentID')) == 3:
        rFields['studentNo']                    = 'Student Number'
        rFields['addressTemporaryStreet']       = 'Temporary Address Street/Brgy.'
        rFields['addressTemporaryMunicipality'] = 'Temporary Address Municipality'
        rFields['addressTemporaryProvince']     = 'Temporary Address Province'
        rFields['addressTemporaryPhone']        = 'Temporary Address Phone'
        rFields['weigh']                        = 'Weight'
        rFields['height']                       = 'Height'
        rFields['complexion']                   = 'Complexion'
        rFields['bloodTypeID']                  = 'Blood Type'
        rFields['fatherName']                   = 'Father Name'
        rFields['fatherOccupation']             = 'Father Occupation'
        rFields['motherName']                   = 'Mother Name'
        rFields['motherOccupation']             = 'Mother Occupation'
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
            model_user.courseID = requests.get("courseID")
            model_user.yearLevel = requests.get("yearLevel")
            model_user.fname = requests.get("fname")
            model_user.mname = requests.get("mname")
            model_user.lname = requests.get("lname")
            model_user.ename = requests.get("ename")
            model_user.citizenship = requests.get("citizenship")
            model_user.birthDate = requests.get("birthDate")
            model_user.birthPlace = requests.get("birthPlace")
            model_user.gender = requests.get("gender")
            model_user.email = requests.get("email")
            model_user.phone = requests.get("phone")
            model_user.religion = requests.get("religion")
            model_user.addressHomeStreet = requests.get("addressHomeStreet")
            model_user.addressHomeMunicipality = requests.get("addressHomeMunicipality")
            model_user.addressHomeProvince = requests.get("addressHomeProvince")
            model_user.addressHomePhone = requests.get("addressHomePhone")
            model_user.emergencyContactName = requests.get("emergencyContactName")
            model_user.emergencyContactPhone = requests.get("emergencyContactPhone")
            model_user.emergencyContactRelationship = requests.get("emergencyContactRelationship")
            model_user.emergencyContactAddress = requests.get("emergencyContactAddress")
            
            if int(requests.get('nstpComponentID'))==3:
                model_user.addressTemporaryStreet = requests.get("addressTemporaryStreet")
                model_user.addressTemporaryMunicipality = requests.get("addressTemporaryMunicipality")
                model_user.addressTemporaryProvince = requests.get("addressTemporaryProvince")
                model_user.addressTemporaryPhone = requests.get("addressTemporaryPhone")
                model_user.fatherName = requests.get("fatherName")
                model_user.fatherOccupation = requests.get("fatherOccupation")
                model_user.motherName = requests.get("motherName")
                model_user.motherOccupation = requests.get("motherOccupation")
                model_user.height = requests.get("height")
                model_user.weigh = requests.get("weigh")
                model_user.complexion = requests.get("complexion")
                model_user.bloodTypeID = requests.get("bloodTypeID")
            db.session.commit()
        
    data["response"] = res
    return jsonify(data)
