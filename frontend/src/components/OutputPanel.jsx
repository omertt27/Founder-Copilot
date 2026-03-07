/**
 * Output Panel Component
 * Renders the generated content as beautifully styled Markdown.
 */
import React, { useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import {
  HiClipboardDocument,
  HiArrowDownTray,
  HiCheck,
  HiLightBulb,
  HiCpuChip,
  HiCodeBracket,
  HiPresentationChartBar,
  HiMegaphone,
  HiSparkles,
  HiClock,
  HiBeaker,
  HiBolt,
} from 'react-icons/hi2';
import './OutputPanel.css';

const FEATURE_META = {
  startup_plan: {
    label: 'Startup Plan',
    emoji: '💡',
    icon: HiLightBulb,
    color: '#6c63ff',
    gradient: 'linear-gradient(135deg, #6c63ff 0%, #5a52e0 100%)',
  },
  tech_architecture: {
    label: 'Technical Architecture',
    emoji: '🏗️',
    icon: HiCpuChip,
    color: '#00d2ff',
    gradient: 'linear-gradient(135deg, #00d2ff 0%, #3a7bd5 100%)',
  },
  github_issues: {
    label: 'GitHub Issues',
    emoji: '📋',
    icon: HiCodeBracket,
    color: '#4ade80',
    gradient: 'linear-gradient(135deg, #4ade80 0%, #22c55e 100%)',
  },
  pitch_deck: {
    label: 'Pitch Deck',
    emoji: '🎤',
    icon: HiPresentationChartBar,
    color: '#ff6b9d',
    gradient: 'linear-gradient(135deg, #ff6b9d 0%, #c44569 100%)',
  },
  marketing_strategy: {
    label: 'Marketing Strategy',
    emoji: '📣',
    icon: HiMegaphone,
    color: '#f59e0b',
    gradient: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
  },
};

const MODEL_LABELS = {
  // Nova 2 (Gen 2)
  nova2lite: { name: 'Nova 2 Lite',  badge: '⚡ Fast Reasoning' },
  nova2pro:  { name: 'Nova 2 Pro',   badge: '✨ High Quality' },
  // Nova 1 (Gen 1)
  premier:   { name: 'Nova Premier', badge: '� Most Powerful' },
  micro:     { name: 'Nova Micro',   badge: '🚀 Fastest' },
  // Demo
  demo:      { name: 'Demo Mode',    badge: '🧪 Sample Output' },
};

export default function OutputPanel({ result, feature }) {
  const [copied, setCopied] = React.useState(false);
  const contentRef = useRef(null);

  if (!result) return null;

  const meta = FEATURE_META[feature] || {
    label: 'Generated Output',
    emoji: '✨',
    icon: HiSparkles,
    color: '#6c63ff',
    gradient: 'linear-gradient(135deg, #6c63ff 0%, #ff6b9d 100%)',
  };
  const Icon = meta.icon;
  const modelInfo = MODEL_LABELS[result.model_used] || { name: `Nova ${result.model_used}`, badge: '' };

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(result.content);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      const textarea = document.createElement('textarea');
      textarea.value = result.content;
      document.body.appendChild(textarea);
      textarea.select();
      document.execCommand('copy');
      document.body.removeChild(textarea);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const handleDownload = () => {
    const blob = new Blob([result.content], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${feature || 'output'}-${Date.now()}.md`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div
      className="output-panel animate-fade-in"
      style={{ '--feature-color': meta.color, '--feature-gradient': meta.gradient }}
    >
      {/* Demo mode banner */}
      {result.demo_mode && (
        <div className="demo-mode-banner">
          <HiBeaker />
          <span>
            <strong>Demo Mode</strong> — This is a sample output. Add AWS credentials to use real Amazon Nova AI.
          </span>
        </div>
      )}

      {/* Colored top bar */}
      <div className="output-accent-bar" />

      <div className="output-header">
        <div className="output-label">
          <div className="output-icon-wrapper">
            <Icon />
          </div>
          <div className="output-label-text">
            <span className="output-feature">{meta.emoji} {meta.label}</span>
            <div className="output-meta-row">
              <span className="output-model-badge">{modelInfo.name}</span>
              {result.tokens_used > 0 && (
                <span className="output-tokens">
                  <HiSparkles /> {result.tokens_used.toLocaleString()} tokens
                </span>
              )}
              {result.generation_time > 0 && (
                <span className="output-gen-time">
                  <HiBolt /> {result.generation_time}s
                </span>
              )}
              <span className="output-timestamp">
                <HiClock /> Just now
              </span>
            </div>
          </div>
        </div>
        <div className="output-actions">
          <button
            className={`output-btn ${copied ? 'output-btn-success' : ''}`}
            onClick={handleCopy}
            title="Copy to clipboard"
          >
            {copied ? <HiCheck /> : <HiClipboardDocument />}
            {copied ? 'Copied!' : 'Copy'}
          </button>
          <button className="output-btn output-btn-download" onClick={handleDownload} title="Download as Markdown">
            <HiArrowDownTray />
            Download .md
          </button>
        </div>
      </div>

      <div className="output-content markdown-content" ref={contentRef}>
        <ReactMarkdown>{result.content}</ReactMarkdown>
      </div>

      <div className="output-footer">
        <span>Powered by <strong>Amazon Nova AI</strong> via Bedrock</span>
        <span className="output-footer-dot">•</span>
        <span>{modelInfo.badge}</span>
        {result.generation_time > 0 && (
          <>
            <span className="output-footer-dot">•</span>
            <span>Generated in {result.generation_time}s</span>
          </>
        )}
      </div>
    </div>
  );
}
