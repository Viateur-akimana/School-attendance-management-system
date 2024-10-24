export interface User {
    id: number;
    username: string;
    firstName: string;
    lastName: string;
    role: 'admin' | 'teacher' | 'staff';
    email: string;
    phone?: string;
  }
  
  export interface Student {
    id: number;
    registrationNumber: string;
    firstName: string;
    lastName: string;
    dateOfBirth: string;
    classGroupId: number;
    parentContact: string;
    parentEmail: string;
  }
  
  export interface ClassGroup {
    id: number;
    name: string;
    teacherId: number;
    academicYear: string;
    isActive: boolean;
  }
  
  export interface Attendance {
    id: number;
    studentId: number;
    classGroupId: number;
    date: string;
    status: 'present' | 'absent' | 'late' | 'excused';
    remarks?: string;
    markedById: number;
    createdAt: string;
    updatedAt: string;
  }
  
  export interface AttendanceReport {
    id: number;
    name: string;
    type: string;
    parameters: Record<string, any>;
    generatedBy: number;
    fileUrl?: string;
    createdAt: string;
  }
  
  export interface Notification {
    id: number;
    userId: number;
    title: string;
    message: string;
    type: string;
    isRead: boolean;
    createdAt: string;
  }