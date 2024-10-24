// src/App.tsx
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import AttendanceList from './components/AttendanceList';
import MarkAttendance from './components/MarkAttendance';

const App: React.FC = () => (
  <Router>
    <Routes>
      <Route path="/" element={<AttendanceList />} />
      <Route path="/mark" element={<MarkAttendance />} />
    </Routes>
  </Router>
);

export default App;
