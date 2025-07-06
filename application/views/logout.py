from flask import Blueprint, redirect, url_for, render_template, jsonify, session
from sqlalchemy import select
from flask_restful import request

import flask
import datetime
import random

from application.services import db, bcrypt
from application.libraries.status_response import status_response
from application.libraries.request_input import request_header, request_form, request_arg

view_name = "logout"

logout = Blueprint(view_name, __name__)

@logout.route('/'+view_name+'/')
def index():
    session.pop('user', None)
    return redirect(url_for('login.index'))
