from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from config import Config, ApprovalStatus

Base = declarative_base()
engine = create_engine(Config.db.url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Company(Base):
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    price = Column(Float, nullable=False)
    shares = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    bids = relationship("Bid", back_populates="company", cascade="all, delete-orphan")
    outputs = relationship("CalculatedOutput", back_populates="company", uselist=False)
    
    __table_args__ = (
        CheckConstraint('price > 0', name='positive_price'),
        CheckConstraint('shares > 0', name='positive_shares'),
    )

class Investor(Base):
    __tablename__ = "investors"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    bids = relationship("Bid", back_populates="investor", cascade="all, delete-orphan")

class Bid(Base):
    __tablename__ = "bids"
    
    id = Column(Integer, primary_key=True, index=True)
    investor_id = Column(Integer, ForeignKey("investors.id"), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    shares_bid = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    investor = relationship("Investor", back_populates="bids")
    company = relationship("Company", back_populates="bids")
    
    __table_args__ = (
        CheckConstraint('shares_bid >= 0', name='non_negative_bid'),
    )

class ApprovalToggle(Base):
    __tablename__ = "approval_toggles"
    
    id = Column(Integer, primary_key=True, index=True)
    field_name = Column(String(100), nullable=False, unique=True)
    team1_status = Column(Integer, default=ApprovalStatus.TBD, nullable=False)
    team2_status = Column(Integer, default=ApprovalStatus.TBD, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    __table_args__ = (
        CheckConstraint('team1_status IN (0, 1)', name='valid_team1_status'),
        CheckConstraint('team2_status IN (0, 1)', name='valid_team2_status'),
    )

class CalculatedOutput(Base):
    __tablename__ = "calculated_outputs"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False, unique=True)
    total_bid = Column(Integer, nullable=False, default=0)
    capital_raised = Column(Float, nullable=False, default=0.0)
    subscription_status = Column(String(20), nullable=False)
    calculated_at = Column(DateTime(timezone=True), server_default=func.now())
    
    company = relationship("Company", back_populates="outputs")
    
    __table_args__ = (
        CheckConstraint('total_bid >= 0', name='non_negative_total_bid'),
        CheckConstraint('capital_raised >= 0', name='non_negative_capital'),
    )

def init_db():
    Base.metadata.create_all(bind=engine)
    return engine

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 