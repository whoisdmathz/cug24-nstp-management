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

view_name = "dashboard"
view_title = "Dashboard"

dashboard = Blueprint(view_name, __name__)

data = {}

# blueprint function
def dashboard_blueprint(app):
    # constructor
    @dashboard.before_request
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

    return dashboard

# pages
@dashboard.route('/'+view_name+'/')
def index():
    
    count_cwts  = db.session.query(User).filter(User.userTypeID==3, User.nstpComponentID==1).count()
    count_lts   = db.session.query(User).filter(User.userTypeID==3, User.nstpComponentID==2).count()
    count_rotc  = db.session.query(User).filter(User.userTypeID==3, User.nstpComponentID==3).count()
    
    total_student   = count_cwts+count_lts+count_rotc
    
    data['subtitle'] = ''
    data['count_cwts']      = count_cwts 
    data['count_lts']       = count_lts 
    data['count_rotc']      = count_rotc 
    data['total_student']   = total_student 
    data['percent_cwts']    = round((count_cwts/total_student)*100, 1) if total_student!=0 else 0
    data['percent_lts']     = round((count_lts/total_student)*100, 1) if total_student!=0 else 0
    data['percent_rotc']    = round((count_rotc/total_student)*100, 1) if total_student!=0 else 0
    return render_template(view_name.replace("-", "_")+'/index.html', data=data)

# apis 
