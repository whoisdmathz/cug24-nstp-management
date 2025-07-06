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

view_name = "courses"
view_title = "Courses"

course = Blueprint(view_name, __name__)

data = {}

# blueprint function
def course_blueprint(app):
    # constructor
    @course.before_request
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

    return course

# pages
@course.route('/'+view_name+'/')
def index():
    
    results = db.session.query(Course)
    results = results.order_by(Course.code.asc())
    results = results.all() 
    
    data['subtitle'] = ''
    data['results'] = results
    return render_template(view_name.replace("-", "_")+'/index.html', data=data)

@course.route('/'+view_name+'/add/')
def add():
    data['subtitle'] = 'Add'
    return render_template(view_name.replace("-", "_")+'/add.html', data=data)

@course.route('/'+view_name+'/view/<int:id>/')
def view(id):
    
    row = db.session.query(Course)
    row = row.filter(Course.courseID==id)
    row = row.first() 
    
    data['subtitle'] = 'View'
    data['id'] = id
    data['row'] = row
    return render_template(view_name.replace("-", "_")+'/view.html', data=data)

@course.route('/'+view_name+'/edit/<int:id>/')
def edit(id):
    
    row = db.session.query(Course)
    row = row.filter(Course.courseID==id)
    row = row.first() 
    
    data['subtitle'] = 'Edit'
    data['id'] = id
    data['row'] = row
    return render_template(view_name.replace("-", "_")+'/edit.html', data=data)

# api 
@course.route('/'+view_name+'/api/', methods=['POST'])
def post():
    
    requests = {
        "code"          : request_form("code"), 
        "description"   : request_form("description"), 
    }
    
    data = {} 
    res = status_response(200) 
    
    hasError = False
        
    # required fields
    errors = ''
    required_fields = {
        'code' : 'Course Code', 
    }
    for key, value in required_fields.items():
        if requests.get(key) == '' or requests.get(key) is None:
            hasError = True
            if errors != '':
                errors += ', '+value 
            else:
                errors += value 
    if hasError is True: res = status_response(409, errors, 'Required field(s):')
    
    # already exist 
    model_course = Course.query.filter_by(code=requests.get("code")).first()
    if hasError is False and model_course is not None:
        hasError = True
        res = status_response(409, 'Course code already exist.')
    
    if hasError is False:
        # insert data
        model_course = Course(
            code = requests.get("code"), 
            description = requests.get("description"), 
        )
        db.session.add(model_course)
        db.session.commit()
    
    data["response"] = res
    return jsonify(data) 

@course.route('/'+view_name+'/api/<int:id>/', methods=['PUT']) 
def put(id):
    
    requests = {
        "code"          : request_form("code"), 
        "description"   : request_form("description"), 
    }
    
    data = {} 
    res = status_response(200) 
    
    hasError = False
        
    # required fields
    errors = ''
    required_fields = {
        'code' : 'Course Code', 
    }
    for key, value in required_fields.items():
        if requests.get(key) == '' or requests.get(key) is None:
            hasError = True
            if errors != '':
                errors += ', '+value 
            else:
                errors += value 
    if hasError is True: res = status_response(409, errors, 'Required field(s):')
    
    # already exist 
    model_course = Course.query.filter(Course.code==requests.get("code"), Course.courseID!=id).first()
    if hasError is False and model_course is not None:
        hasError = True
        res = status_response(409, 'Course code already exist.')
    
    if hasError is False:
        # update data
        model_course = Course.query.filter_by(courseID=id).first() 
        if model_course is not None: 
            model_course.code = requests.get("code") 
            model_course.description = requests.get("description") 
            db.session.commit()
    
    data["response"] = res
    return jsonify(data)
