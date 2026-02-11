"""Pydantic schemas for request/response validation."""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Agent Schemas
class AgentBase(BaseModel):
    name: str
    voice_id: Optional[str] = None
    prompt: Optional[str] = None
    greeting_messages: Optional[str] = None
    is_active: bool = True

class AgentCreate(AgentBase):
    pass

class AgentUpdate(BaseModel):
    name: Optional[str] = None
    voice_id: Optional[str] = None
    prompt: Optional[str] = None
    greeting_messages: Optional[str] = None
    is_active: Optional[bool] = None

class AgentResponse(AgentBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class AgentListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    agents: List[AgentResponse]

# Contact Schemas
class ContactBase(BaseModel):
    name: str
    phone: str
    email: Optional[str] = None
    company: Optional[str] = None
    notes: Optional[str] = None
    tags: Optional[str] = None
    timezone: Optional[str] = "UTC"

class ContactCreate(ContactBase):
    pass

class ContactUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    company: Optional[str] = None
    notes: Optional[str] = None
    tags: Optional[str] = None
    timezone: Optional[str] = None

class ContactResponse(ContactBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ContactListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    contacts: List[ContactResponse]

class ContactImportResult(BaseModel):
    success: int
    failed: int
    errors: List[str]

# Call Schemas
class CallBase(BaseModel):
    agent_id: int
    contact_id: int
    status: str = "initiated"
    outcome: Optional[str] = None
    sentiment: Optional[str] = None
    notes: Optional[str] = None

class CallCreate(BaseModel):
    agent_id: int
    contact_id: int
    ngrok_url: Optional[str] = None

class CallUpdate(BaseModel):
    status: Optional[str] = None
    duration: Optional[int] = None
    transcript: Optional[str] = None
    recording_url: Optional[str] = None
    outcome: Optional[str] = None
    sentiment: Optional[str] = None
    notes: Optional[str] = None
    ended_at: Optional[datetime] = None

class CallResponse(CallBase):
    id: int
    call_sid: Optional[str] = None
    duration: Optional[int] = None
    transcript: Optional[str] = None
    recording_url: Optional[str] = None
    started_at: datetime
    ended_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class CallListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    calls: List[CallResponse]

# Booking Schemas
class BookingBase(BaseModel):
    call_id: Optional[int] = None  # Optional for manual bookings
    contact_id: int
    meeting_time: datetime
    timezone: str = "UTC"
    duration_minutes: int = 30
    meeting_link: Optional[str] = None
    status: str = "pending"
    notes: Optional[str] = None

class BookingCreate(BookingBase):
    pass

class BookingUpdate(BaseModel):
    meeting_time: Optional[datetime] = None
    timezone: Optional[str] = None
    duration_minutes: Optional[int] = None
    meeting_link: Optional[str] = None
    status: Optional[str] = None
    confirmation_sent: Optional[bool] = None
    reminder_sent: Optional[bool] = None
    notes: Optional[str] = None

class BookingResponse(BookingBase):
    id: int
    confirmation_sent: bool
    reminder_sent: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class BookingListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    bookings: List[BookingResponse]

# Dashboard Schemas
class DashboardStats(BaseModel):
    total_agents: int
    total_contacts: int
    total_calls: int
    total_bookings: int
    calls_today: int
    bookings_this_week: int
    active_calls: int
    success_rate: float

# Outbound Call Schema
class OutboundCallRequest(BaseModel):
    agent_id: int
    contact_id: int
    ngrok_url: str = Field(..., description="Ngrok HTTPS URL for webhooks")
