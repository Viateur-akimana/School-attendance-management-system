from fastapi import FastAPI
from app.api.v1.endpoints import auth, students, classroom,attendance,notification
from app.db.database import Base, engine

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student Management System")

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(students.router, prefix="/api/v1/students", tags=["Students"])
app.include_router(classroom.router, prefix="/api/v1/classrooms", tags=["ClassRooms"])
app.include_router(attendance.router, prefix="/api/v1/attendance", tags=["Attendance"])
app.include_router(notification.router, prefix="/api/v1/notifications", tags=["Notifications"])