/**
 * Output Panel Component
 * Renders the generated content as styled Markdown.
 */
import React, { useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import {
  HiClipboardDocument,
  HiArrowDownTray,
  HiCheck,
} from 'react-icons/hi2';
import './OutputPanel.css';

const FEATURE_LABELS = {
  startup_plan: '💡 Startup Plan',
  tech_architecture: '🏗️ Technical Architecture',
  github_issues: '📋 GitHub Issues',
  pitch_deck: '🎤 Pitch Deck',
};

export default function OutputPanel({ result, feature }) {
  const [copied, setCopied] = React.useState(false);
  const contentRef = useRef(null);

  if (!result) return null;

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(result.content);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // Fallback
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
    <div className="output-panel animate-fade-in">
      <div className="output-header">
        <div className="output-label">
          <span className="output-feature">
            {FEATURE_LABELS[feature] || 'Generated Output'}
          </span>
          <span className="output-model">
            Model: Nova {result.model_used || 'Premier'}
            {result.tokens_used ? ` · ${result.tokens_used} tokens` : ''}
          </span>
        </div>
        <div className="output-actions">
          <button className="output-btn" onClick={handleCopy} title="Copy to clipboard">
            {copied ? <HiCheck /> : <HiClipboardDocument />}
            {copied ? 'Copied!' : 'Copy'}
          </button>
          <button className="output-btn" onClick={handleDownload} title="Download as Markdown">
            <HiArrowDownTray />
            Download
          </button>
        </div>
      </div>

      <div className="output-content markdown-content" ref={contentRef}>
        <ReactMarkdown>{result.content}</ReactMarkdown>
      </div>
    </div>
  );
}
