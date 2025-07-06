from sqlalchemy.dialects.mysql import TINYINT, SMALLINT, INTEGER, VARCHAR, TEXT, DATETIME, DATE
from application.services import db

class Batch(db.Model):
    __tablename__ = "batches"

    batchID         = db.Column(INTEGER(unsigned=True), nullable=False, primary_key=True) 
    nstpComponentID = db.Column(TINYINT(unsigned=True), db.ForeignKey('nstp_components.nstpComponentID'), nullable=False) 
    userID          = db.Column(INTEGER(unsigned=True), db.ForeignKey('users.userID'), nullable=False) 
    schoolYear      = db.Column(VARCHAR(60), nullable=False) 
    term            = db.Column(TINYINT(30), nullable=False) 
    code            = db.Column(VARCHAR(30), nullable=False) 
    studentCount    = db.Column(SMALLINT(unsigned=True), nullable=False) 
    status          = db.Column(TINYINT, nullable=False) 