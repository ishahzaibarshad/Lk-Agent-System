"""
Quick check that Twilio credentials from .env are loaded and valid.
Run: python check_twilio.py
"""
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root
load_dotenv(Path(__file__).resolve().parent / ".env")

from config.settings import settings

def main():
    print("\n" + "="*50)
    print("  Twilio configuration check")
    print("="*50 + "\n")

    sid = (settings.TWILIO_ACCOUNT_SID or "").strip()
    token = (settings.TWILIO_AUTH_TOKEN or "").strip()
    from_num = (settings.TWILIO_FROM_NUMBER or "").strip()

    ok = True
    if not sid:
        print("[X] TWILIO_ACCOUNT_SID is missing or empty")
        ok = False
    else:
        print("[OK] TWILIO_ACCOUNT_SID is set (" + sid[:6] + "..." + sid[-4:] + ")")

    if not token:
        print("[X] TWILIO_AUTH_TOKEN is missing or empty")
        ok = False
    else:
        print("[OK] TWILIO_AUTH_TOKEN is set (****)")

    if not from_num:
        print("[X] TWILIO_FROM_NUMBER is missing or empty")
        ok = False
    else:
        print("[OK] TWILIO_FROM_NUMBER is set (" + from_num + ")")

    if not ok:
        print("\nAdd the missing values to your .env file and run this script again.")
        print("="*50 + "\n")
        return

    # Try to create Twilio client (validates credentials)
    try:
        from twilio.rest import Client
        client = Client(sid, token)
        # Quick API call to validate
        account = client.api.accounts(sid).fetch()
        print("\n[OK] Twilio credentials are valid. Account: " + account.friendly_name)
    except Exception as e:
        print("\n[X] Twilio credentials appear invalid: " + str(e))
        ok = False

    print("\n" + "="*50)
    if ok:
        print("  Result: Twilio is configured. You can make calls from the dashboard.")
    else:
        print("  Result: Fix the issues above, then try again.")
    print("="*50 + "\n")

if __name__ == "__main__":
    main()
