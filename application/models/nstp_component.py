from sqlalchemy.dialects.mysql import TINYINT, SMALLINT, INTEGER, VARCHAR, TEXT, DATETIME, DATE
from application.services import db

class Nstp_component(db.Model):
    __tablename__ = "nstp_components"

    nstpComponentID = db.Column(TINYINT(unsigned=True), nullable=False, primary_key=True) 
    code            = db.Column(VARCHAR(4), nullable=False) 
    description     = db.Column(TEXT, nullable=False) 