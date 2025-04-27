import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="navbar-brand">Health Information System</div>
      <div className="navbar-menu">
        <Link to="/" className="navbar-item">Dashboard</Link>
        <Link to="/clients" className="navbar-item">Clients</Link>
        <Link to="/programs" className="navbar-item">Programs</Link>
      </div>
    </nav>
  );
};

export default Navbar;