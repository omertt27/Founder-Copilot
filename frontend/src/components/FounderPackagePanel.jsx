/**
 * Founder Package Panel
 * Displays the full multi-agent pipeline results in a tabbed view.
 */
import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { motion, AnimatePresence } from 'framer-motion';
import {
  HiLightBulb,
  HiCpuChip,
  HiCodeBracket,
  HiPresentationChartBar,
  HiMegaphone,
  HiClipboardDocument,
  HiCheck,
  HiClock,
  HiBeaker,
  HiSparkles,
} from 'react-icons/hi2';
import './FounderPackagePanel.css';

const STEP_META = {
  startup_plan: { icon: HiLightBulb, color: '#6c63ff', label: 'Startup Plan' },
  tech_architecture: { icon: HiCpuChip, color: '#00d2ff', label: 'Tech Architecture' },
  github_issues: { icon: HiCodeBracket, color: '#4ade80', label: 'GitHub Issues' },
  pitch_deck: { icon: HiPresentationChartBar, color: '#ff6b9d', label: 'Pitch Deck' },
  marketing_strategy: { icon: HiMegaphone, color: '#f59e0b', label: 'Marketing Strategy' },
};

export default function FounderPackagePanel({ result }) {
  const [activeTab, setActiveTab] = useState(0);
  const [copiedTab, setCopiedTab] = useState(null);

  if (!result || !result.steps) return null;

  const { steps, total_tokens, total_time, model_used, demo_mode, idea } = result;

  const handleCopy = async (content, idx) => {
    try {
      await navigator.clipboard.writeText(content);
    } catch {
      const ta = document.createElement('textarea');
      ta.value = content;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
    }
    setCopiedTab(idx);
    setTimeout(() => setCopiedTab(null), 2000);
  };

  const handleCopyAll = async () => {
    const all = steps.map((s) => `# ${s.agent}\n\n${s.content}`).join('\n\n---\n\n');
    try {
      await navigator.clipboard.writeText(all);
    } catch {
      const ta = document.createElement('textarea');
      ta.value = all;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
    }
    setCopiedTab('all');
    setTimeout(() => setCopiedTab(null), 2000);
  };

  const activeStep = steps[activeTab];
  const meta = STEP_META[activeStep?.feature] || { icon: HiSparkles, color: '#6c63ff', label: 'Output' };
  const Icon = meta.icon;

  return (
    <motion.div
      className="fp-panel"
      initial={{ opacity: 0, y: 24 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
    >
      {/* Header */}
      <div className="fp-panel-header">
        <div className="fp-panel-title-row">
          <div className="fp-panel-rocket">🚀</div>
          <div>
            <h2 className="fp-panel-title">Full Founder Package</h2>
            <p className="fp-panel-subtitle">"{idea}"</p>
          </div>
        </div>
        <div className="fp-panel-meta">
          {demo_mode && (
            <span className="fp-badge demo">🧪 Demo Mode</span>
          )}
          <span className="fp-badge">
            <HiClock /> {total_time}s total
          </span>
          {total_tokens && (
            <span className="fp-badge">
              <HiSparkles /> {total_tokens.toLocaleString()} tokens
            </span>
          )}
          <button className="fp-copy-all-btn" onClick={handleCopyAll}>
            {copiedTab === 'all' ? <HiCheck /> : <HiClipboardDocument />}
            {copiedTab === 'all' ? 'Copied!' : 'Copy All'}
          </button>
        </div>
      </div>

      {/* Agent pipeline progress */}
      <div className="fp-pipeline">
        {steps.map((step, idx) => {
          const sm = STEP_META[step.feature] || { icon: HiSparkles, color: '#6c63ff' };
          const SIcon = sm.icon;
          return (
            <React.Fragment key={idx}>
              <button
                className={`fp-pipeline-step ${activeTab === idx ? 'active' : ''}`}
                style={{ '--step-color': sm.color }}
                onClick={() => setActiveTab(idx)}
              >
                <div className="fp-step-icon">
                  <SIcon />
                </div>
                <div className="fp-step-info">
                  <span className="fp-step-agent">{step.agent}</span>
                  <span className="fp-step-time">{step.generation_time}s</span>
                </div>
              </button>
              {idx < steps.length - 1 && (
                <div className="fp-pipeline-arrow">→</div>
              )}
            </React.Fragment>
          );
        })}
      </div>

      {/* Active tab content */}
      <AnimatePresence mode="wait">
        <motion.div
          key={activeTab}
          className="fp-tab-content"
          style={{ '--step-color': meta.color }}
          initial={{ opacity: 0, x: 10 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -10 }}
          transition={{ duration: 0.2 }}
        >
          <div className="fp-tab-header">
            <div className="fp-tab-icon" style={{ color: meta.color }}>
              <Icon />
            </div>
            <div>
              <h3 className="fp-tab-title">{activeStep.agent}</h3>
              <span className="fp-tab-tokens">
                {activeStep.tokens_used?.toLocaleString()} tokens · {activeStep.generation_time}s
              </span>
            </div>
            <button
              className="fp-copy-btn"
              onClick={() => handleCopy(activeStep.content, activeTab)}
            >
              {copiedTab === activeTab ? <HiCheck /> : <HiClipboardDocument />}
              {copiedTab === activeTab ? 'Copied!' : 'Copy'}
            </button>
          </div>

          <div className="fp-markdown-body">
            <ReactMarkdown>{activeStep.content}</ReactMarkdown>
          </div>
        </motion.div>
      </AnimatePresence>

      {/* Navigation */}
      <div className="fp-nav">
        <button
          className="fp-nav-btn"
          disabled={activeTab === 0}
          onClick={() => setActiveTab((t) => t - 1)}
        >
          ← Previous Agent
        </button>
        <span className="fp-nav-count">{activeTab + 1} / {steps.length}</span>
        <button
          className="fp-nav-btn"
          disabled={activeTab === steps.length - 1}
          onClick={() => setActiveTab((t) => t + 1)}
        >
          Next Agent →
        </button>
      </div>
    </motion.div>
  );
}
