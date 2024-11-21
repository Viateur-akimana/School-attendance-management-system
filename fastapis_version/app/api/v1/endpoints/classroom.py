from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.api.deps import get_db, get_current_user
from app.schemas.schemas import ClassRoomCreate, ClassRoom, ClassRoomUpdate
from app.models.models import ClassRoom as ClassRoomModel, User

router = APIRouter()

@router.post("/", response_model=ClassRoom)
def create_classroom(
    classroom: ClassRoomCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_classroom = db.query(ClassRoomModel).filter(ClassRoomModel.name == classroom.name).first()
    if db_classroom:
        raise HTTPException(status_code=400, detail="Classroom already exists")
    
    db_classroom = ClassRoomModel(**classroom.dict())
    db.add(db_classroom)
    db.commit()
    db.refresh(db_classroom)
    return db_classroom

@router.get("/", response_model=List[ClassRoom])
def read_classrooms(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    classrooms = db.query(ClassRoomModel).offset(skip).limit(limit).all()
    return classrooms

@router.get("/{classroom_id}", response_model=ClassRoom)
def read_classroom(
    classroom_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    classroom = db.query(ClassRoomModel).filter(ClassRoomModel.id == classroom_id).first()
    if classroom is None:
        raise HTTPException(status_code=404, detail="Classroom not found")
    return classroom

@router.put("/{classroom_id}", response_model=ClassRoom)
def update_classroom(
    classroom_id: int,
    classroom: ClassRoomUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_classroom = db.query(ClassRoomModel).filter(ClassRoomModel.id == classroom_id).first()
    if db_classroom is None:
        raise HTTPException(status_code=404, detail="Classroom not found")
    
    for field, value in classroom.dict(exclude_unset=True).items():
        setattr(db_classroom, field, value)
    
    db.commit()
    db.refresh(db_classroom)
    return db_classroom

@router.delete("/{classroom_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_classroom(
    classroom_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    classroom = db.query(ClassRoomModel).filter(ClassRoomModel.id == classroom_id).first()
    if classroom is None:
        raise HTTPException(status_code=404, detail="Classroom not found")
    
    db.delete(classroom)
    db.commit()
    return {"ok": True}
