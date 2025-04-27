import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';

const ClientDetail = () => {
  const { id } = useParams();
  const [client, setClient] = useState(null);
  const [programs, setPrograms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [enrolling, setEnrolling] = useState(false);
  const [selectedProgram, setSelectedProgram] = useState('');
  const [enrollmentMessage, setEnrollmentMessage] = useState('');

  useEffect(() => {
    const fetchClientAndPrograms = async () => {
      try {
        setLoading(true);
        
        // Fetch client details
        const clientResponse = await fetch(`http://localhost:5000/api/clients/${id}`);
        if (!clientResponse.ok) {
          throw new Error('Client not found');
        }
        const clientData = await clientResponse.json();
        setClient(clientData);
        
        // Fetch all available programs
        const programsResponse = await fetch('http://localhost:5000/api/programs');
        if (!programsResponse.ok) {
          throw new Error('Failed to fetch programs');
        }
        const programsData = await programsResponse.json();
        setPrograms(programsData);
        
        setError(null);
      } catch (err) {
        setError(err.message);
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    
    fetchClientAndPrograms();
  }, [id]);

  const handleEnroll = async (e) => {
    e.preventDefault();
    
    if (!selectedProgram) {
      setEnrollmentMessage('Please select a program');
      return;
    }
    
    try {
      const response = await fetch('http://localhost:5000/api/enrollments', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          client_id: client.id,
          program_id: selectedProgram
        }),
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.error || 'Failed to enroll client');
      }
      
      // Reload client data to show updated enrollments
      const clientResponse = await fetch(`http://localhost:5000/api/clients/${id}`);
      const clientData = await clientResponse.json();
      setClient(clientData);
      
      setEnrollmentMessage('Client successfully enrolled in program');
      setSelectedProgram('');
      setTimeout(() => setEnrolling(false), 2000);
    } catch (err) {
      setEnrollmentMessage(err.message);
      console.error(err);
    }
  };

  if (loading) return <div className="loading">Loading client details...</div>;
  if (error) return <div className="error-message">{error}</div>;
  if (!client) return <div className="not-found">Client not found</div>;
  
  // Filter out programs the client is already enrolled in
  const availablePrograms = programs.filter(program => 
    !client.programs.some(enrolledProgram => enrolledProgram.id === program.id)
  );

  return (
    <div className="client-profile">
      <div className="profile-header">
        <h1>{client.first_name} {client.last_name}</h1>
        <div className="profile-actions">
          <button 
            onClick={() => setEnrolling(!enrolling)}
            className="button"
            disabled={availablePrograms.length === 0}
          >
            Enroll in Program
          </button>
        </div>
      </div>
      
      <div className="profile-content">
        <div className="profile-section personal-info">
          <h2>Personal Information</h2>
          <div className="info-grid">
            <div className="info-item">
              <span className="label">Date of Birth:</span>
              <span className="value">{new Date(client.date_of_birth).toLocaleDateString()}</span>
            </div>
            <div className="info-item">
              <span className="label">Gender:</span>
              <span className="value">{client.gender}</span>
            </div>
            <div className="info-item">
              <span className="label">Phone:</span>
              <span className="value">{client.phone || 'Not provided'}</span>
            </div>
            <div className="info-item">
              <span className="label">Email:</span>
              <span className="value">{client.email || 'Not provided'}</span>
            </div>
            <div className="info-item">
              <span className="label">Address:</span>
              <span className="value">{client.address || 'Not provided'}</span>
            </div>
          </div>
        </div>
        
        {enrolling && (
          <div className="enrollment-form">
            <h2>Enroll in New Program</h2>
            
            {enrollmentMessage && (
              <div className={enrollmentMessage.includes('success') ? 'success-message' : 'error-message'}>
                {enrollmentMessage}
              </div>
            )}
            
            {availablePrograms.length === 0 ? (
              <div className="info-message">This client is already enrolled in all available programs.</div>
            ) : (
              <form onSubmit={handleEnroll}>
                <div className="form-group">
                  <label htmlFor="program">Select Program:</label>
                  <select 
                    id="program"
                    value={selectedProgram}
                    onChange={(e) => setSelectedProgram(e.target.value)}
                    required
                  >
                    <option value="">-- Select a program --</option>
                    {availablePrograms.map(program => (
                      <option key={program.id} value={program.id}>
                        {program.name}
                      </option>
                    ))}
                  </select>
                </div>
                <button type="submit" className="button">Enroll</button>
                <button 
                  type="button" 
                  onClick={() => {
                    setEnrolling(false);
                    setEnrollmentMessage('');
                  }}
                  className="button secondary"
                >
                  Cancel
                </button>
              </form>
            )}
          </div>
        )}
        
        <div className="profile-section programs">
          <h2>Enrolled Programs</h2>
          
          {client.programs.length === 0 ? (
            <div className="info-message">
              No programs enrolled. Use the "Enroll in Program" button to add programs.
            </div>
          ) : (
            <div className="program-list">
              {client.programs.map(program => (
                <div key={program.id} className="program-item">
                  <div className="program-name">{program.name}</div>
                  <div className="program-description">{program.description}</div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ClientDetail;
