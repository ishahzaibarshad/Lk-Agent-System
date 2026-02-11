"""Agent management API routes."""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from database.connection import get_db
from models.database import User, Agent
from models.schemas import AgentCreate, AgentUpdate, AgentResponse, AgentListResponse
from utils.auth import get_current_user

router = APIRouter(prefix="/api/agents", tags=["Agents"])

@router.post("", response_model=AgentResponse, status_code=status.HTTP_201_CREATED)
def create_agent(
    agent_data: AgentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new agent."""
    new_agent = Agent(
        **agent_data.model_dump(),
        owner_id=current_user.id
    )
    db.add(new_agent)
    db.commit()
    db.refresh(new_agent)
    return new_agent

@router.get("", response_model=AgentListResponse)
def list_agents(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all agents for the current user."""
    query = db.query(Agent).filter(Agent.owner_id == current_user.id)
    
    if is_active is not None:
        query = query.filter(Agent.is_active == is_active)
    
    total = query.count()
    agents = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "agents": agents
    }

@router.get("/{agent_id}", response_model=AgentResponse)
def get_agent(
    agent_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific agent."""
    agent = db.query(Agent).filter(
        Agent.id == agent_id,
        Agent.owner_id == current_user.id
    ).first()
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    return agent

@router.put("/{agent_id}", response_model=AgentResponse)
def update_agent(
    agent_id: int,
    agent_data: AgentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update an agent."""
    agent = db.query(Agent).filter(
        Agent.id == agent_id,
        Agent.owner_id == current_user.id
    ).first()
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    
    # Update fields
    for field, value in agent_data.model_dump(exclude_unset=True).items():
        setattr(agent, field, value)
    
    db.commit()
    db.refresh(agent)
    return agent

@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_agent(
    agent_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete an agent."""
    agent = db.query(Agent).filter(
        Agent.id == agent_id,
        Agent.owner_id == current_user.id
    ).first()
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    
    db.delete(agent)
    db.commit()
    return None
