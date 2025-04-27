from flask import Flask, request, jsonify, make_response
from models import db, Client, HealthProgram, User, Enrollment
from datetime import datetime
import os
from flask_cors import CORS

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    
    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY='dev',
            SQLALCHEMY_DATABASE_URI='sqlite:///health_system.db',
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
        )
    else:
        app.config.from_mapping(test_config)
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()

    # Health Program Endpoints
    @app.route('/api/programs', methods=['POST'])
    def create_program():
        """Create a new health program"""
        data = request.get_json()
        
        if not data or 'name' not in data:
            return jsonify({'error': 'Name is required'}), 400
            
        if HealthProgram.query.filter_by(name=data['name']).first():
            return jsonify({'error': 'Program with this name already exists'}), 409
            
        program = HealthProgram(
            name=data['name'],
            description=data.get('description', ''),
            created_by=None  # No current_user
        )
        
        db.session.add(program)
        db.session.commit()
        
        return jsonify({'message': 'Program created successfully', 'program': program.to_dict()}), 201

    @app.route('/api/programs', methods=['GET'])
    def get_programs():
        """Get all health programs"""
        programs = HealthProgram.query.all()
        return jsonify([program.to_dict() for program in programs])

    @app.route('/api/programs/<int:id>', methods=['GET'])
    def get_program(id):
        """Get a specific health program by ID"""
        program = HealthProgram.query.get(id)
        
        if not program:
            return jsonify({'error': 'Program not found'}), 404

        return jsonify({'program': program.to_dict()})


    @app.route('/api/programs/<int:id>', methods=['DELETE'])
    def delete_program(id):
        """Delete a health program by ID"""
        program = HealthProgram.query.get(id)
        
        if not program:
            return jsonify({'error': 'Program not found'}), 404

        db.session.delete(program)
        db.session.commit()

        return jsonify({'message': 'Program deleted successfully'}), 200

    @app.route('/api/programs/<int:id>', methods=['PATCH'])
    def update_program(id):
        """Update an existing health program"""
        program = HealthProgram.query.get(id)
        
        if not program:
            return jsonify({'error': 'Program not found'}), 404

        data = request.get_json()

        # Update fields
        program.name = data.get('name', program.name)
        program.description = data.get('description', program.description)

        db.session.commit()

        return jsonify({'message': 'Program updated successfully', 'program': program.to_dict()}), 200


    # Client Endpoints
    @app.route('/api/clients', methods=['POST'])
    def register_client():
        """Register a new client"""
        data = request.get_json()
        
        required_fields = ['first_name', 'last_name', 'date_of_birth', 'gender']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        try:
            date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        client = Client(
            first_name=data['first_name'],
            last_name=data['last_name'],
            date_of_birth=date_of_birth,
            gender=data['gender'],
            contact_number=data.get('contact_number'),
            email=data.get('email'),
            address=data.get('address'),
            registered_by=None  # No current_user
        )
        
        db.session.add(client)
        db.session.commit()
        
        return jsonify({
            'message': 'Client registered successfully', 
            'client': client.to_dict_basic()  # Ensure to return the full client data
        }), 201


    @app.route('/api/clients', methods=['GET'])
    def search_clients():
        """Search for clients with optional filters"""
        first_name = request.args.get('first_name')
        last_name = request.args.get('last_name')
        
        query = Client.query
        
        if first_name:
            query = query.filter(Client.first_name.ilike(f'%{first_name}%'))
        if last_name:
            query = query.filter(Client.last_name.ilike(f'%{last_name}%'))
        
        clients = query.all()
        return jsonify([client.to_dict_basic() for client in clients])

    @app.route('/api/clients/<int:client_id>', methods=['GET'])
    def get_client(client_id):
        """Get a client's profile by ID"""
        client = Client.query.get_or_404(client_id)
        return jsonify(client.to_dict())

    # Enrollment Endpoints
    @app.route('/api/clients/<int:client_id>/programs/<int:program_id>', methods=['POST'])
    def enroll_client(client_id, program_id):
        """Enroll a client in a health program"""
        client = Client.query.get_or_404(client_id)
        program = HealthProgram.query.get_or_404(program_id)
        
        existing_enrollment = Enrollment.query.filter_by(
            client_id=client_id,
            program_id=program_id,
            status='active'
        ).first()
        
        if existing_enrollment:
            return jsonify({'message': 'Client is already actively enrolled in this program'}), 409
        
        data = request.get_json() or {}
        notes = data.get('notes', '')
        
        enrollment = Enrollment(
            client_id=client_id,
            program_id=program_id,
            notes=notes,
            enrolled_by=None  # No current_user
        )
        
        db.session.add(enrollment)
        db.session.commit()
        
        return jsonify({
            'message': f'Client enrolled in {program.name} successfully',
            'enrollment': enrollment.to_dict()
        })

    @app.route('/api/clients/<int:client_id>/programs', methods=['GET'])
    def get_client_programs(client_id):
        """Get all programs a client is enrolled in"""
        client = Client.query.get_or_404(client_id)
        enrollments = Enrollment.query.filter_by(client_id=client_id).all()
        return jsonify([enrollment.to_dict() for enrollment in enrollments])
    
    @app.route('/api/enrollments', methods=['POST'])
def create_enrollment():
    """Enroll a client in a program"""
    data = request.get_json()
    
    client_id = data.get('client_id')
    program_id = data.get('program_id')
    
    if not client_id or not program_id:
        return jsonify({'error': 'Client ID and Program ID are required'}), 400
    
    # Check if this enrollment already exists
    existing_enrollment = Enrollment.query.filter_by(
        client_id=client_id,
        program_id=program_id,
        status='active'
    ).first()
    
    if existing_enrollment:
        return jsonify({'error': 'Client is already enrolled in this program'}), 409
    
    # Create new enrollment
    new_enrollment = Enrollment(
        client_id=client_id, 
        program_id=program_id,
        enrolled_by=None  # No current_user
    )
    
    db.session.add(new_enrollment)
    db.session.commit()
    
    return jsonify({'message': 'Client enrolled successfully', 'enrollment': new_enrollment.to_dict()}), 201


    @app.route('/api/users', methods=['POST'])
    def create_user():
        """Create a new user"""
        data = request.get_json()

        required_fields = ['username', 'email']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 409

        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 409

        user = User(
            username=data['username'],
            email=data['email'],
            role=data.get('role', 'user')  # default role is 'user'
        )

        db.session.add(user)
        db.session.commit()

        return jsonify({'message': 'User created successfully', 'user': user.to_dict()}), 201

    @app.route('/api/users', methods=['GET'])
    def get_users():
        """Get all users"""
        users = User.query.all()
        return jsonify([user.to_dict() for user in users])

    @app.route('/api/users/<int:user_id>', methods=['GET'])
    def get_user(user_id):
        """Get a specific user by ID"""
        user = User.query.get_or_404(user_id)
        return jsonify(user.to_dict())

    @app.route('/api/users/<int:user_id>', methods=['DELETE'])
    def delete_user(user_id):
        """Delete a user"""
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'})


    # --- Enrollment Management Endpoints ---
    @app.route('/api/enrollments', methods=['GET'])
    def get_enrollments():
        """Get all enrollments"""
        enrollments = Enrollment.query.all()
        return jsonify([enrollment.to_dict() for enrollment in enrollments])

    @app.route('/api/enrollments/<int:enrollment_id>', methods=['GET'])
    def get_enrollment(enrollment_id):
        """Get a specific enrollment by ID"""
        enrollment = Enrollment.query.get_or_404(enrollment_id)
        return jsonify(enrollment.to_dict())

    @app.route('/api/enrollments/<int:enrollment_id>', methods=['DELETE'])
    def delete_enrollment(enrollment_id):
        """Delete an enrollment"""
        enrollment = Enrollment.query.get_or_404(enrollment_id)
        db.session.delete(enrollment)
        db.session.commit()
        return jsonify({'message': 'Enrollment deleted successfully'})

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
