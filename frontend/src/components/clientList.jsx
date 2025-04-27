import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

const ClientList = () => {
  const [clients, setClients] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchClients = async (search = '') => {
    try {
      setLoading(true);
      const response = await fetch(`http://localhost:5000/api/clients?search=${search}`);
      
      if (!response.ok) {
        throw new Error('Failed to fetch clients');
      }
      
      const data = await response.json();
      setClients(data);
      setError(null);
    } catch (err) {
      setError('Error loading clients. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchClients();
  }, []);

  const handleSearch = (e) => {
    e.preventDefault();
    fetchClients(searchTerm);
  };

  return (
    <div className="client-list">
      <div className="list-header">
        <h1>Client Registry</h1>
        <Link to="/clients/new" className="button">Register New Client</Link>
      </div>
      
      <form onSubmit={handleSearch} className="search-form">
        <input
          type="text"
          placeholder="Search clients by name..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="search-input"
        />
        <button type="submit" className="search-button">Search</button>
      </form>
      
      {loading ? (
        <div className="loading">Loading clients...</div>
      ) : error ? (
        <div className="error-message">{error}</div>
      ) : clients.length === 0 ? (
        <div className="no-results">No clients found. Please register a new client.</div>
      ) : (
        <div className="client-grid">
          {clients.map(client => (
            <Link to={`/clients/${client.id}`} key={client.id} className="client-card">
              <div className="client-name">{client.first_name} {client.last_name}</div>
              <div className="client-details">
                <div>Gender: {client.gender}</div>
                <div>Programs: {client.programs ? client.programs.length : 0}</div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
};

export default ClientList;