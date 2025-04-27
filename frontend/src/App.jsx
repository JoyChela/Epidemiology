import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import ClientList from './components/ClientList';
import ClientDetail from './components/ClientDetails';
import ClientForm from './components/ClientForm';
import ProgramList from './components/ProgramList';
import ProgramForm from './components/ProgramForm';
import ProgramEdit from './components/ProgramEdit.jsx';
import Navbar from './components/Navbar';
import './App.css';

function App() {

  return (
    <Router>
      <div className="app">
        <Navbar />
        <div className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/clients" element={<ClientList />} />
            <Route path="/clients/new" element={<ClientForm />} />
            <Route path="/clients/:id" element={<ClientDetail />} />
            <Route path="/programs" element={<ProgramList />} />
            <Route path="/programs/new" element={<ProgramForm />} />
            <Route path="/programs/edit/:id" element={<ProgramEdit />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;