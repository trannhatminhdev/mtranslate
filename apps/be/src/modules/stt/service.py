"""
Speech-to-Text service with pluggable providers.

Supports:
- OpenAI Whisper API (cloud)
- Deepgram API (cloud)
- faster-whisper (local, requires GPU)
"""

import io
from abc import ABC, abstractmethod

from common.config import settings


class STTProvider(ABC):
    """Base class for STT providers."""

    @abstractmethod
    async def transcribe(self, audio_data: bytes, language: str = "auto") -> dict:
        """
        Transcribe audio data to text.

        Args:
            audio_data: Raw PCM audio bytes (16kHz, mono, s16le)
            language: Source language code or "auto" for detection

        Returns:
            dict with keys: text, language, confidence, is_final
        """
        pass

    @abstractmethod
    async def transcribe_stream(self, audio_chunk: bytes, language: str = "auto"):
        """
        Process a streaming audio chunk.
        Yields partial transcripts as they become available.
        """
        pass


class OpenAISTT(STTProvider):
    """OpenAI Whisper API provider."""

    def __init__(self):
        from openai import AsyncOpenAI
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def transcribe(self, audio_data: bytes, language: str = "auto") -> dict:
        """Transcribe audio using OpenAI Whisper API."""
        # Convert raw PCM to WAV in memory
        wav_buffer = self._pcm_to_wav(audio_data)

        kwargs = {"model": "whisper-1", "file": ("audio.wav", wav_buffer, "audio/wav")}
        if language != "auto":
            kwargs["language"] = language

        response = await self.client.audio.transcriptions.create(**kwargs)

        return {
            "text": response.text,
            "language": language,
            "confidence": 1.0,
            "is_final": True,
        }

    async def transcribe_stream(self, audio_chunk: bytes, language: str = "auto"):
        """OpenAI doesn't support true streaming, accumulate and transcribe."""
        # For streaming, we accumulate chunks and transcribe when enough data
        result = await self.transcribe(audio_chunk, language)
        yield result

    @staticmethod
    def _pcm_to_wav(pcm_data: bytes, sample_rate: int = 16000, channels: int = 1) -> io.BytesIO:
        """Convert raw PCM bytes to WAV format in memory."""
        import struct

        buffer = io.BytesIO()
        data_size = len(pcm_data)

        # WAV header
        buffer.write(b"RIFF")
        buffer.write(struct.pack("<I", 36 + data_size))
        buffer.write(b"WAVE")
        buffer.write(b"fmt ")
        buffer.write(struct.pack("<I", 16))  # chunk size
        buffer.write(struct.pack("<H", 1))  # PCM format
        buffer.write(struct.pack("<H", channels))
        buffer.write(struct.pack("<I", sample_rate))
        buffer.write(struct.pack("<I", sample_rate * channels * 2))  # byte rate
        buffer.write(struct.pack("<H", channels * 2))  # block align
        buffer.write(struct.pack("<H", 16))  # bits per sample
        buffer.write(b"data")
        buffer.write(struct.pack("<I", data_size))
        buffer.write(pcm_data)

        buffer.seek(0)
        return buffer


class DeepgramSTT(STTProvider):
    """Deepgram API provider (placeholder for future implementation)."""

    async def transcribe(self, audio_data: bytes, language: str = "auto") -> dict:
        raise NotImplementedError("Deepgram STT not yet implemented")

    async def transcribe_stream(self, audio_chunk: bytes, language: str = "auto"):
        raise NotImplementedError("Deepgram STT streaming not yet implemented")


def get_stt_provider() -> STTProvider:
    """Factory function to get the configured STT provider."""
    providers = {
        "openai": OpenAISTT,
        "deepgram": DeepgramSTT,
    }
    provider_cls = providers.get(settings.STT_PROVIDER)
    if not provider_cls:
        raise ValueError(f"Unknown STT provider: {settings.STT_PROVIDER}")
    return provider_cls()
