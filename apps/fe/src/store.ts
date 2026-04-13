/**
 * MTrans Application State Store (Zustand)
 *
 * Centralized state management for:
 * - Translation session state
 * - Audio device configuration
 * - Live transcript data
 * - Connection status
 */

import { create } from "zustand";

export interface TranscriptLine {
  id: string;
  text: string;
  isFinal: boolean;
  timestamp: number;
}

export interface TranslationResult {
  id: string;
  sourceText: string;
  translatedText: string;
  timestamp: number;
}

type ConnectionStatus = "disconnected" | "connecting" | "connected";

interface AppState {
  // Language config
  sourceLang: string;
  targetLang: string;
  setSourceLang: (lang: string) => void;
  setTargetLang: (lang: string) => void;
  swapLanguages: () => void;

  // Session state
  isTranslating: boolean;
  setIsTranslating: (v: boolean) => void;

  // Connection
  connectionStatus: ConnectionStatus;
  setConnectionStatus: (s: ConnectionStatus) => void;
  latencyMs: number;
  setLatencyMs: (ms: number) => void;

  // Transcripts
  sourceTranscripts: TranscriptLine[];
  targetTranslations: TranslationResult[];
  addSourceTranscript: (line: TranscriptLine) => void;
  addTranslation: (result: TranslationResult) => void;
  clearTranscripts: () => void;

  // Virtual mic
  virtualMicActive: boolean;
  setVirtualMicActive: (v: boolean) => void;

  // Audio
  selectedInputDevice: string;
  setSelectedInputDevice: (id: string) => void;
}

export const useAppStore = create<AppState>((set) => ({
  // Language
  sourceLang: "vi",
  targetLang: "en",
  setSourceLang: (lang) => set({ sourceLang: lang }),
  setTargetLang: (lang) => set({ targetLang: lang }),
  swapLanguages: () =>
    set((state) => ({
      sourceLang: state.targetLang,
      targetLang: state.sourceLang,
    })),

  // Session
  isTranslating: false,
  setIsTranslating: (v) => set({ isTranslating: v }),

  // Connection
  connectionStatus: "disconnected",
  setConnectionStatus: (s) => set({ connectionStatus: s }),
  latencyMs: 0,
  setLatencyMs: (ms) => set({ latencyMs: ms }),

  // Transcripts
  sourceTranscripts: [],
  targetTranslations: [],
  addSourceTranscript: (line) =>
    set((state) => ({
      sourceTranscripts: [...state.sourceTranscripts.slice(-50), line],
    })),
  addTranslation: (result) =>
    set((state) => ({
      targetTranslations: [...state.targetTranslations.slice(-50), result],
    })),
  clearTranscripts: () =>
    set({ sourceTranscripts: [], targetTranslations: [] }),

  // Virtual mic
  virtualMicActive: false,
  setVirtualMicActive: (v) => set({ virtualMicActive: v }),

  // Audio
  selectedInputDevice: "",
  setSelectedInputDevice: (id) => set({ selectedInputDevice: id }),
}));
