# server/app/models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from server.app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    telegram_id = Column(String(50), nullable=True)
    # etc.

class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String(20), default="ACTIVE")  # or "INACTIVE"
    start_date = Column(DateTime)
    end_date = Column(DateTime)

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True)
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"))
    amount = Column(Float, nullable=False)
    payment_date = Column(DateTime)
    transaction_id = Column(String(100))