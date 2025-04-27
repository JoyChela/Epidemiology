# Health Information System

A simple health information system for managing clients and health programs/services. This project allows healthcare providers to register clients, create health programs, and manage client enrollments in various health programs.

## Features

- 👤 **Client Management**: Register new clients and manage their profiles
- 🏥 **Health Programs**: Create and manage health programs (e.g., TB, Malaria, HIV)
- 🔄 **Program Enrollment**: Enroll clients in one or more health programs
- 🔍 **Search Functionality**: Find clients easily with search functionality
- 📊 **Dashboard**: Overview of system statistics
- 🔌 **API Access**: Access client profiles and other data via a RESTful API

## Tech Stack

- **Frontend**: React.js
- **Backend**: Flask (Python)
- **Database**: SQLite (development), can be migrated to PostgreSQL for production
- **API**: RESTful API with JSON responses

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 14+
- npm or yarn

### Backend Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/health-information-system.git
   cd health-information-system
   ```

2. Set up a Python virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the Flask application:
   ```
   flask run
   ```
   The API will be available at http://localhost:5000

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm start
   ```
   The application will be available at http://localhost:3000

## API Documentation

### Client Endpoints

- `GET /api/clients`: Get all clients (supports search with query parameter `?search=name`)
- `POST /api/clients`: Create a new client
- `GET /api/clients/<client_id>`: Get client details by ID

### Program Endpoints

- `GET /api/programs`: Get all health programs
- `POST /api/programs`: Create a new health program
- `GET /api/programs/<program_id>`: Get program details by ID

### Enrollment Endpoints

- `POST /api/enrollments`: Enroll a client in a program
- `GET /api/clients/<client_id>/enrollments`: Get all enrollments for a specific client

## Security Considerations

- Input validation on both frontend and backend
- Error handling to prevent information disclosure
- Database query parameterization to prevent SQL injection
- CORS configuration to control API access

## Project Structure

```
health-information-system/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── models.py           # Database models
│   ├── routes/             # API routes
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── public/             # Static files
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── App.js          # Main React component
│   │   └── index.js        # React entry point
│   └── package.json        # JavaScript dependencies
└── README.md               # Project documentation
```

## Future Enhancements

- User authentication and authorization
- More detailed client medical records
- Appointment scheduling
- Reporting and analytics
- Mobile application

## Additional Resources

- [Project Presentation](https://app.presentations.ai/view/4XCMJv)
