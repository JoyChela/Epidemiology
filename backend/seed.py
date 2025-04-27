from datetime import datetime, timedelta
import random
import os
from app import create_app
from models import db, Client, HealthProgram, User, Enrollment

def seed_database():
    """Seed the database with sample data for testing"""
    print("Seeding database...")
    
    # Create users (doctors and admin)
    users = [
        {
            'username': 'admin',
            'email': 'admin@healthsystem.com',
            'password': 'admin123',
            'first_name': 'Admin',
            'last_name': 'User',
            'role': 'admin'
        },
        {
            'username': 'doctor1',
            'email': 'doctor1@healthsystem.com',
            'password': 'doctor123',
            'first_name': 'John',
            'last_name': 'Doe',
            'role': 'doctor'
        },
        {
            'username': 'doctor2',
            'email': 'doctor2@healthsystem.com',
            'password': 'doctor123',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'role': 'doctor'
        }
    ]
    
    created_users = []
    for user_data in users:
        password = user_data.pop('password')
        user = User(**user_data)
        user.set_password(password)
        db.session.add(user)
        created_users.append(user)
    
    db.session.commit()
    print(f"Added {len(users)} users")
    
    # Create health programs
    programs = [
        {'name': 'Tuberculosis Control', 'description': 'Comprehensive TB prevention and treatment program'},
        {'name': 'Malaria Prevention', 'description': 'Program focused on malaria prevention and early treatment'},
        {'name': 'HIV/AIDS Care', 'description': 'HIV testing, treatment, and support services'},
        {'name': 'Diabetes Management', 'description': 'Monitoring and management services for diabetes patients'},
        {'name': 'Maternal Health', 'description': 'Prenatal and postnatal care for expectant mothers'}
    ]
    
    created_programs = []
    admin_user = User.query.filter_by(username='admin').first()
    
    for program_data in programs:
        program = HealthProgram(
            **program_data,
            created_by=admin_user.id if admin_user else None
        )
        db.session.add(program)
        created_programs.append(program)
    
    db.session.commit()
    print(f"Added {len(programs)} health programs")
    
    # Create sample clients
    first_names = ['John', 'Jane', 'Michael', 'Sarah', 'David', 'Lisa', 'Robert', 'Emily', 'James', 'Maria']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']
    genders = ['Male', 'Female']
    
    created_clients = []
    doctor_user = User.query.filter_by(username='doctor1').first()
    
    # Create 20 random clients
    for i in range(20):
        # Random date of birth between 20 and 80 years ago
        days_ago = random.randint(20*365, 80*365)
        dob = datetime.now().date() - timedelta(days=days_ago)
        
        client = Client(
            first_name=random.choice(first_names),
            last_name=random.choice(last_names),
            date_of_birth=dob,
            gender=random.choice(genders),
            contact_number=f'+1-555-{random.randint(100,999)}-{random.randint(1000,9999)}',
            email=f'client{i+1}@example.com',
            address=f'{random.randint(100,999)} Main St, Anytown, ST {random.randint(10000,99999)}',
            registered_by=doctor_user.id if doctor_user else None
        )
        db.session.add(client)
        created_clients.append(client)

    db.session.commit()
    print(f"Added {len(created_clients)} sample clients")
    
    # Enroll clients in random programs
    enrollment_statuses = ['active', 'completed', 'suspended']
    enrollment_status_weights = [0.7, 0.2, 0.1]  # 70% active, 20% completed, 10% suspended
    
    for client in created_clients:
        # Enroll each client in 1-3 random programs
        for _ in range(random.randint(1, 3)):
            program = random.choice(created_programs)
            
            # Check if client is already enrolled in this program
            existing_enrollment = Enrollment.query.filter_by(
                client_id=client.id,
                program_id=program.id
            ).first()
            
            if not existing_enrollment:
                # Random enrollment between 1 and 365 days ago
                days_ago = random.randint(1, 365)
                enrollment_date = datetime.now() - timedelta(days=days_ago)
                
                # Random status based on weights
                status = random.choices(
                    enrollment_statuses, 
                    weights=enrollment_status_weights, 
                    k=1
                )[0]
                
                enrollment = Enrollment(
                    client_id=client.id,
                    program_id=program.id,
                    enrollment_date=enrollment_date,
                    status=status,
                    notes=f"Sample enrollment notes for {client.first_name} in {program.name}",
                    enrolled_by=doctor_user.id if doctor_user else None
                )
                db.session.add(enrollment)
    
    db.session.commit()
    print("Enrolled clients in health programs")
    print("Database seeding completed!")

def reset_database(app):
    """Drop all tables and recreate them"""
    with app.app_context():
        print("Dropping all tables...")
        db.drop_all()
        print("Creating all tables...")
        db.create_all()

if __name__ == '__main__':
    # Remove existing database file if it exists
    db_file = 'instance/health_system.db'
    if os.path.exists(db_file):
        print(f"Removing existing database file: {db_file}")
        os.remove(db_file)
    
    app = create_app()
    
    with app.app_context():
        # Create tables
        db.create_all()
        # Seed the database
        seed_database()