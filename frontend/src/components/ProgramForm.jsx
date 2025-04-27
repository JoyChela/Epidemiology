import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const ProgramForm = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: '',
    description: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    try {
      const response = await fetch('http://localhost:5000/api/programs', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.error || 'Failed to create program');
      }
      
      // Redirect to the programs list
      navigate('/programs');
    } catch (err) {
      setError(err.message);
      console.error('Error creating program:', err);
      setLoading(false);
    }
  };

  return (
    <div className="program-form-container">
      <h1>Create New Health Program</h1>
      
      {error && <div className="error-message">{error}</div>}
      
      <form onSubmit={handleSubmit} className="program-form">
        <div className="form-group">
          <label htmlFor="name">Program Name *</label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            placeholder="e.g., Tuberculosis Control Program"
            required
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="description">Program Description *</label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            placeholder="Describe the purpose and services of this health program"
            rows="5"
            required
          />
        </div>
        
        <div className="form-actions">
          <button type="submit" className="button" disabled={loading}>
            {loading ? 'Creating...' : 'Create Program'}
          </button>
          <button 
            type="button" 
            className="button secondary" 
            onClick={() => navigate('/programs')}
            disabled={loading}
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
};

export default ProgramForm;