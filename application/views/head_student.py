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

view_name = "head-students"
view_title = "All Students"

head_student = Blueprint(view_name, __name__)

data = {}

# blueprint function
def head_student_blueprint(app):
    # constructor
    @head_student.before_request
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

    return head_student

# pages
@head_student.route('/'+view_name+'/')
def index():
    
    results = db.session.query(User)
    results = results.outerjoin(Course, User.courseID==Course.courseID)
    results = results.outerjoin(Nstp_component, User.nstpComponentID==Nstp_component.nstpComponentID)
    results = results.with_entities(
        User.userID,
        User.lname,
        User.fname,
        User.mname,
        Course.code.label('cCode'),
        User.yearLevel,
        Nstp_component.code.label('ncCode'),
        User.gender,
        User.phone,
    )
    results = results.filter(User.userTypeID==3)
    results = results.filter(User.nstpComponentID==session['user']['nstpComponentID'])
    results = results.order_by(User.lname.asc())
    results = results.order_by(User.fname.asc())
    results = results.all()
    
    data['subtitle'] = ''
    data['results'] = results
    return render_template(view_name.replace("-", "_")+'/index.html', data=data)

@head_student.route('/'+view_name+'/view/<int:id>/')
def view(id):
    
    model_user = db.session.query(User)
    model_user = model_user.outerjoin(Course, User.courseID==Course.courseID)
    model_user = model_user.outerjoin(Nstp_component, User.nstpComponentID==Nstp_component.nstpComponentID)
    model_user = model_user.outerjoin(Blood_type, User.bloodTypeID==Blood_type.bloodTypeID)
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
    model_user = model_user.filter(User.userID==id)
    model_user = model_user.first()
    
    model_terms = db.session.query(Batch_student)
    model_terms = model_terms.outerjoin(Batch, Batch_student.batchID==Batch.batchID)
    model_terms = model_terms.with_entities(
        Batch_student.userID,
        Batch.term,
        Batch.schoolYear,
        Batch_student.attendance,
        Batch_student.exam,
        Batch_student.performance,
        Batch_student.total,
        Batch_student.status,
    )
    model_terms = model_terms.filter(Batch_student.userID==id)
    model_terms = model_terms.order_by(Batch.schoolYear.asc())
    model_terms = model_terms.order_by(Batch.term.asc())
    model_terms = model_terms.all()
    
    data['subtitle'] = 'View'
    data['id'] = id
    data['row'] = model_user
    data['terms'] = model_terms
    return render_template(view_name.replace("-", "_")+'/view.html', data=data)