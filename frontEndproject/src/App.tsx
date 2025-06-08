import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { SimulationPage } from './pages/SimulationPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<SimulationPage />} />
        <Route path="/simulation" element={<SimulationPage />} />
      </Routes>
    </Router>
  );
}

export default App;