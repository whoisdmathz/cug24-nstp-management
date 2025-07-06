from sqlalchemy.dialects.mysql import TINYINT, VARCHAR
from application.services import db

class User_type(db.Model):
    __tablename__ = "user_types"

    userTypeID  = db.Column(TINYINT(unsigned=True), nullable=False, primary_key=True) 
    name        = db.Column(VARCHAR(50), nullable=False) 