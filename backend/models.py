from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    """User model for doctors/staff who access the system"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='doctor')  # doctor, admin, etc.
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

class Enrollment(db.Model):
    """Detailed enrollment model instead of using association table"""
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    program_id = db.Column(db.Integer, db.ForeignKey('health_program.id'), nullable=False)
    enrollment_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='active')  # active, completed, suspended
    notes = db.Column(db.Text)
    enrolled_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Relationships
    client = db.relationship('Client', back_populates='enrollments')
    program = db.relationship('HealthProgram', back_populates='enrollments')
    user = db.relationship('User')
    
    def to_dict(self):
        return {
            'id': self.id,
            'client_id': self.client_id,
            'program_id': self.program_id,
            'program_name': self.program.name,
            'enrollment_date': self.enrollment_date.isoformat(),
            'status': self.status,
            'notes': self.notes,
            'enrolled_by': self.enrolled_by
        }

class Client(db.Model):
    __tablename__ = 'client'
    
    id = db.Column(db.Integer, primary_key=True)  # Add this primary key
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    contact_number = db.Column(db.String(20))
    email = db.Column(db.String(100))
    address = db.Column(db.Text)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)
    registered_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Relationships
    enrollments = db.relationship('Enrollment', backref='client', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'gender': self.gender,
            'contact_number': self.contact_number,
            'email': self.email,
            'address': self.address,
            'registered_at': self.registered_at.isoformat() if self.registered_at else None
        }
    
    def to_dict_basic(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name
        }
    
    def to_dict_basic(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
        }

class HealthProgram(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Relationships
    enrollments = db.relationship('Enrollment', back_populates='program', cascade='all, delete-orphan')
    creator = db.relationship('User')
    
    def to_dict(self):
        active_enrollments = [e for e in self.enrollments if e.status == 'active']
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_date': self.created_date.isoformat(),
            'created_by': self.created_by,
            'client_count': len(active_enrollments)
        }
        
    def to_dict_basic(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }