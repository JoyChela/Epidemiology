from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
import uuid
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize MetaData and SQLAlchemy
metadata = MetaData()
db = SQLAlchemy(metadata=metadata)

class Client(db.Model, SerializerMixin):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(15))
    email = db.Column(db.String(100))
    address = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    # Relationship with programs through enrollments
    enrollments = db.relationship('Enrollment', back_populates='client', cascade='all, delete-orphan')
    
    # SerializerMixin provides the to_dict method, but we'll override it to fit your structure
    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'gender': self.gender,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'programs': [enrollment.program.to_dict() for enrollment in self.enrollments]
        }

class HealthProgram(db.Model, SerializerMixin):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    # Relationship with clients through enrollments
    enrollments = db.relationship('Enrollment', back_populates='program', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Enrollment(db.Model, SerializerMixin):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    client_id = db.Column(db.String(36), db.ForeignKey('client.id'), nullable=False)
    program_id = db.Column(db.String(36), db.ForeignKey('health_program.id'), nullable=False)
    enrollment_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    status = db.Column(db.String(20), default='active')
    
    # Relationships
    client = db.relationship('Client', back_populates='enrollments')
    program = db.relationship('HealthProgram', back_populates='enrollments')
    
    # Add a unique constraint to prevent duplicate enrollments
    __table_args__ = (db.UniqueConstraint('client_id', 'program_id', name='unique_enrollment'),)

class User(db.Model, SerializerMixin):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='doctor')
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
