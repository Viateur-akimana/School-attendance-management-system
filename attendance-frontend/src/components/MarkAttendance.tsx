// src/components/MarkAttendance.tsx
import React, { useState } from 'react';
import { markAttendance } from '../services/api';

const MarkAttendance: React.FC = () => {
  const [studentId, setStudentId] = useState<string>('');
  const [status, setStatus] = useState<string>('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await markAttendance({ student: parseInt(studentId), status });
      alert('Attendance marked successfully!');
      setStudentId('');
      setStatus('');
    } catch (error) {
      console.error(error);
      alert('Failed to mark attendance.');
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Mark Attendance</h1>
      <form onSubmit={handleSubmit} className="flex flex-col space-y-4">
        <input
          type="text"
          placeholder="Student ID"
          value={studentId}
          onChange={(e) => setStudentId(e.target.value)}
          className="border border-gray-300 p-2 rounded"
        />
        <select
          value={status}
          onChange={(e) => setStatus(e.target.value)}
          className="border border-gray-300 p-2 rounded"
        >
          <option value="">Select Status</option>
          <option value="Present">Present</option>
          <option value="Absent">Absent</option>
        </select>
        <button
          type="submit"
          className="bg-blue-500 text-white p-2 rounded"
        >
          Mark Attendance
        </button>
      </form>
    </div>
  );
};

export default MarkAttendance;
