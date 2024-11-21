from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.api.deps import get_db, get_current_user
from app.schemas.schemas import AttendanceCreate, Attendance, AttendanceUpdate
from app.models.models import Attendance as AttendanceModel, User

router = APIRouter()

@router.post("/", response_model=Attendance)
def create_attendance(
    attendance: AttendanceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_attendance = AttendanceModel(**attendance.dict())
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance

@router.get("/", response_model=List[Attendance])
def read_attendances(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    attendances = db.query(AttendanceModel).offset(skip).limit(limit).all()
    return attendances

@router.get("/{attendance_id}", response_model=Attendance)
def read_attendance(
    attendance_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    attendance = db.query(AttendanceModel).filter(AttendanceModel.id == attendance_id).first()
    if attendance is None:
        raise HTTPException(status_code=404, detail="Attendance not found")
    return attendance

@router.put("/{attendance_id}", response_model=Attendance)
def update_attendance(
    attendance_id: int,
    attendance: AttendanceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_attendance = db.query(AttendanceModel).filter(AttendanceModel.id == attendance_id).first()
    if db_attendance is None:
        raise HTTPException(status_code=404, detail="Attendance not found")
    
    for field, value in attendance.dict(exclude_unset=True).items():
        setattr(db_attendance, field, value)
    
    db.commit()
    db.refresh(db_attendance)
    return db_attendance

@router.delete("/{attendance_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_attendance(
    attendance_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    attendance = db.query(AttendanceModel).filter(AttendanceModel.id == attendance_id).first()
    if attendance is None:
        raise HTTPException(status_code=404, detail="Attendance not found")
    
    db.delete(attendance)
    db.commit()
    return {"ok": True}
