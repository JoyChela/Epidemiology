import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

const Dashboard = () => {
  const [stats, setStats] = useState({
    clientCount: 0,
    programCount: 0,
    enrollmentCount: 0
  });

  useEffect(() => {
    const fetchStats = async () => {
      try {
        // Fetch client count
        const clientResponse = await fetch('http://localhost:5000/api/clients');
        const clients = await clientResponse.json();
        
        // Fetch program count
        const programResponse = await fetch('http://localhost:5000/api/programs');
        const programs = await programResponse.json();
        
        // Calculate enrollment count (in a real app, you'd have a dedicated endpoint)
        let enrollmentCount = 0;
        for (const client of clients) {
          enrollmentCount += client.programs ? client.programs.length : 0;
        }
        
        setStats({
          clientCount: clients.length,
          programCount: programs.length,
          enrollmentCount: enrollmentCount
        });
      } catch (error) {
        console.error('Error fetching dashboard stats:', error);
      }
    };
    
    fetchStats();
  }, []);

  return (
    <div className="dashboard">
      <h1>Health Information System Dashboard</h1>
      
      <div className="dashboard-stats">
        <div className="stat-card">
          <h3>Clients</h3>
          <div className="stat-value">{stats.clientCount}</div>
          <Link to="/clients" className="stat-link">View all</Link>
        </div>
        
        <div className="stat-card">
          <h3>Programs</h3>
          <div className="stat-value">{stats.programCount}</div>
          <Link to="/programs" className="stat-link">View all</Link>
        </div>
        
        <div className="stat-card">
          <h3>Active Enrollments</h3>
          <div className="stat-value">{stats.enrollmentCount}</div>
        </div>
      </div>
      
      <div className="dashboard-actions">
        <Link to="/clients/new" className="button">Register New Client</Link>
        <Link to="/programs/new" className="button">Create New Program</Link>
      </div>
    </div>
  );
};

export default Dashboard;