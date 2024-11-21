from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.api.deps import get_db, get_current_user
from app.schemas.schemas import NotificationCreate, Notification
from app.models.models import Notification as NotificationModel, User

router = APIRouter()

@router.post("/", response_model=Notification)
def create_notification(
    notification: NotificationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_notification = NotificationModel(**notification.dict())
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification

@router.get("/", response_model=List[Notification])
def read_notifications(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    notifications = db.query(NotificationModel).offset(skip).limit(limit).all()
    return notifications

@router.get("/{notification_id}", response_model=Notification)
def read_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    notification = db.query(NotificationModel).filter(NotificationModel.id == notification_id).first()
    if notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification

@router.put("/{notification_id}", response_model=Notification)
def update_notification(
    notification_id: int,
    notification: NotificationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_notification = db.query(NotificationModel).filter(NotificationModel.id == notification_id).first()
    if db_notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    for field, value in notification.dict(exclude_unset=True).items():
        setattr(db_notification, field, value)
    
    db.commit()
    db.refresh(db_notification)
    return db_notification

@router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    notification = db.query(NotificationModel).filter(NotificationModel.id == notification_id).first()
    if notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    db.delete(notification)
    db.commit()
    return {"ok": True}
