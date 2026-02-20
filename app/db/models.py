from os import truncate

from sqlalchemy import Column, Integer, String, Enum, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
import enum
from datetime import datetime

Base = declarative_base()

class Data_Plan(enum.Enum):
    FREE = "free"
    PRO = "pro"
    PREMIUM = "premium"

class Status_Pay(enum.Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELED = "canceled"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer, unique=True, index=True, nullable=True)

    username = Column(String)
    create_at = Column(DateTime, default=datetime.utcnow)

    data_plan = Column(Enum(Data_Plan), default=Data_Plan.FREE)
    subscription_expires = Column(DateTime)

    total_request = Column(Integer, default=0)
    monthly_request = Column(Integer, default=0)

    is_active = Column(Boolean, default=True)

    requests = relationship("Request", back_populates="user", cascade="all, delete")
    payments = relationship("Payment", back_populates="user", cascade="all, delete")

class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)

    request = Column(String)

    create_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="requests")


class Payment(Base):
    __tablename__ = "payment"

    id = Column(Integer, primary_key=True)
    provider_payment_id = Column(String, unique=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)

    amount = Column(Integer)
    status = Column(Enum(Status_Pay))

    create_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="payments")
