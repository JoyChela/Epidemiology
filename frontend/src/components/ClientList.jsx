import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

const ClientList = () => {
  const [clients, setClients] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [deleteMessage, setDeleteMessage] = useState(null);

  const fetchClients = async (search = '') => {
    try {
      setLoading(true);
      let url = 'http://127.0.0.1:5000/api/clients';
      
      if (search) {
        // Use the search parameter which handles both first and last name
        url += `?search=${encodeURIComponent(search)}`;
      }

      const response = await fetch(url);

      if (!response.ok) {
        throw new Error(`Failed to fetch clients: ${response.statusText}`);
      }

      const data = await response.json();
      console.log("Fetched clients:", data);
      
      // For each client, fetch their active programs to display the count and names
      const clientsWithPrograms = await Promise.all(data.map(async (client) => {
        try {
          // Fetch the full client details including programs
          const detailResponse = await fetch(`http://127.0.0.1:5000/api/clients/${client.id}`);
          if (detailResponse.ok) {
            const detailData = await detailResponse.json();
            // If the client has programs, get them, otherwise return the basic client data
            if (detailData.programs) {
              return {
                ...client,
                programs: detailData.programs
              };
            }
          }
          return client;
        } catch (err) {
          console.error(`Error fetching details for client ${client.id}:`, err);
          return client;
        }
      }));

      setClients(clientsWithPrograms);
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

  const handleClearSearch = () => {
    setSearchTerm('');
    fetchClients('');
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this client?')) {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/clients/${id}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json'
          }
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || `Failed to delete client: ${response.statusText}`);
        }

        // Remove the deleted client from the state
        setClients(clients.filter(client => client.id !== id));
        setDeleteMessage('Client deleted successfully');
        
        // Clear message after 3 seconds
        setTimeout(() => {
          setDeleteMessage(null);
        }, 3000);
      } catch (err) {
        setError(`Error deleting client: ${err.message}`);
        console.error(err);
      }
    }
  };

  return (
    <div className="client-list">
      <div className="list-header">
        <h1>Client Registry</h1>
        <Link to="/clients/new" className="button">Register New Client</Link>
      </div>

      {deleteMessage && (
        <div className="success-message">{deleteMessage}</div>
      )}

      {error && (
        <div className="error-message">{error}</div>
      )}

      <form onSubmit={handleSearch} className="search-form">
        <input
          type="text"
          placeholder="Search clients by name..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="search-input"
        />
        <button type="submit" className="search-button">Search</button>
        {searchTerm && (
          <button 
            type="button" 
            onClick={handleClearSearch} 
            className="clear-button"
          >
            Clear
          </button>
        )}
      </form>

      {loading ? (
        <div className="loading">Loading clients...</div>
      ) : clients.length === 0 ? (
        <div className="no-results">
          {searchTerm ? 
            `No clients found matching "${searchTerm}". Try a different search term or` : 
            'No clients found. Please'} 
          <Link to="/clients/new"> register a new client</Link>.
        </div>
      ) : (
        <div className="client-grid">
          {clients.map(client => (
            <div key={client.id} className="client-card-container">
              <Link to={`/clients/${client.id}`} className="client-card">
                <div className="client-name">{client.first_name} {client.last_name}</div>
                <div className="client-details">
                  <div className="client-gender">Gender: {client.gender || 'Not specified'}</div>
                  <div className="client-programs-count">
                    Programs: {client.programs ? client.programs.length : 0}
                    {client.programs && client.programs.length > 0 && (
                      <div className="program-names">
                        {client.programs.map((program, index) => (
                          <span key={program.id} className="program-badge">
                            {program.name}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              </Link>
              <button 
                onClick={() => handleDelete(client.id)} 
                className="delete-button"
              >
                Delete
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ClientList;