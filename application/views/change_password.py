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

view_name = "change_password"

change_password = Blueprint(view_name, __name__)

@change_password.route('/change-password/', methods=['PUT'])
def index():
    
    requests = {
        "opassword": request_form("opassword"), 
        "password": request_form("password"), 
        "cpassword": request_form("cpassword"), 
    }
    
    data = { }
    res = status_response(200)
    
    
    hasError = False
    
    # required fields
    errors = ''
    rFields = {
        'opassword' : 'Old Password', 
        'password'  : 'New Password', 
        'cpassword' : 'Confirm New Password', 
    }   
    for key, value in rFields.items():
        if requests.get(key) == '' or requests.get(key) is None:
            hasError = True
            if errors != '':
                errors += ', '+value
            else:
                errors += value
    if hasError is True: res = status_response(409, 'Required field(s): '+errors)
    # duplicate name
    model_user = User.query.filter(User.userID==session['user']['userID']).first()
    if hasError is False and model_user is not None:
        if not bcrypt.check_password_hash(model_user.password, requests.get("opassword")):
            hasError = True
            res = status_response(401, 'Invalid old password.')
        
    # password does not match
    if hasError is False and requests.get("password") != requests.get("cpassword"):
        hasError = True
        res = status_response(401, 'New password does not match.')
    
    if hasError is False:
        model_user = User.query.filter_by(userID=session['user']['userID']).first()
        if model_user is not None:
            model_user.password = bcrypt.generate_password_hash(requests.get("password")).decode('utf-8')
            db.session.commit()
        else:
            res = status_response(404, 'User not found!')
        
    data["response"] = res
    return jsonify(data)
