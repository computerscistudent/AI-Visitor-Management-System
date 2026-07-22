from datetime import datetime,timezone
from app.database import db

class Visitor(db.Model):
    __tablename__ = 'visitors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False,unique=True)
    photo_path = db.Column(db.String(255),nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    attendances = db.relationship("Attendance",backref="visitor",lazy=True,cascade="all, delete-orphan")

class Attendance(db.Model):
    __tablename__ = 'attendance'

    id = db.Column(db.Integer, primary_key=True)
    visitor_id = db.Column(db.Integer,db.ForeignKey("visitors.id"),nullable=False)
    date = db.Column(db.Date,nullable=False)
    time = db.Column(db.Time,nullable=False)
    created_at = db.Column(db.DateTime,default=lambda: datetime.now(timezone.utc))

    
