"""Contact management API routes."""
import csv
import io
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.orm import Session

from database.connection import get_db
from models.database import User, Contact
from models.schemas import ContactCreate, ContactUpdate, ContactResponse, ContactListResponse, ContactImportResult
from utils.auth import get_current_user

router = APIRouter(prefix="/api/contacts", tags=["Contacts"])

@router.post("", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
def create_contact(
    contact_data: ContactCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new contact."""
    new_contact = Contact(
        **contact_data.model_dump(),
        owner_id=current_user.id
    )
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact

@router.get("", response_model=ContactListResponse)
def list_contacts(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all contacts for the current user."""
    query = db.query(Contact).filter(Contact.owner_id == current_user.id)
    
    if search:
        query = query.filter(
            (Contact.name.ilike(f"%{search}%")) |
            (Contact.email.ilike(f"%{search}%")) |
            (Contact.phone.ilike(f"%{search}%")) |
            (Contact.company.ilike(f"%{search}%"))
        )
    
    total = query.count()
    contacts = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "contacts": contacts
    }

@router.get("/{contact_id}", response_model=ContactResponse)
def get_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific contact."""
    contact = db.query(Contact).filter(
        Contact.id == contact_id,
        Contact.owner_id == current_user.id
    ).first()
    
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )
    return contact

@router.put("/{contact_id}", response_model=ContactResponse)
def update_contact(
    contact_id: int,
    contact_data: ContactUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a contact."""
    contact = db.query(Contact).filter(
        Contact.id == contact_id,
        Contact.owner_id == current_user.id
    ).first()
    
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )
    
    # Update fields
    for field, value in contact_data.model_dump(exclude_unset=True).items():
        setattr(contact, field, value)
    
    db.commit()
    db.refresh(contact)
    return contact

@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a contact."""
    contact = db.query(Contact).filter(
        Contact.id == contact_id,
        Contact.owner_id == current_user.id
    ).first()
    
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )
    
    db.delete(contact)
    db.commit()
    return None

@router.post("/import/csv", response_model=ContactImportResult)
async def import_contacts_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Import contacts from CSV file."""
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be a CSV"
        )
    
    contents = await file.read()
    csv_text = contents.decode('utf-8')
    csv_reader = csv.DictReader(io.StringIO(csv_text))
    
    success_count = 0
    failed_count = 0
    errors = []
    
    for row_num, row in enumerate(csv_reader, start=2):
        try:
            # Validate required fields
            if not row.get('name') or not row.get('phone'):
                errors.append(f"Row {row_num}: Missing required fields (name, phone)")
                failed_count += 1
                continue
            
            # Create contact
            contact = Contact(
                name=row['name'],
                phone=row['phone'],
                email=row.get('email', ''),
                company=row.get('company', ''),
                notes=row.get('notes', ''),
                tags=row.get('tags', ''),
                timezone=row.get('timezone', 'UTC'),
                owner_id=current_user.id
            )
            db.add(contact)
            success_count += 1
        except Exception as e:
            errors.append(f"Row {row_num}: {str(e)}")
            failed_count += 1
    
    db.commit()
    
    return {
        "success": success_count,
        "failed": failed_count,
        "errors": errors[:10]  # Limit to first 10 errors
    }
