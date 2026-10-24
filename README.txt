========================================
NSOL BPO AI CALL ASSISTANT
========================================

QUICK START
-----------
1. Double-click START.bat to start the system
2. Wait for browser to open (http://localhost:8000/frontend/dashboard.html)
3. Do not use default login credentials. Configure a unique administrator credential using a verified application setup path before any deployment. Verify account provisioning in the application code.\n4. To stop: Double-click STOP.bat

SYSTEM COMPONENTS
-----------------
- FastAPI Backend (Port 8000)
- LiveKit Agent (Merideth - BPO Assistant)
- Twilio Voice Integration
- SQLite Database (nsol_bpo.db)
- Web Dashboard (HTML/JS/Tailwind CSS)

KEY FILES
---------
- main.py: Core application with LiveKit agent
- .env: Configuration and API keys
- requirements.txt: Python dependencies
- frontend/dashboard.html: Main dashboard
- frontend/demo_dashboard.html: Demo mode
- sample_contacts.csv: Example contacts for import

REQUIRED CREDENTIALS (.env file)
---------------------------------
- Twilio: TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER
- LiveKit: LIVEKIT_API_KEY, LIVEKIT_API_SECRET, LIVEKIT_URL
- ElevenLabs: ELEVENLABS_API_KEY
- Deepgram: DEEPGRAM_API_KEY
- OpenAI: OPENAI_API_KEY

FEATURES
--------
1. Dashboard: View stats, manage agents, contacts, calls
2. Contacts: Add manually or import CSV
3. Make Calls: Initiate outbound calls via Twilio
4. Call History: View transcripts, recordings, outcomes
5. Bookings: Manual and automatic appointment scheduling
6. Demo Mode: Impressive UI for manager presentations

REQUIREMENTS
------------
- Python 3.11+
- Ngrok (for Twilio webhooks)
- Active internet connection
- API keys for all services

TROUBLESHOOTING
---------------
- If port 8000 is busy: Run STOP.bat first
- If dashboard doesn't load: Check if FastAPI started successfully
- For call issues: Verify .env has all Twilio credentials
- Database issues: Delete nsol_bpo.db and restart (creates fresh DB)

SUPPORT
-------
Check HOW_TO_RUN.md for detailed setup instructions.
