"""
Outbound call handler for Twilio → LiveKit agent.

Use this to place an outbound call from your Twilio number to a phone number.
When the callee answers, Twilio connects them to your LiveKit agent via SIP.

Usage:
  python call_livekit.py +1234567890

Ensure Agent.py is running and LIVEKIT_SIP_URI is set in .env.
"""
import os
import sys
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv(".env")

ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
FROM_NUMBER = os.environ["TWILIO_FROM_NUMBER"]
LIVEKIT_SIP_URI = os.environ["LIVEKIT_SIP_URI"]

# Prefer Auth Token; fall back to API Key for REST
AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
if AUTH_TOKEN:
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
else:
    client = Client(
        os.environ["TWILIO_API_KEY_SID"],
        os.environ["TWILIO_API_KEY_SECRET"],
        ACCOUNT_SID,
    )


def get_twiml_for_livekit() -> str:
    """Build TwiML that dials LiveKit SIP when the outbound call is answered."""
    # answerOnBridge: don't answer the callee until LiveKit answers (avoids drop).
    # timeout: how long to wait for LiveKit to answer (seconds).
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Dial callerId="{FROM_NUMBER}" timeout="90" answerOnBridge="true">
    <Sip>{LIVEKIT_SIP_URI}</Sip>
  </Dial>
</Response>""".strip()




def make_outbound_call(to_number: str, use_url: str | None = None):
    """
    Call handler: place an outbound call from Twilio to to_number.
    When the callee answers, they are connected to the LiveKit agent via SIP.

    If use_url is set (e.g. your webhook URL), Twilio will request that URL
    when the call is answered and use the returned TwiML. Otherwise uses
    inline TwiML.
    """
    kwargs = {"to": to_number, "from_": FROM_NUMBER}
    if use_url:
        kwargs["url"] = use_url
    else:
        kwargs["twiml"] = get_twiml_for_livekit()
    call = client.calls.create(**kwargs)
    print("Call started")
    print("Call SID:", call.sid)
    return call


def run_webhook_server(host: str = "0.0.0.0", port: int = 5000):
    """Run a small HTTP server that returns TwiML for /voice (for url= in Twilio)."""
    try:
        from flask import Flask, Response
    except ImportError:
        print("Install flask to use the webhook server: pip install flask")
        sys.exit(1)
    app = Flask(__name__)

    @app.route("/voice", methods=["GET", "POST"])
    def voice():
        twiml = get_twiml_for_livekit()
        return Response(twiml, mimetype="application/xml")

    print(f"Call handler webhook: http://{host}:{port}/voice")
    app.run(host=host, port=port)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python call_livekit.py <to_number>     # make outbound call")
        print("  python call_livekit.py serve [port]    # run webhook server for url=")
        print("Example: python call_livekit.py +441234567890")
        sys.exit(1)
    if sys.argv[1].lower() == "serve":
        port = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
        run_webhook_server(port=port)
    else:
        make_outbound_call(sys.argv[1])
