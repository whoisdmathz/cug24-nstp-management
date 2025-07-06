from sqlalchemy.dialects.mysql import TINYINT, SMALLINT, INTEGER, VARCHAR, TEXT, DATETIME, DATE
from application.services import db

class Batch_student(db.Model):
    __tablename__ = "batch_students"

    batchStudentID  = db.Column(INTEGER(unsigned=True), nullable=False, primary_key=True) 
    batchID         = db.Column(INTEGER(unsigned=True), db.ForeignKey('batches.batchID'), nullable=False) 
    userID          = db.Column(INTEGER(unsigned=True), db.ForeignKey('users.userID'), nullable=False) 
    attendance      = db.Column(TINYINT, nullable=False) 
    exam            = db.Column(TINYINT, nullable=False) 
    performance     = db.Column(TINYINT, nullable=False) 
    total           = db.Column(TINYINT, nullable=False) 
    status          = db.Column(TINYINT, nullable=False) 