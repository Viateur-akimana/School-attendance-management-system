from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ClassRoom(Base):
    __tablename__ = "classrooms"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    students = relationship("Student", back_populates="class_room")

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    class_room_id = Column(Integer, ForeignKey("classrooms.id"))
    roll_number = Column(Integer, unique=True)
    email = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    class_room = relationship("ClassRoom", back_populates="students")
    attendances = relationship("Attendance", back_populates="student")
    notifications = relationship("Notification", back_populates="student")

class Attendance(Base):
    __tablename__ = "attendances"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    date = Column(DateTime, default=datetime.utcnow)
    status = Column(Boolean, default=False)  # True for present, False for absent
    student = relationship("Student", back_populates="attendances")

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    message = Column(String, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    date_sent = Column(DateTime, default=datetime.utcnow)
    student = relationship("Student", back_populates="notifications")