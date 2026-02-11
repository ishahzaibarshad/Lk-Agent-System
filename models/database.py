"""SQLAlchemy database models."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean, Float
from sqlalchemy.orm import relationship
from database.connection import Base

class User(Base):
    """User model for authentication."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    agents = relationship("Agent", back_populates="owner", cascade="all, delete-orphan")
    contacts = relationship("Contact", back_populates="owner", cascade="all, delete-orphan")

class Agent(Base):
    """AI Agent model."""
    __tablename__ = "agents"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    voice_id = Column(String(255))
    prompt = Column(Text)
    greeting_messages = Column(Text)  # JSON string of greeting messages
    is_active = Column(Boolean, default=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    owner = relationship("User", back_populates="agents")
    calls = relationship("Call", back_populates="agent", cascade="all, delete-orphan")

class Contact(Base):
    """Contact model."""
    __tablename__ = "contacts"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=False)
    email = Column(String(255))
    company = Column(String(255))
    notes = Column(Text)
    tags = Column(String(500))  # Comma-separated tags
    timezone = Column(String(50))
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    owner = relationship("User", back_populates="contacts")
    calls = relationship("Call", back_populates="contact", cascade="all, delete-orphan")
    bookings = relationship("Booking", back_populates="contact", cascade="all, delete-orphan")

class Call(Base):
    """Call record model."""
    __tablename__ = "calls"
    
    id = Column(Integer, primary_key=True, index=True)
    call_sid = Column(String(255), unique=True, index=True)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False)
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=False)
    status = Column(String(50), default="initiated")  # initiated, in_progress, completed, failed
    duration = Column(Integer)  # Duration in seconds
    transcript = Column(Text)
    recording_url = Column(String(500))
    outcome = Column(String(50))  # qualified, not_qualified, callback, voicemail, no_answer
    sentiment = Column(String(50))  # positive, neutral, negative
    notes = Column(Text)
    call_metadata = Column(Text)  # JSON string for additional data
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    agent = relationship("Agent", back_populates="calls")
    contact = relationship("Contact", back_populates="calls")
    booking = relationship("Booking", back_populates="call", uselist=False, cascade="all, delete-orphan")

class Booking(Base):
    """Booking/Appointment model."""
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    call_id = Column(Integer, ForeignKey("calls.id"), unique=True, nullable=True)  # Nullable for manual bookings
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=False)
    meeting_time = Column(DateTime, nullable=False)
    timezone = Column(String(50), default="UTC")
    duration_minutes = Column(Integer, default=30)
    meeting_link = Column(String(500))  # Zoom/Meet link
    status = Column(String(50), default="pending")  # pending, confirmed, completed, cancelled
    confirmation_sent = Column(Boolean, default=False)
    reminder_sent = Column(Boolean, default=False)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    call = relationship("Call", back_populates="booking")
    contact = relationship("Contact", back_populates="bookings")
