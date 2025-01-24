from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, database
from datetime import datetime, timedelta

router = APIRouter()

# 의존성
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/subscriptions/")
def create_subscription(user_id: int, db: Session = Depends(get_db)):
    # 사용자 존재 확인
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 활성 구독이 있는지 확인
    active_sub = db.query(models.Subscription).filter(
        models.Subscription.user_id == user_id,
        models.Subscription.status == models.Subscription.STATUS_ACTIVE
    ).first()
    
    if active_sub:
        raise HTTPException(status_code=400, detail="User already has an active subscription")
    
    # 구독 생성
    start_date = datetime.utcnow()
    end_date = start_date + timedelta(days=30)  # 30일 구독
    
    subscription = models.Subscription(
        user_id=user_id,
        status=models.Subscription.STATUS_PENDING,  # 결제 전이므로 PENDING
        start_date=start_date,
        end_date=end_date
    )
    
    db.add(subscription)
    db.commit()
    db.refresh(subscription)
    return subscription

@router.get("/subscriptions/")
def get_subscriptions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    subscriptions = db.query(models.Subscription).offset(skip).limit(limit).all()
    return subscriptions

@router.get("/subscriptions/{subscription_id}")
def get_subscription(subscription_id: int, db: Session = Depends(get_db)):
    subscription = db.query(models.Subscription).filter(models.Subscription.id == subscription_id).first()
    if subscription is None:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return subscription

@router.put("/subscriptions/{subscription_id}/activate")
def activate_subscription(subscription_id: int, db: Session = Depends(get_db)):
    subscription = db.query(models.Subscription).filter(models.Subscription.id == subscription_id).first()
    if subscription is None:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    if subscription.status == models.Subscription.STATUS_ACTIVE:
        raise HTTPException(status_code=400, detail="Subscription is already active")
    
    subscription.status = models.Subscription.STATUS_ACTIVE
    db.commit()
    db.refresh(subscription)
    return subscription

@router.get("/users/{user_id}/subscription")
def get_user_subscription(user_id: int, db: Session = Depends(get_db)):
    subscription = db.query(models.Subscription).filter(
        models.Subscription.user_id == user_id,
        models.Subscription.status == models.Subscription.STATUS_ACTIVE
    ).first()
    
    if subscription is None:
        raise HTTPException(status_code=404, detail="No active subscription found")
    return subscription