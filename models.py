from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class CorrespondenceEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_received = db.Column(db.Date, nullable=False)
    sender = db.Column(db.String(255))    # Od kogo
    receiver = db.Column(db.String(255))  # Do kogo
    subject = db.Column(db.String(255), nullable=False)
    notes = db.Column(db.Text)
    reference_number = db.Column(db.String(50))  
    direction = db.Column(db.String(10), nullable=False)  