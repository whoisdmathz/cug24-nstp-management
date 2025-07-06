from sqlalchemy.dialects.mysql import TINYINT, SMALLINT, INTEGER, VARCHAR, TEXT, DATETIME, DATE
from application.services import db

class Blood_type(db.Model):
    __tablename__ = "blood_types"

    bloodTypeID = db.Column(TINYINT(unsigned=True), nullable=False, primary_key=True) 
    name        = db.Column(VARCHAR(5), nullable=False) 