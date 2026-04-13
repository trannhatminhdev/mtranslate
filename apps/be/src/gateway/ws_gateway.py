"""
WebSocket Gateway for real-time voice translation.

Handles the full pipeline:
  Client Audio → STT → Translation → TTS → Client Audio

Protocol:
  - Client sends JSON control messages and binary audio frames
  - Server sends JSON status messages and binary translated audio frames
"""

import asyncio
import json
import struct
import time
import traceback

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from modules.stt.service import get_stt_provider
from modules.translation.service import get_translation_provider
from modules.tts.service import get_tts_provider

router = APIRouter()


class TranslationSession:
    """Manages a single translation WebSocket session."""

    def __init__(self, websocket: WebSocket):
        self.ws = websocket
        self.source_lang: str = "vi"
        self.target_lang: str = "en"
        self.context: str = ""
        self.voice: str = "alloy"
        self.audio_format: dict = {
            "sample_rate": 16000,
            "channels": 1,
            "encoding": "pcm_s16le",
        }
        self.is_active: bool = False
        self.sequence: int = 0

        # Audio buffer for accumulating chunks before STT
        self.audio_buffer: bytearray = bytearray()
        self.buffer_duration_ms: int = 0
        # Minimum audio duration (ms) before sending to STT
        self.min_buffer_ms: int = 1500

        # AI providers (lazy init)
        self._stt = None
        self._translator = None
        self._tts = None

    @property
    def stt(self):
        if self._stt is None:
            self._stt = get_stt_provider()
        return self._stt

    @property
    def translator(self):
        if self._translator is None:
            self._translator = get_translation_provider()
        return self._translator

    @property
    def tts(self):
        if self._tts is None:
            self._tts = get_tts_provider()
        return self._tts

    async def handle_control_message(self, data: dict):
        """Handle JSON control messages from client."""
        msg_type = data.get("type")

        if msg_type == "session.start":
            self.source_lang = data.get("source_lang", "vi")
            self.target_lang = data.get("target_lang", "en")
            self.context = data.get("options", {}).get("context", "")
            self.voice = data.get("options", {}).get("voice_id", "alloy")

            if "audio_format" in data:
                self.audio_format.update(data["audio_format"])

            self.is_active = True
            self.audio_buffer.clear()
            self.buffer_duration_ms = 0

            await self._send_json({
                "type": "session.started",
                "source_lang": self.source_lang,
                "target_lang": self.target_lang,
            })
            print(f"📡 Session started: {self.source_lang} → {self.target_lang}")

        elif msg_type == "session.end":
            # Process any remaining audio in buffer
            if self.audio_buffer:
                await self._process_buffered_audio()
            self.is_active = False
            await self._send_json({"type": "session.ended"})
            print("📡 Session ended")

        elif msg_type == "config.update":
            if "source_lang" in data:
                self.source_lang = data["source_lang"]
            if "target_lang" in data:
                self.target_lang = data["target_lang"]
            if "context" in data:
                self.context = data["context"]
            if "voice_id" in data:
                self.voice = data["voice_id"]
            await self._send_json({"type": "config.updated"})

    async def handle_audio_data(self, data: bytes):
        """Handle binary audio frames from client."""
        if not self.is_active:
            return

        # Accumulate audio data
        self.audio_buffer.extend(data)

        # Calculate buffer duration: bytes / (sample_rate * channels * bytes_per_sample)
        bytes_per_sample = 2  # s16le
        sample_rate = self.audio_format["sample_rate"]
        channels = self.audio_format["channels"]
        self.buffer_duration_ms = (
            len(self.audio_buffer) * 1000 // (sample_rate * channels * bytes_per_sample)
        )

        # Process when we have enough audio
        if self.buffer_duration_ms >= self.min_buffer_ms:
            await self._process_buffered_audio()

    async def _process_buffered_audio(self):
        """Process accumulated audio buffer through the full pipeline."""
        if not self.audio_buffer:
            return

        audio_data = bytes(self.audio_buffer)
        self.audio_buffer.clear()
        self.buffer_duration_ms = 0

        start_time = time.time()

        try:
            # Step 1: STT - Speech to Text
            stt_result = await self.stt.transcribe(audio_data, self.source_lang)
            source_text = stt_result.get("text", "").strip()

            if not source_text:
                return

            # Send partial transcript to client
            await self._send_json({
                "type": "transcript.partial",
                "text": source_text,
                "is_final": True,
            })

            # Step 2: Translation
            translated_text = await self.translator.translate(
                source_text,
                self.source_lang,
                self.target_lang,
                self.context,
            )

            if not translated_text:
                return

            # Send translation result to client
            await self._send_json({
                "type": "translation.result",
                "source_text": source_text,
                "translated_text": translated_text,
                "is_final": True,
            })

            # Step 3: TTS - Text to Speech
            self.sequence += 1
            async for audio_chunk in self.tts.synthesize_stream(translated_text, self.voice):
                # Prepend 4-byte sequence number to audio chunk
                header = struct.pack("<I", self.sequence)
                await self.ws.send_bytes(header + audio_chunk)

            # Send pipeline timing info
            elapsed_ms = int((time.time() - start_time) * 1000)
            await self._send_json({
                "type": "pipeline.complete",
                "latency_ms": elapsed_ms,
                "sequence": self.sequence,
            })

            print(
                f"✅ [{elapsed_ms}ms] {self.source_lang}→{self.target_lang}: "
                f'"{source_text}" → "{translated_text}"'
            )

        except Exception as e:
            traceback.print_exc()
            await self._send_json({
                "type": "error",
                "code": "pipeline_error",
                "message": str(e),
            })

    async def _send_json(self, data: dict):
        """Send a JSON message to the client."""
        await self.ws.send_text(json.dumps(data))


@router.websocket("/ws/translate")
async def websocket_translate(websocket: WebSocket):
    """
    WebSocket endpoint for real-time voice translation.

    Protocol:
    - Text frames: JSON control messages
    - Binary frames: Raw PCM audio data
    """
    await websocket.accept()
    session = TranslationSession(websocket)
    print(f"🔌 Client connected: {websocket.client}")

    try:
        while True:
            message = await websocket.receive()

            if "text" in message:
                # JSON control message
                data = json.loads(message["text"])
                await session.handle_control_message(data)

            elif "bytes" in message:
                # Binary audio data
                await session.handle_audio_data(message["bytes"])

    except WebSocketDisconnect:
        print(f"🔌 Client disconnected: {websocket.client}")
    except Exception as e:
        print(f"❌ WebSocket error: {e}")
        traceback.print_exc()
    finally:
        session.is_active = False
