# NSOL BPO Call Assistant

A FastAPI-based call-management prototype for NSOL BPO. The repository combines a scripted voice-agent workflow with Twilio call-management routes, a SQLite-backed application, and dashboard interfaces.

## Included components

- FastAPI service with routes for outbound calls, Twilio webhooks, status callbacks, and media streams
- Scripted LiveKit voice-agent conversation for lead qualification and meeting scheduling
- Dashboard and API modules for contacts, agents, calls, and bookings
- HTML dashboard plus an optional Streamlit interface
- SQLite database setup and sample contacts CSV

**Integration status:** The existing run guide still describes the Twilio media-stream connection to the LiveKit agent as work to complete. Verify the end-to-end audio path before describing the system as a working live voice product.

## Run locally

Install dependencies with `pip install -r requirements.txt`, configure provider credentials in a local `.env` file, then start the FastAPI service using the repository’s startup script or `uvicorn main:app --host 0.0.0.0 --port 8000`. Start the optional dashboard with `streamlit run streamlit_app.py` after the API is available.

Do not use default login credentials for a deployed instance. Replace any sample credentials, rotate provider tokens, and keep `.env` out of version control.

## Stack

Python · FastAPI · LiveKit Agents · Twilio · SQLite · Streamlit · HTML · Tailwind CSS

## Repository relationship

`Lk_Agent_Frontend` currently contains the same source files as this repository. These appear to be duplicate copies of one project, not separate implementations. Consider selecting one canonical repository before featuring the project in a portfolio.

