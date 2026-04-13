"""
Text-to-Speech service with pluggable providers.

Supports:
- OpenAI TTS API (cloud, high quality)
- Edge TTS (free, Microsoft voices)
"""

from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator

from common.config import settings

# Available voices per provider
OPENAI_VOICES = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]


class TTSProvider(ABC):
    """Base class for TTS providers."""

    @abstractmethod
    async def synthesize(self, text: str, voice: str = "default") -> bytes:
        """
        Synthesize text to audio.

        Args:
            text: Text to convert to speech
            voice: Voice ID to use

        Returns:
            Raw PCM audio bytes (24kHz, mono, s16le)
        """
        pass

    @abstractmethod
    async def synthesize_stream(self, text: str, voice: str = "default") -> AsyncGenerator[bytes, None]:
        """
        Stream synthesized audio chunks.
        Yields PCM audio chunks as they are generated.
        """
        pass


class OpenAITTS(TTSProvider):
    """OpenAI TTS API provider."""

    def __init__(self):
        from openai import AsyncOpenAI
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def synthesize(self, text: str, voice: str = "alloy") -> bytes:
        """Synthesize text using OpenAI TTS."""
        if not text.strip():
            return b""

        if voice not in OPENAI_VOICES:
            voice = "alloy"

        response = await self.client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text,
            response_format="pcm",  # Raw PCM 24kHz mono s16le
        )
        return response.content

    async def synthesize_stream(self, text: str, voice: str = "alloy") -> AsyncGenerator[bytes, None]:
        """Stream synthesized audio from OpenAI TTS."""
        if not text.strip():
            return

        if voice not in OPENAI_VOICES:
            voice = "alloy"

        async with self.client.audio.speech.with_streaming_response.create(
            model="tts-1",
            voice=voice,
            input=text,
            response_format="pcm",
        ) as response:
            async for chunk in response.iter_bytes(chunk_size=4096):
                yield chunk


class EdgeTTS(TTSProvider):
    """Microsoft Edge TTS provider (free)."""

    async def synthesize(self, text: str, voice: str = "en-US-AriaNeural") -> bytes:
        """Synthesize text using Edge TTS."""
        import edge_tts

        communicate = edge_tts.Communicate(text, voice)
        audio_data = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]
        return audio_data

    async def synthesize_stream(self, text: str, voice: str = "en-US-AriaNeural") -> AsyncGenerator[bytes, None]:
        """Stream synthesized audio from Edge TTS."""
        import edge_tts

        communicate = edge_tts.Communicate(text, voice)
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                yield chunk["data"]


def get_tts_provider() -> TTSProvider:
    """Factory function to get the configured TTS provider."""
    providers = {
        "openai": OpenAITTS,
        "edge_tts": EdgeTTS,
    }
    provider_cls = providers.get(settings.TTS_PROVIDER)
    if not provider_cls:
        raise ValueError(f"Unknown TTS provider: {settings.TTS_PROVIDER}")
    return provider_cls()
