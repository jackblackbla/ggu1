from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)  # 해시된 비밀번호
    telegram_id = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # relationships
    subscriptions = relationship("Subscription", back_populates="user", cascade="all, delete-orphan")

class Subscription(Base):
    __tablename__ = "subscriptions"
    
    # 상태 상수
    STATUS_ACTIVE = "ACTIVE"
    STATUS_INACTIVE = "INACTIVE"
    STATUS_PENDING = "PENDING"
    STATUS_EXPIRED = "EXPIRED"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String(20), default=STATUS_PENDING, index=True)
    billing_cycle = Column(String(10), nullable=False, default="MONTHLY")  # MONTHLY/YEARLY
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # relationships
    user = relationship("User", back_populates="subscriptions")
    payments = relationship("Payment", back_populates="subscription", cascade="all, delete-orphan")

class Payment(Base):
    __tablename__ = "payments"
    
    STATUS_PENDING = "PENDING"
    STATUS_COMPLETED = "COMPLETED"
    STATUS_FAILED = "FAILED"
    
    id = Column(Integer, primary_key=True)
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"), nullable=False)
    amount = Column(Float, nullable=False)
    payment_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    transaction_id = Column(String(100), unique=True)
    status = Column(String(20), default=STATUS_PENDING)
    pg_provider = Column(String(20), nullable=False, default="TOSS")  # 결제 제공자
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # relationships
    subscription = relationship("Subscription", back_populates="payments")