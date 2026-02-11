import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root (parent of config/)
_env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=_env_path)


class Settings:
    """
    Configuration settings for Merideth Cold Calling System.
    
    Required environment variables:
    - LIVEKIT_URL: LiveKit server URL
    - LIVEKIT_API_KEY: LiveKit API key
    - LIVEKIT_API_SECRET: LiveKit API secret
    - ELEVENLABS_API_KEY: ElevenLabs API key for STT/TTS
    
    Optional environment variables:
    - OPENAI_API_KEY: OpenAI API key for fallback Q&A
    - OPENAI_MODEL: OpenAI model to use (default: gpt-4o-mini)
    - ELEVEN_VOICE_ID: ElevenLabs voice ID (default: bIHbv24MWmeRgasZH58o)
    - DATABASE_URL: Database connection string
    - DEBUG: Enable debug mode (default: true)
    - HOST: Server host (default: 0.0.0.0)
    - PORT: Server port (default: 8000)
    """
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///merideth.db")
    
    # LiveKit Configuration
    LIVEKIT_URL: str = os.getenv("LIVEKIT_URL", "wss://localhost:7880")
    LIVEKIT_API_KEY: str = os.getenv("LIVEKIT_API_KEY", "devkey")
    LIVEKIT_API_SECRET: str = os.getenv("LIVEKIT_API_SECRET", "secret")
    
    # Deepgram Configuration (STT)
    DEEPGRAM_API_KEY: str = os.getenv("DEEPGRAM_API_KEY", "")
    
    # ElevenLabs Configuration (TTS)
    ELEVEN_API_KEY: str = os.getenv("ELEVEN_API_KEY", "")
    ELEVEN_VOICE_ID: str = os.getenv("ELEVEN_VOICE_ID", "bIHbv24MWmeRgasZH58o")
    
    # OpenAI Configuration (LLM for fallback Q&A)
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    # Twilio Configuration (for outbound calls)
    TWILIO_ACCOUNT_SID: str = (os.getenv("TWILIO_ACCOUNT_SID") or "").strip()
    TWILIO_AUTH_TOKEN: str = (os.getenv("TWILIO_AUTH_TOKEN") or "").strip()
    TWILIO_API_KEY_SID: str = (os.getenv("TWILIO_API_KEY_SID") or "").strip()
    TWILIO_API_KEY_SECRET: str = (os.getenv("TWILIO_API_KEY_SECRET") or "").strip()
    TWILIO_FROM_NUMBER: str = (os.getenv("TWILIO_FROM_NUMBER") or "").strip()
    LIVEKIT_SIP_URI: str = os.getenv("LIVEKIT_SIP_URI", "")
    # Optional: set in .env for demo so frontend never prompts for Ngrok URL
    NGROK_BASE_URL: str = (os.getenv("NGROK_BASE_URL") or "").strip()
    
    # App Configuration
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # Authentication
    SECRET_KEY: str = os.getenv("SECRET_KEY", "nsol-bpo-secret-key-change-in-production-2024")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "10080"))  # 7 days
    
    # Monitoring
    METRICS_PORT: int = int(os.getenv("METRICS_PORT", "9090"))


settings = Settings()
