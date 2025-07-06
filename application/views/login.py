from flask import Blueprint, session, redirect, url_for, render_template, jsonify, session 
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

view_name = "login"
view_title = "Login"

login = Blueprint(view_name, __name__)

data = {}

# blueprint function
def login_blueprint(app):
    # constructor
    @login.before_request
    def before_request_func():
        # logout 
        if 'user' in session: 
            module = 'dashboard'
            print(session['user'])
            if session['user']['userTypeID']==1: module = 'dashboard'
            if session['user']['userTypeID']==2: module = 'head-batches'
            if session['user']['userTypeID']==3: module = 'student-home'
            return redirect(url_for(module+'.index'))
        # initialize variable
        data['view'] = view_name
        data['title'] = view_title
        data['subtitle'] = ''

    return login

# starting
@login.route('/')
def welcome():
    return redirect(url_for('login.index'))

# pages
@login.route('/'+view_name+'/')
def index():
    data['subtitle'] = ''
    return render_template(view_name.replace("-", "_")+'/index.html', data=data)

# apis 
@login.route('/'+view_name+'/authenticate/', methods=['POST'])
def authenticate():
    
    requests = {
        "username": request_form("username"), 
        "password": request_form("password"), 
    }
    
    data = {}
    res = status_response(200)
    module = 'dashboard'
    
    if requests.get("username") and requests.get("password"):
        user = User.query.filter_by(username=requests.get("username")).first()
        if user and bcrypt.check_password_hash(user.password, requests.get("password")):
            
            model_component = db.session.query(Nstp_component)
            model_component = model_component.filter_by(nstpComponentID=user.nstpComponentID)
            model_component = model_component.first()
            
            component = ''
            if model_component:
                component = model_component.code
            
            userDetails = {
                'userID': user.userID, 
                'userTypeID': user.userTypeID, 
                'lname': user.lname, 
                'fname': user.fname, 
                'mname': user.mname, 
                'nstpComponentID': user.nstpComponentID, 
                'component': component, 
            }
            session['user'] = userDetails
            if user.userTypeID==1 : module = 'dashboard'
            if user.userTypeID==2 : module = 'head-batches'
            if user.userTypeID==3 : module = 'student-home'
        else:
            res = status_response(401, "Incorrect username or password.")
    else:
        res = status_response(400, "Please fill all fields.")
    
    data["module"] = module
    data["response"] = res
    return jsonify(data)
