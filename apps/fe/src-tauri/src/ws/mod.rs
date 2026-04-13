//! WebSocket Client Module
//!
//! Connects to the MTrans backend API via WebSocket for real-time translation.
//!
//! Protocol:
//! - Sends JSON control messages (session.start, session.end, config.update)
//! - Sends binary audio frames (raw PCM)
//! - Receives JSON status messages (transcript, translation)
//! - Receives binary translated audio frames
//!
//! TODO: Implementation
//! 1. Connect to backend WebSocket endpoint
//! 2. Send session.start with language config
//! 3. Stream audio chunks as binary frames
//! 4. Receive and parse responses
//! 5. Route translated audio to virtual mic
//! 6. Handle reconnection on disconnect

pub mod client;
