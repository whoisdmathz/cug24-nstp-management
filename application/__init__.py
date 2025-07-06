import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from application.services import db, bcrypt

from application.views.register import register_blueprint
from application.views.login import login_blueprint
from application.views.change_password import change_password
from application.views.logout import logout
from application.views.dashboard import dashboard_blueprint
from application.views.batch import batch_blueprint
from application.views.profile import profile_blueprint
from application.views.student import student_blueprint
from application.views.course import course_blueprint
from application.views.user import user_blueprint
from application.views.head_batch import head_batch_blueprint
from application.views.head_student import head_student_blueprint
from application.views.student_home import student_home_blueprint

DB_SERVER   = "localhost"
DB_PORT     = "3306"
DB_USERNAME = "root"
DB_PASSWORD = ""
DB_NAME     = "thesis_2024_nstp"

def create_app():
    app = Flask(__name__)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'NSTP'
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}'
    # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
    db.init_app(app)
    bcrypt.init_app(app)
    
    app.register_blueprint(register_blueprint(app))
    app.register_blueprint(login_blueprint(app))
    app.register_blueprint(change_password)
    app.register_blueprint(logout)
    app.register_blueprint(dashboard_blueprint(app))
    app.register_blueprint(batch_blueprint(app))
    app.register_blueprint(student_blueprint(app))
    app.register_blueprint(course_blueprint(app))
    app.register_blueprint(user_blueprint(app))
    app.register_blueprint(head_batch_blueprint(app))
    app.register_blueprint(head_student_blueprint(app))
    app.register_blueprint(profile_blueprint(app))
    app.register_blueprint(student_home_blueprint(app))

    return app

app = create_app()
if __name__ == '__main__':
    app.run(debug=True)