from sqlalchemy.dialects.mysql import TINYINT, SMALLINT, INTEGER, VARCHAR, TEXT, DATETIME
from application.services import db

class Configuration(db.Model):
    __tablename__ = "configurations"

    configurationID = db.Column(INTEGER(unsigned=True), nullable=False, primary_key=True) 
    name            = db.Column(VARCHAR(150), nullable=False) 
    value           = db.Column(TEXT, nullable=False) 
    remarks         = db.Column(TEXT, nullable=False) 
    isShown         = db.Column(TINYINT, nullable=False) 