# MTrans - AI Voice Translation

> Real-time AI-powered voice translation with virtual microphone for Zoom/Teams/Meet.

## Architecture

```
mtrans/
├── apps/
│   ├── be/          # Backend API (FastAPI + Python)
│   └── fe/          # Desktop App (Tauri + React)
├── plugins/         # Platform-specific virtual audio drivers
├── docker/          # Docker configurations
└── turbo.json       # Monorepo pipeline
```

## Quick Start

### Prerequisites
- Node.js >= 20
- pnpm >= 10
- Python >= 3.11
- Rust (for Tauri desktop app)

### Install dependencies
```bash
pnpm install
```

### Run backend
```bash
pnpm dev:be
```

### Run desktop app
```bash
pnpm dev:fe
```

## How It Works

1. **Capture** audio from your physical microphone
2. **Stream** audio to backend via WebSocket
3. **Transcribe** speech using Whisper STT
4. **Translate** text using LLM (GPT-4o)
5. **Synthesize** translated speech using TTS
6. **Output** to virtual microphone
7. **Select** virtual mic in Zoom/Teams as your microphone

## License
Private - All rights reserved
