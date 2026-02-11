"""Booking management API routes."""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from database.connection import get_db
from models.database import User, Booking, Call, Agent, Contact
from models.schemas import BookingCreate, BookingUpdate, BookingResponse, BookingListResponse
from utils.auth import get_current_user

router = APIRouter(prefix="/api/bookings", tags=["Bookings"])

@router.post("", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(
    booking_data: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new booking."""
    # If call_id is provided, verify call exists and belongs to user
    if booking_data.call_id:
        call = db.query(Call).join(Agent).filter(
            Call.id == booking_data.call_id,
            Agent.owner_id == current_user.id
        ).first()
        
        if not call:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Call not found"
            )
        
        # Check if booking already exists for this call
        existing = db.query(Booking).filter(Booking.call_id == booking_data.call_id).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Booking already exists for this call"
            )
    else:
        # Manual booking - verify contact exists and belongs to user
        contact = db.query(Contact).filter(
            Contact.id == booking_data.contact_id,
            Contact.owner_id == current_user.id
        ).first()
        
        if not contact:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contact not found"
            )
    
    new_booking = Booking(**booking_data.model_dump())
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking

@router.get("", response_model=BookingListResponse)
def list_bookings(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all bookings for the current user."""
    # Join through Contact to filter by owner
    query = db.query(Booking).join(Contact).filter(Contact.owner_id == current_user.id)
    
    if status:
        query = query.filter(Booking.status == status)
    
    total = query.count()
    bookings = query.order_by(Booking.meeting_time.desc()).offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "bookings": bookings
    }

@router.get("/{booking_id}", response_model=BookingResponse)
def get_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific booking."""
    booking = db.query(Booking).join(Contact).filter(
        Booking.id == booking_id,
        Contact.owner_id == current_user.id
    ).first()
    
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    return booking

@router.put("/{booking_id}", response_model=BookingResponse)
def update_booking(
    booking_id: int,
    booking_data: BookingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a booking."""
    booking = db.query(Booking).join(Contact).filter(
        Booking.id == booking_id,
        Contact.owner_id == current_user.id
    ).first()
    
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    # Update fields
    for field, value in booking_data.model_dump(exclude_unset=True).items():
        setattr(booking, field, value)
    
    db.commit()
    db.refresh(booking)
    return booking

@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a booking."""
    booking = db.query(Booking).join(Contact).filter(
        Booking.id == booking_id,
        Contact.owner_id == current_user.id
    ).first()
    
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    db.delete(booking)
    db.commit()
    return None
