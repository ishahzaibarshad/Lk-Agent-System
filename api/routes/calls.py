"""Call management API routes."""
from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from database.connection import get_db
from models.database import User, Call, Agent
from models.schemas import CallCreate, CallUpdate, CallResponse, CallListResponse
from utils.auth import get_current_user

router = APIRouter(prefix="/api/calls", tags=["Calls"])

@router.post("", response_model=CallResponse, status_code=status.HTTP_201_CREATED)
def create_call_record(
    call_data: CallCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new call record."""
    # Verify agent belongs to user
    agent = db.query(Agent).filter(
        Agent.id == call_data.agent_id,
        Agent.owner_id == current_user.id
    ).first()
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    
    new_call = Call(
        agent_id=call_data.agent_id,
        contact_id=call_data.contact_id,
        status="initiated"
    )
    db.add(new_call)
    db.commit()
    db.refresh(new_call)
    return new_call

@router.get("", response_model=CallListResponse)
def list_calls(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    outcome: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all calls for the current user."""
    query = db.query(Call).join(Agent).filter(Agent.owner_id == current_user.id)
    
    if status:
        query = query.filter(Call.status == status)
    if outcome:
        query = query.filter(Call.outcome == outcome)
    
    total = query.count()
    calls = query.order_by(Call.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "calls": calls
    }

@router.get("/{call_id}", response_model=CallResponse)
def get_call(
    call_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific call."""
    call = db.query(Call).join(Agent).filter(
        Call.id == call_id,
        Agent.owner_id == current_user.id
    ).first()
    
    if not call:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Call not found"
        )
    return call

@router.put("/{call_id}", response_model=CallResponse)
def update_call(
    call_id: int,
    call_data: CallUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a call."""
    call = db.query(Call).join(Agent).filter(
        Call.id == call_id,
        Agent.owner_id == current_user.id
    ).first()
    
    if not call:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Call not found"
        )
    
    # Update fields
    for field, value in call_data.model_dump(exclude_unset=True).items():
        setattr(call, field, value)
    
    db.commit()
    db.refresh(call)
    return call

@router.delete("/{call_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_call(
    call_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a call."""
    call = db.query(Call).join(Agent).filter(
        Call.id == call_id,
        Agent.owner_id == current_user.id
    ).first()
    
    if not call:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Call not found"
        )
    
    db.delete(call)
    db.commit()
    return None
