import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';

const ProgramList = () => {
  const [programs, setPrograms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetchPrograms();
  }, []);

  const fetchPrograms = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:5000/api/programs');
      
      if (!response.ok) {
        throw new Error('Failed to fetch programs');
      }
      
      const data = await response.json();
      setPrograms(data);
      setError(null);
    } catch (err) {
      setError('Error loading programs. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this program?')) {
      return;
    }

    try {
      const response = await fetch(`http://localhost:5000/api/programs/${id}`, {
        method: 'DELETE',
      });

      if (!response.ok) {
        throw new Error('Failed to delete program');
      }

      setPrograms(programs.filter(program => program.id !== id));
    } catch (err) {
      console.error('Error deleting program:', err);
      alert('Failed to delete program. Please try again.');
    }
  };

  const handleEdit = (id) => {
    navigate(`/programs/edit/${id}`);
  };

  return (
    <div className="program-list-container">
      <div className="list-header">
        <h1>Health Programs</h1>
        <Link to="/programs/new" className="button">Create New Program</Link>
      </div>
      
      {loading ? (
        <div className="loading">Loading programs...</div>
      ) : error ? (
        <div className="error-message">{error}</div>
      ) : programs.length === 0 ? (
        <div className="no-results">No health programs found. Please create a new program.</div>
      ) : (
        <div className="program-grid">
          {programs.map(program => (
            <div key={program.id} className="program-card">
              <h3 className="program-title">{program.name}</h3>
              <p className="program-desc">{program.description}</p>
              <div className="program-meta">
                <span className="program-date">
                  Created: {new Date(program.created_at).toLocaleDateString()}
                </span>
              </div>
              <div className="program-actions">
                <button onClick={() => handleEdit(program.id)} className="edit-button">
                  Edit
                </button>
                <button onClick={() => handleDelete(program.id)} className="delete-button">
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ProgramList;
