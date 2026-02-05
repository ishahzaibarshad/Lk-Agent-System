"""
Twilio Service - Handles outbound calls using Twilio Programmable Voice + Media Streams
No SIP configuration needed - uses webhooks and WebSocket Media Streams
"""
import os
import asyncio
import base64
import json
from typing import Optional
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Connect, Stream
from livekit import api, rtc
from livekit.agents import JobContext

from config.settings import settings
from utils.logger import setup_logging
from utils.audio_converter import AudioConverter, AudioBuffer

logger = setup_logging()


class TwilioOutboundService:
    """Service for making outbound calls with Twilio and connecting to LiveKit via Media Streams"""
    
    def __init__(self):
        self.account_sid = settings.TWILIO_ACCOUNT_SID
        self.auth_token = settings.TWILIO_AUTH_TOKEN
        self.from_number = settings.TWILIO_FROM_NUMBER
        
        if not all([self.account_sid, self.auth_token, self.from_number]):
            raise ValueError(
                "Missing required Twilio credentials. Please set TWILIO_ACCOUNT_SID, "
                "TWILIO_AUTH_TOKEN, and TWILIO_FROM_NUMBER in your .env file"
            )
        
        self.client = Client(self.account_sid, self.auth_token)
        logger.info("Twilio Outbound Service initialized")
    
    def place_call(
        self,
        to_number: str,
        webhook_url: str,
        status_callback_url: Optional[str] = None
    ) -> dict:
        """
        Place an outbound call using Twilio Programmable Voice
        
        Args:
            to_number: Phone number to call (E.164 format, e.g., +14155551234)
            webhook_url: Your public webhook URL that will return TwiML with Media Stream
            status_callback_url: Optional URL for call status updates
        
        Returns:
            dict with call_sid and status
        """
        try:
            call = self.client.calls.create(
                to=to_number,
                from_=self.from_number,
                url=webhook_url,
                status_callback=status_callback_url,
                status_callback_event=['initiated', 'ringing', 'answered', 'completed'],
                method='POST'
            )
            
            logger.info(f"Outbound call initiated: {call.sid} to {to_number}")
            
            return {
                "success": True,
                "call_sid": call.sid,
                "status": call.status,
                "to": to_number,
                "from": self.from_number,
            }
        
        except Exception as e:
            logger.error(f"Error placing call: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    def generate_twiml(
        websocket_url: str,
        call_sid: str,
        room_name: Optional[str] = None
    ) -> str:
        """
        Generate TwiML response with bidirectional Media Stream
        
        Args:
            websocket_url: Your WebSocket URL where Twilio will stream audio
            call_sid: Twilio call SID (for tracking)
            room_name: Optional LiveKit room name
        
        Returns:
            TwiML XML string
        """
        response = VoiceResponse()
        
        # Use Connect + Stream for bidirectional audio
        connect = Connect()
        stream = Stream(url=websocket_url)
        
        # Add custom parameters to pass to WebSocket
        stream.parameter(name='call_sid', value=call_sid)
        if room_name:
            stream.parameter(name='room_name', value=room_name)
        
        connect.append(stream)
        response.append(connect)
        
        logger.info(f"Generated TwiML for call {call_sid} with WebSocket URL: {websocket_url}")
        
        return str(response)
    
    def update_call_status(self, call_sid: str, status: str) -> bool:
        """
        Update call status (for internal tracking)
        
        Args:
            call_sid: Twilio call SID
            status: Status to log
        
        Returns:
            bool indicating success
        """
        try:
            logger.info(f"Call {call_sid} status: {status}")
            return True
        except Exception as e:
            logger.error(f"Error updating call status: {str(e)}")
            return False


class TwilioMediaStreamHandler:
    """
    Handles Twilio Media Stream WebSocket connection
    Receives audio from Twilio and sends it to LiveKit
    Receives audio from LiveKit and sends it back to Twilio
    """
    
    def __init__(self, websocket, livekit_room_name: str):
        self.websocket = websocket
        self.livekit_room_name = livekit_room_name
        self.stream_sid = None
        self.call_sid = None
        self.livekit_room = None
        self.livekit_participant = None
        self.audio_track = None
        self.is_connected = False
        
        # Audio conversion and buffering
        self.audio_converter = AudioConverter()
        self.incoming_audio_buffer = AudioBuffer(max_size=10)
        self.outgoing_audio_buffer = AudioBuffer(max_size=10)
        
        logger.info(f"TwilioMediaStreamHandler initialized for room: {livekit_room_name}")
    
    async def handle_connection(self):
        """Main handler for WebSocket connection from Twilio"""
        try:
            logger.info("Waiting for Twilio Media Stream messages...")
            
            async for message in self.websocket.iter_text():
                await self.handle_message(message)
        
        except Exception as e:
            logger.error(f"Error in Media Stream handler: {str(e)}")
        
        finally:
            await self.cleanup()
    
    async def handle_message(self, message: str):
        """Process incoming WebSocket message from Twilio"""
        try:
            data = json.loads(message)
            event_type = data.get("event")
            
            if event_type == "connected":
                logger.info("Twilio Media Stream connected")
            
            elif event_type == "start":
                await self.handle_start(data)
            
            elif event_type == "media":
                await self.handle_media(data)
            
            elif event_type == "stop":
                await self.handle_stop(data)
            
            elif event_type == "dtmf":
                await self.handle_dtmf(data)
        
        except json.JSONDecodeError:
            logger.error(f"Failed to parse message: {message}")
        except Exception as e:
            logger.error(f"Error handling message: {str(e)}")
    
    async def handle_start(self, data: dict):
        """Handle stream start event"""
        self.stream_sid = data["streamSid"]
        self.call_sid = data["start"]["callSid"]
        
        custom_params = data["start"].get("customParameters", {})
        room_override = custom_params.get("room_name")
        
        if room_override:
            self.livekit_room_name = room_override
        
        logger.info(
            f"Stream started - StreamSID: {self.stream_sid}, "
            f"CallSID: {self.call_sid}, Room: {self.livekit_room_name}"
        )
        
        # Connect to LiveKit room
        await self.connect_to_livekit()
    
    async def handle_media(self, data: dict):
        """Handle incoming audio from Twilio"""
        if not self.is_connected or not self.audio_source:
            if not self.is_connected:
                logger.warning("Skipping audio - not connected to LiveKit yet")
            if not self.audio_source:
                logger.warning("Skipping audio - audio source not initialized")
            return
        
        try:
            # Get audio payload (base64 encoded μ-law)
            payload = data["media"]["payload"]
            
            # Decode base64 to get μ-law audio
            mulaw_audio = base64.b64decode(payload)
            
            if len(mulaw_audio) == 0:
                return
            
            # Convert μ-law to PCM16 for LiveKit
            pcm_audio = self.audio_converter.mulaw_to_pcm(
                mulaw_audio,
                target_sample_rate=16000
            )
            
            # Send PCM audio to LiveKit room via audio source
            if len(pcm_audio) > 0:
                # Twilio sends 20ms chunks at 8kHz = 160 bytes μ-law
                # After conversion to 16kHz PCM16 = 320 samples = 640 bytes
                samples_per_channel = len(pcm_audio) // 2  # PCM16 = 2 bytes per sample
                
                # Create audio frame
                frame = rtc.AudioFrame(
                    data=pcm_audio,
                    sample_rate=16000,
                    num_channels=1,
                    samples_per_channel=samples_per_channel
                )
                
                # Capture frame to audio source
                await self.audio_source.capture_frame(frame)
                logger.info(f"📤 Sent to Agent: {len(mulaw_audio)}b μ-law → {len(pcm_audio)}b PCM ({samples_per_channel} samples)")
            
        except Exception as e:
            logger.error(f"Error handling media: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
    
    async def handle_stop(self, data: dict):
        """Handle stream stop event"""
        logger.info(f"Stream stopped - StreamSID: {self.stream_sid}")
        await self.cleanup()
    
    async def handle_dtmf(self, data: dict):
        """Handle DTMF digit press"""
        digit = data.get("dtmf", {}).get("digit")
        logger.info(f"DTMF received: {digit}")
    
    async def connect_to_livekit(self):
        """Connect to LiveKit room as a participant"""
        try:
            # Generate access token for this call
            token = api.AccessToken(
                settings.LIVEKIT_API_KEY,
                settings.LIVEKIT_API_SECRET
            )
            token.with_identity(f"twilio-{self.call_sid}")
            token.with_name(f"Twilio Call {self.call_sid}")
            token.with_grants(api.VideoGrants(
                room_join=True,
                room=self.livekit_room_name,
            ))
            
            access_token = token.to_jwt()
            
            logger.info(f"Generated LiveKit token for room: {self.livekit_room_name}")
            
            # Create and connect to LiveKit Room
            self.livekit_room = rtc.Room()
            
            logger.info(f"Connecting to LiveKit room: {self.livekit_room_name}")
            await self.livekit_room.connect(settings.LIVEKIT_URL, access_token)
            logger.info(f"Connected to LiveKit room: {self.livekit_room_name}")
            
            # Create audio track source for caller audio
            self.audio_source = rtc.AudioSource(16000, 1)  # 16kHz, mono
            self.audio_track = rtc.LocalAudioTrack.create_audio_track(
                "caller-audio",
                self.audio_source
            )
            
            # Publish the track with microphone source type so agent picks it up
            options = rtc.TrackPublishOptions()
            options.source = rtc.TrackSource.SOURCE_MICROPHONE  # Identify as microphone
            
            await self.livekit_room.local_participant.publish_track(
                self.audio_track,
                options
            )
            logger.info("Published caller audio track as MICROPHONE source to LiveKit")
            
            # Listen for agent audio
            @self.livekit_room.on("track_subscribed")
            def on_track_subscribed(track, publication, participant):
                if track.kind == rtc.TrackKind.KIND_AUDIO:
                    logger.info(f"Subscribed to audio track from {participant.identity}")
                    asyncio.create_task(self.receive_agent_audio(track))
            
            self.is_connected = True
            logger.info(f"✅ LiveKit room connected - Agent should join now!")
        
        except Exception as e:
            logger.error(f"Error connecting to LiveKit: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            self.is_connected = False
    
    async def send_audio_to_twilio(self, pcm_audio: bytes, sample_rate: int = 16000):
        """
        Send audio back to Twilio (for bidirectional communication)
        
        Args:
            pcm_audio: PCM16 audio data from LiveKit agent
            sample_rate: Sample rate of the PCM audio (16000 or 48000)
        """
        try:
            if not self.stream_sid or not self.websocket:
                logger.warning("Cannot send audio - stream not ready")
                return
            
            # Convert PCM to μ-law for Twilio
            mulaw_audio = self.audio_converter.pcm_to_mulaw(
                pcm_audio,
                source_sample_rate=sample_rate
            )
            
            if len(mulaw_audio) == 0:
                return
            
            # Base64 encode for WebSocket transmission
            payload_base64 = base64.b64encode(mulaw_audio).decode('utf-8')
            
            message = {
                "event": "media",
                "streamSid": self.stream_sid,
                "media": {
                    "payload": payload_base64
                }
            }
            
            await self.websocket.send_text(json.dumps(message))
            logger.info(f"📥 Sent to Caller: {len(pcm_audio)}b PCM → {len(mulaw_audio)}b μ-law")
        
        except Exception as e:
            logger.error(f"Error sending audio to Twilio: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
    
    async def send_mark(self, mark_name: str):
        """Send a mark message to Twilio (for synchronization)"""
        try:
            message = {
                "event": "mark",
                "streamSid": self.stream_sid,
                "mark": {
                    "name": mark_name
                }
            }
            await self.websocket.send_text(json.dumps(message))
        except Exception as e:
            logger.error(f"Error sending mark: {str(e)}")
    
    async def cleanup(self):
        """Clean up resources"""
        logger.info(f"Cleaning up Media Stream handler for {self.call_sid}")
        
        self.is_connected = False
        
        # Disconnect from LiveKit room
        if self.livekit_room:
            await self.livekit_room.disconnect()
            logger.info("Disconnected from LiveKit room")
        
        logger.info("Media Stream handler cleanup complete")
    
    async def receive_agent_audio(self, track: rtc.RemoteAudioTrack):
        """Receive audio from LiveKit agent and send to Twilio"""
        try:
            async for event in rtc.AudioStream(track):
                if isinstance(event, rtc.AudioFrameEvent):
                    frame = event.frame
                    
                    # Convert frame data to bytes
                    pcm_audio = bytes(frame.data)
                    
                    # Send to Twilio (will convert to μ-law)
                    await self.send_audio_to_twilio(
                        pcm_audio,
                        sample_rate=frame.sample_rate
                    )
        except Exception as e:
            logger.error(f"Error receiving agent audio: {str(e)}")
