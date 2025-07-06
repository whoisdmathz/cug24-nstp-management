from sqlalchemy.dialects.mysql import TINYINT, SMALLINT, INTEGER, VARCHAR, TEXT, DATETIME, DATE
from application.services import db

class Course(db.Model):
    __tablename__ = "courses"

    courseID    = db.Column(TINYINT(unsigned=True), nullable=False, primary_key=True) 
    code        = db.Column(VARCHAR(15), nullable=False) 
    description = db.Column(TEXT, nullable=False) 