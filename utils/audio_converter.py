"""
Audio conversion utilities for Twilio Media Streams

Twilio sends audio in μ-law (G.711) format at 8kHz, mono
LiveKit expects PCM16 format at 16kHz or 48kHz

This module handles conversion between these formats.
"""

import audioop
import array
from typing import Optional

from utils.logger import setup_logging

logger = setup_logging()


class AudioConverter:
    """Convert between μ-law and PCM audio formats"""
    
    # Twilio Media Stream audio format
    TWILIO_SAMPLE_RATE = 8000  # 8kHz
    TWILIO_CHANNELS = 1  # Mono
    TWILIO_SAMPLE_WIDTH = 1  # 1 byte per sample (μ-law)
    
    # LiveKit audio format
    LIVEKIT_SAMPLE_RATE = 16000  # 16kHz (or 48000)
    LIVEKIT_CHANNELS = 1  # Mono
    LIVEKIT_SAMPLE_WIDTH = 2  # 2 bytes per sample (PCM16)
    
    @staticmethod
    def mulaw_to_pcm(mulaw_data: bytes, target_sample_rate: int = 16000) -> bytes:
        """
        Convert μ-law audio to PCM16
        
        Args:
            mulaw_data: Raw μ-law encoded audio bytes
            target_sample_rate: Target sample rate (16000 or 48000)
        
        Returns:
            PCM16 audio bytes
        """
        try:
            # Decode μ-law to linear PCM (16-bit)
            pcm_data = audioop.ulaw2lin(mulaw_data, 2)
            
            # Resample if needed (8kHz -> 16kHz or 48kHz)
            if target_sample_rate != AudioConverter.TWILIO_SAMPLE_RATE:
                pcm_data, _ = audioop.ratecv(
                    pcm_data,
                    2,  # sample width (2 bytes for PCM16)
                    1,  # channels (mono)
                    AudioConverter.TWILIO_SAMPLE_RATE,  # input rate
                    target_sample_rate,  # output rate
                    None  # state
                )
            
            return pcm_data
        
        except Exception as e:
            logger.error(f"Error converting μ-law to PCM: {e}")
            return b""
    
    @staticmethod
    def pcm_to_mulaw(pcm_data: bytes, source_sample_rate: int = 16000) -> bytes:
        """
        Convert PCM16 audio to μ-law
        
        Args:
            pcm_data: Raw PCM16 audio bytes
            source_sample_rate: Source sample rate (16000 or 48000)
        
        Returns:
            μ-law encoded audio bytes
        """
        try:
            # Resample to 8kHz if needed
            if source_sample_rate != AudioConverter.TWILIO_SAMPLE_RATE:
                pcm_data, _ = audioop.ratecv(
                    pcm_data,
                    2,  # sample width (2 bytes for PCM16)
                    1,  # channels (mono)
                    source_sample_rate,  # input rate
                    AudioConverter.TWILIO_SAMPLE_RATE,  # output rate (8kHz)
                    None  # state
                )
            
            # Encode linear PCM to μ-law
            mulaw_data = audioop.lin2ulaw(pcm_data, 2)
            
            return mulaw_data
        
        except Exception as e:
            logger.error(f"Error converting PCM to μ-law: {e}")
            return b""
    
    @staticmethod
    def adjust_volume(audio_data: bytes, sample_width: int, factor: float) -> bytes:
        """
        Adjust audio volume
        
        Args:
            audio_data: Raw audio bytes
            sample_width: Sample width in bytes (1 for μ-law, 2 for PCM16)
            factor: Volume factor (1.0 = no change, 2.0 = double volume)
        
        Returns:
            Audio bytes with adjusted volume
        """
        try:
            return audioop.mul(audio_data, sample_width, factor)
        except Exception as e:
            logger.error(f"Error adjusting volume: {e}")
            return audio_data
    
    @staticmethod
    def get_rms_volume(audio_data: bytes, sample_width: int) -> float:
        """
        Get RMS (root mean square) volume level
        
        Args:
            audio_data: Raw audio bytes
            sample_width: Sample width in bytes
        
        Returns:
            RMS volume level (0-32768 for 16-bit audio)
        """
        try:
            return float(audioop.rms(audio_data, sample_width))
        except Exception as e:
            logger.error(f"Error calculating RMS: {e}")
            return 0.0
    
    @staticmethod
    def mix_audio(audio1: bytes, audio2: bytes, sample_width: int) -> bytes:
        """
        Mix two audio streams
        
        Args:
            audio1: First audio stream bytes
            audio2: Second audio stream bytes
            sample_width: Sample width in bytes
        
        Returns:
            Mixed audio bytes
        """
        try:
            # Ensure both streams are the same length
            min_len = min(len(audio1), len(audio2))
            audio1 = audio1[:min_len]
            audio2 = audio2[:min_len]
            
            return audioop.add(audio1, audio2, sample_width)
        except Exception as e:
            logger.error(f"Error mixing audio: {e}")
            return audio1


class AudioBuffer:
    """Buffer for managing audio chunks"""
    
    def __init__(self, max_size: int = 10):
        """
        Initialize audio buffer
        
        Args:
            max_size: Maximum number of chunks to buffer
        """
        self.buffer = []
        self.max_size = max_size
    
    def add(self, audio_chunk: bytes):
        """Add audio chunk to buffer"""
        self.buffer.append(audio_chunk)
        
        # Remove oldest if buffer is full
        if len(self.buffer) > self.max_size:
            self.buffer.pop(0)
    
    def get_all(self) -> bytes:
        """Get all buffered audio as single bytes object"""
        return b"".join(self.buffer)
    
    def clear(self):
        """Clear the buffer"""
        self.buffer.clear()
    
    def is_empty(self) -> bool:
        """Check if buffer is empty"""
        return len(self.buffer) == 0
    
    def size(self) -> int:
        """Get number of chunks in buffer"""
        return len(self.buffer)


# Example usage
if __name__ == "__main__":
    # Test audio conversion
    converter = AudioConverter()
    
    # Simulate μ-law audio from Twilio (empty for testing)
    mulaw_sample = bytes([0] * 160)  # 20ms at 8kHz
    
    # Convert to PCM
    pcm_sample = converter.mulaw_to_pcm(mulaw_sample, target_sample_rate=16000)
    print(f"μ-law size: {len(mulaw_sample)} bytes")
    print(f"PCM16 size: {len(pcm_sample)} bytes")
    
    # Convert back to μ-law
    mulaw_back = converter.pcm_to_mulaw(pcm_sample, source_sample_rate=16000)
    print(f"μ-law back size: {len(mulaw_back)} bytes")
    
    # Test buffer
    buffer = AudioBuffer(max_size=5)
    buffer.add(b"chunk1")
    buffer.add(b"chunk2")
    buffer.add(b"chunk3")
    print(f"Buffer size: {buffer.size()}")
    print(f"Buffered audio: {buffer.get_all()}")
