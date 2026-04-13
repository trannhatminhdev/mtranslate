//! Audio module - Capture, VAD, and Virtual Mic output
//!
//! This module handles the audio pipeline:
//! - Capturing audio from the physical microphone (CPAL + WASAPI)
//! - Voice Activity Detection (Silero VAD via ONNX Runtime)
//! - Writing translated audio to virtual microphone

pub mod capture;
pub mod vad;
pub mod virtual_mic;

/// Audio configuration
pub struct AudioConfig {
    pub sample_rate: u32,
    pub channels: u16,
    pub chunk_duration_ms: u32,
}

impl Default for AudioConfig {
    fn default() -> Self {
        Self {
            sample_rate: 16000,
            channels: 1,
            chunk_duration_ms: 30,
        }
    }
}
