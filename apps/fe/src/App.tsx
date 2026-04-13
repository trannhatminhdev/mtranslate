/**
 * MTrans - AI Voice Translation
 * Main Application Component
 */

import { useAppStore } from "./store";

/* ===================================
   Language data
   =================================== */
const LANGUAGES = [
  { code: "vi", name: "Tiếng Việt", flag: "🇻🇳" },
  { code: "en", name: "English", flag: "🇺🇸" },
  { code: "zh", name: "中文", flag: "🇨🇳" },
  { code: "ja", name: "日本語", flag: "🇯🇵" },
  { code: "ko", name: "한국어", flag: "🇰🇷" },
  { code: "fr", name: "Français", flag: "🇫🇷" },
  { code: "de", name: "Deutsch", flag: "🇩🇪" },
  { code: "es", name: "Español", flag: "🇪🇸" },
  { code: "th", name: "ไทย", flag: "🇹🇭" },
  { code: "id", name: "Indonesia", flag: "🇮🇩" },
];

/* ===================================
   Sub-components
   =================================== */

function TitleBar() {
  const { connectionStatus, latencyMs } = useAppStore();

  const statusClass =
    connectionStatus === "connected"
      ? "status-dot--connected"
      : connectionStatus === "connecting"
        ? "status-dot--connecting"
        : "status-dot--disconnected";

  const latencyClass =
    latencyMs < 800
      ? ""
      : latencyMs < 1500
        ? "latency-badge--slow"
        : "latency-badge--bad";

  return (
    <div className="title-bar">
      <div className="title-bar__logo">
        <div className="title-bar__logo-icon">M</div>
        <span>MTrans</span>
      </div>

      <div className="title-bar__status">
        <span className={`status-dot ${statusClass}`} />
        <span>{connectionStatus}</span>
        {connectionStatus === "connected" && latencyMs > 0 && (
          <span className={`latency-badge ${latencyClass}`}>
            {latencyMs}ms
          </span>
        )}
      </div>

      <div className="title-bar__controls">
        <button className="title-bar__btn" title="Minimize">─</button>
        <button className="title-bar__btn" title="Maximize">□</button>
        <button className="title-bar__btn title-bar__btn--close" title="Close">✕</button>
      </div>
    </div>
  );
}

function LanguageSelector() {
  const { sourceLang, targetLang, setSourceLang, setTargetLang, swapLanguages } =
    useAppStore();

  return (
    <div className="language-section">
      <div className="language-select">
        <span className="language-select__label">Source</span>
        <select
          id="source-language"
          className="language-select__dropdown"
          value={sourceLang}
          onChange={(e) => setSourceLang(e.target.value)}
        >
          {LANGUAGES.map((lang) => (
            <option key={lang.code} value={lang.code}>
              {lang.flag} {lang.name}
            </option>
          ))}
        </select>
      </div>

      <button
        id="swap-languages"
        className="language-swap-btn"
        onClick={swapLanguages}
        title="Swap languages"
      >
        ⇄
      </button>

      <div className="language-select">
        <span className="language-select__label">Target</span>
        <select
          id="target-language"
          className="language-select__dropdown"
          value={targetLang}
          onChange={(e) => setTargetLang(e.target.value)}
        >
          {LANGUAGES.map((lang) => (
            <option key={lang.code} value={lang.code}>
              {lang.flag} {lang.name}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
}

function TranslationPanel() {
  const { sourceTranscripts, targetTranslations, isTranslating } = useAppStore();

  return (
    <div className="translation-panel">
      {/* Source transcript */}
      <div className="transcript-box transcript-box--source">
        <div className="transcript-box__header">
          <span className="transcript-box__title">🎤 Original Speech</span>
          {isTranslating && <Waveform active />}
        </div>
        <div className="transcript-box__content">
          {sourceTranscripts.length === 0 ? (
            <div className="transcript-box__placeholder">
              Speech will appear here when you start translating...
            </div>
          ) : (
            sourceTranscripts.map((line) => (
              <div
                key={line.id}
                className={`transcript-line ${!line.isFinal ? "transcript-line--partial" : ""}`}
              >
                {line.text}
              </div>
            ))
          )}
        </div>
      </div>

      {/* Translation output */}
      <div className="transcript-box transcript-box--target">
        <div className="transcript-box__header">
          <span className="transcript-box__title">🌐 Translation</span>
        </div>
        <div className="transcript-box__content">
          {targetTranslations.length === 0 ? (
            <div className="transcript-box__placeholder">
              Translated text will appear here...
            </div>
          ) : (
            targetTranslations.map((result) => (
              <div key={result.id} className="transcript-line">
                {result.translatedText}
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}

function Waveform({ active = false }: { active?: boolean }) {
  return (
    <div className={`waveform ${active ? "waveform--active" : ""}`}>
      {[1, 2, 3, 4, 5].map((i) => (
        <div key={i} className="waveform__bar" style={{ height: active ? undefined : "4px" }} />
      ))}
    </div>
  );
}

function ControlBar() {
  const {
    isTranslating,
    setIsTranslating,
    virtualMicActive,
    connectionStatus,
  } = useAppStore();

  const handleToggle = () => {
    // TODO: In real implementation, this will:
    // 1. Start audio capture via Tauri command
    // 2. Open WebSocket to backend
    // 3. Begin streaming pipeline
    setIsTranslating(!isTranslating);
  };

  return (
    <div className="control-bar">
      <div className="control-info">
        <span className="control-info__label">Virtual Mic</span>
        <span className="control-info__value">
          {virtualMicActive ? "✅ Active" : "⚠️ Not detected"}
        </span>
      </div>

      <button
        id="mic-toggle"
        className={`mic-button ${isTranslating ? "mic-button--active" : ""}`}
        onClick={handleToggle}
        title={isTranslating ? "Stop translation" : "Start translation"}
      >
        {isTranslating ? "⏹" : "🎤"}
      </button>

      <div className="control-info">
        <span className="control-info__label">Status</span>
        <span className="control-info__value">
          {isTranslating
            ? "🔴 Translating..."
            : connectionStatus === "connected"
              ? "🟢 Ready"
              : "⚫ Idle"}
        </span>
      </div>
    </div>
  );
}

/* ===================================
   Main App
   =================================== */

function App() {
  return (
    <div className="app">
      <TitleBar />
      <main className="main-content">
        <LanguageSelector />
        <TranslationPanel />
      </main>
      <ControlBar />
    </div>
  );
}

export default App;
