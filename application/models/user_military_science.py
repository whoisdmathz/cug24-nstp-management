from sqlalchemy.dialects.mysql import TINYINT, SMALLINT, INTEGER, VARCHAR, TEXT, DATETIME, DATE
from application.services import db

class User_military_science(db.Model):
    __tablename__ = "user_military_sciences"

    userMilitaryScienceID   = db.Column(INTEGER(unsigned=True), nullable=False, primary_key=True) 
    userID                  = db.Column(INTEGER(unsigned=True), db.ForeignKey('users.userID'), nullable=False) 
    ms                      = db.Column(TEXT, nullable=False) 
    semester                = db.Column(TINYINT, nullable=False) 
    schoolYear              = db.Column(TEXT, nullable=False) 
    grade                   = db.Column(TINYINT, nullable=False) 
    remarks                 = db.Column(TEXT, nullable=False) 