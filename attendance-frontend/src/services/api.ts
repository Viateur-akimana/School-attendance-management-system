import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api';

export interface Student {
  id: number;
  user: {
    username: string;
    first_name: string;
    last_name: string;
  };
  classroom: number;
}

export interface Attendance {
  id: number;
  student: Student;
  date: string;
  status: string;
}

export const getAttendance = async (): Promise<Attendance[]> => {
  const response = await axios.get(`${API_URL}/attendance/`);
  return response.data;
};

export const markAttendance = async (data: {
  student: number;
  status: string;
}): Promise<Attendance> => {
  const response = await axios.post(`${API_URL}/attendance/`, data);
  return response.data;
};
