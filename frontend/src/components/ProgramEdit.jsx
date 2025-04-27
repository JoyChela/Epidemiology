import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';

const ProgramEdit = () => {
  const [program, setProgram] = useState({ name: '', description: '' });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const { id } = useParams(); // Get the program ID from the URL

  useEffect(() => {
    fetchProgram();
  }, [id]);

  const fetchProgram = async () => {
    try {
      setLoading(true);
      const response = await fetch(`http://localhost:5000/api/programs/${id}`);

      if (!response.ok) {
        throw new Error('Failed to fetch program');
      }

      const data = await response.json();
      // Extract the program data from the response
      setProgram(data.program);
      setError(null);
    } catch (err) {
      setError('Error loading program. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    try {
      const response = await fetch(`http://localhost:5000/api/programs/${id}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(program),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to update program');
      }

      navigate('/programs'); // Redirect to the program list after saving
    } catch (err) {
      setError(err.message || 'Error saving program. Please try again.');
      console.error(err);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setProgram(prevState => ({
      ...prevState,
      [name]: value,
    }));
  };

  const handleCancel = () => {
    navigate('/programs');
  };

  return (
    <div className="program-edit-container">
      <h1>Edit Program</h1>
      
      {loading ? (
        <div>Loading...</div>
      ) : error ? (
        <div className="error-message">{error}</div>
      ) : (
        <div className="form-container">
          <div className="form-group">
            <label htmlFor="name">Program Name</label>
            <input
              type="text"
              id="name"
              name="name"
              value={program.name || ''}
              onChange={handleChange}
              className="form-control"
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="description">Description</label>
            <textarea
              id="description"
              name="description"
              value={program.description || ''}
              onChange={handleChange}
              className="form-control"
              rows="4"
            ></textarea>
          </div>
          
          <div className="button-group">
            <button onClick={handleSave} className="save-button">Save</button>
            <button onClick={handleCancel} className="cancel-button">Cancel</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ProgramEdit;