"""Initialize database and create admin user."""
import sys
from database.connection import init_db, SessionLocal
from models.database import User, Agent
from utils.auth import get_password_hash

def create_admin():
    """Create default admin user and agent."""
    db = SessionLocal()
    try:
        # Check if admin exists
        existing_admin = db.query(User).filter(User.email == "admin@nsolbpo.com").first()
        if existing_admin:
            print("[INFO] Admin user already exists")
            return

        # Create admin user
        admin = User(
            email="admin@nsolbpo.com",
            hashed_password=get_password_hash("admin123"),
            full_name="Admin User",
            is_active=True,
            is_superuser=True
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)
        print("[OK] Admin user created successfully")
        print("    Email: admin@nsolbpo.com")
        print("    Password: admin123")

        # Create default agent (Merideth)
        merideth = Agent(
            name="Merideth",
            voice_id="21m00Tcm4TlvDq8ikWAM",  # ElevenLabs default voice
            is_active=True,
            owner_id=admin.id,
            prompt="You are Merideth, an AI assistant for NSOL BPO services.",
            greeting_messages="Hello, this is Merideth from NSOL BPO.|Hi there, Merideth calling from NSOL BPO.|Good day, this is Merideth with NSOL BPO."
        )
        db.add(merideth)
        db.commit()
        print("[OK] Default agent 'Merideth' created successfully")

    except Exception as e:
        print(f"[ERROR] Failed to create admin: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("========================================")
    print("  NSOL BPO Database Initialization")
    print("========================================")
    print()
    
    print("[1/2] Creating database tables...")
    try:
        init_db()
        print("[OK] Database tables created")
    except Exception as e:
        print(f"[ERROR] Failed to create tables: {str(e)}")
        sys.exit(1)
    
    print()
    print("[2/2] Creating admin user...")
    create_admin()
    
    print()
    print("========================================")
    print("  Initialization Complete!")
    print("========================================")
    print()
    print("Next steps:")
    print("1. Update .env file with your API keys")
    print("2. Run START.bat to start the system")
    print("3. Login at http://localhost:8000/frontend/dashboard.html")
    print()
