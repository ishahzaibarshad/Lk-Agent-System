"""Dashboard API routes."""
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from database.connection import get_db
from models.database import User, Agent, Contact, Call, Booking
from models.schemas import DashboardStats
from utils.auth import get_current_user

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

@router.get("/stats", response_model=DashboardStats)
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get dashboard statistics for the current user."""
    # Total counts
    total_agents = db.query(Agent).filter(Agent.owner_id == current_user.id).count()
    total_contacts = db.query(Contact).filter(Contact.owner_id == current_user.id).count()
    total_calls = db.query(Call).join(Agent).filter(Agent.owner_id == current_user.id).count()
    total_bookings = db.query(Booking).join(Contact).filter(Contact.owner_id == current_user.id).count()
    
    # Calls today
    today = datetime.utcnow().date()
    calls_today = db.query(Call).join(Agent).filter(
        Agent.owner_id == current_user.id,
        func.date(Call.created_at) == today
    ).count()
    
    # Bookings this week
    week_start = datetime.utcnow() - timedelta(days=7)
    bookings_this_week = db.query(Booking).join(Contact).filter(
        Contact.owner_id == current_user.id,
        Booking.created_at >= week_start
    ).count()
    
    # Active calls (in_progress status)
    active_calls = db.query(Call).join(Agent).filter(
        Agent.owner_id == current_user.id,
        Call.status == "in_progress"
    ).count()
    
    # Success rate (completed calls with positive outcome)
    completed_calls = db.query(Call).join(Agent).filter(
        Agent.owner_id == current_user.id,
        Call.status == "completed"
    ).count()
    
    successful_calls = db.query(Call).join(Agent).filter(
        Agent.owner_id == current_user.id,
        Call.status == "completed",
        Call.outcome.in_(["qualified", "callback"])
    ).count()
    
    success_rate = (successful_calls / completed_calls * 100) if completed_calls > 0 else 0.0
    
    return {
        "total_agents": total_agents,
        "total_contacts": total_contacts,
        "total_calls": total_calls,
        "total_bookings": total_bookings,
        "calls_today": calls_today,
        "bookings_this_week": bookings_this_week,
        "active_calls": active_calls,
        "success_rate": round(success_rate, 2)
    }
