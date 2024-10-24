import React, { useEffect, useState } from 'react';
import { getAttendance, Attendance } from '../services/api';

const AttendanceList: React.FC = () => {
  const [attendance, setAttendance] = useState<Attendance[]>([]);

  useEffect(() => {
    getAttendance().then(setAttendance).catch(console.error);
  }, []);

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Attendance List</h1>
      <table className="min-w-full border-collapse border border-gray-300">
        <thead>
          <tr>
            <th className="border border-gray-300 p-2">Student</th>
            <th className="border border-gray-300 p-2">Status</th>
            <th className="border border-gray-300 p-2">Date</th>
          </tr>
        </thead>
        <tbody>
          {attendance.map((record) => (
            <tr key={record.id} className="hover:bg-gray-100">
              <td className="border border-gray-300 p-2">{`${record.student.user.first_name} ${record.student.user.last_name}`}</td>
              <td className="border border-gray-300 p-2">{record.status}</td>
              <td className="border border-gray-300 p-2">{record.date}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AttendanceList;
