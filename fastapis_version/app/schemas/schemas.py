from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class ClassRoomBase(BaseModel):
    name: str

class ClassRoomCreate(ClassRoomBase):
    pass

class ClassRoomUpdate(BaseModel):
    name: Optional[str]

class ClassRoom(ClassRoomBase):
    id: int
    students: List["Student"]

    class Config:
        orm_mode = True

class StudentBase(BaseModel):
    name: str
    class_room_id: int
    roll_number: int
    email: EmailStr

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    name: Optional[str]
    class_room_id: Optional[int]
    roll_number: Optional[int]
    email: Optional[EmailStr]

class Student(StudentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class AttendanceBase(BaseModel):
    student_id: int
    status: bool

class AttendanceCreate(AttendanceBase):
    pass

class AttendanceUpdate(BaseModel):
    student_id: Optional[int]
    status: Optional[bool]

class Attendance(AttendanceBase):
    id: int
    date: datetime

    class Config:
        orm_mode = True

class NotificationBase(BaseModel):
    student_id: int
    message: str

class NotificationCreate(NotificationBase):
    pass

class Notification(NotificationBase):
    id: int
    date_sent: datetime

    class Config:
        orm_mode = True