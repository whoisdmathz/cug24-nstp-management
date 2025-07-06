from sqlalchemy.dialects.mysql import TINYINT, SMALLINT, INTEGER, VARCHAR, TEXT, DATETIME, DATE
from application.services import db

class Batch_attendance_log(db.Model):
    __tablename__ = "batch_attendance_logs"

    batchAttendanceLogID    = db.Column(INTEGER(unsigned=True), nullable=False, primary_key=True) 
    batchAttendanceID       = db.Column(INTEGER(unsigned=True), db.ForeignKey('batch_attendances.batchAttendanceID'), nullable=False) 
    batchStudentID          = db.Column(INTEGER(unsigned=True), db.ForeignKey('batch_students.batchStudentID'), nullable=False) 