from sqlalchemy.dialects.mysql import TINYINT, SMALLINT, INTEGER, VARCHAR, TEXT, DATETIME, DATE
from application.services import db

class Batch_attendance(db.Model):
    __tablename__ = "batch_attendances"

    batchAttendanceID   = db.Column(INTEGER(unsigned=True), nullable=False, primary_key=True) 
    batchID             = db.Column(INTEGER(unsigned=True), db.ForeignKey('batches.batchID'), nullable=False) 
    date                = db.Column(DATE, nullable=True) 
    dateInserted        = db.Column(DATETIME, nullable=True) 