from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class CorrespondenceEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_received = db.Column(db.Date)
    sender = db.Column(db.String)
    receiver = db.Column(db.String)
    subject = db.Column(db.String)
    notes = db.Column(db.Text)