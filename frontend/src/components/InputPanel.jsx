/**
 * Input Panel Component
 * Handles user input for the selected feature.
 */
import React, { useState } from 'react';
import { HiPaperAirplane, HiArrowPath } from 'react-icons/hi2';
import './InputPanel.css';

const PLACEHOLDERS = {
  startup_plan:
    'Describe your startup idea... e.g. "AI tool that summarizes long meetings and creates action items automatically"',
  tech_architecture:
    'Describe what you want to build... e.g. "A SaaS platform for freelancers to track time, send invoices, and manage clients"',
  github_issues:
    'Describe the product to create issues for... e.g. "Developer tool that uses AI to automatically write documentation from code"',
  pitch_deck:
    'Describe your startup for the pitch deck... e.g. "AI-powered meeting assistant that records, summarizes, and creates action items"',
};

const TITLES = {
  startup_plan: '💡 Describe Your Startup Idea',
  tech_architecture: '🏗️ Describe Your Product',
  github_issues: '📋 Describe Your Project',
  pitch_deck: '🎤 Describe Your Startup',
};

const MODEL_OPTIONS = [
  { value: 'pro', label: 'Nova Pro', desc: 'Best quality' },
  { value: 'lite', label: 'Nova Lite', desc: 'Balanced' },
  { value: 'micro', label: 'Nova Micro', desc: 'Fastest' },
];

export default function InputPanel({
  feature,
  onGenerate,
  loading,
  extraFields,
}) {
  const [input, setInput] = useState('');
  const [model, setModel] = useState('pro');
  const [productName, setProductName] = useState('');
  const [techStack, setTechStack] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    onGenerate({
      input: input.trim(),
      model,
      productName: productName.trim() || 'My Startup',
      techStack: techStack.trim() || 'To be determined',
    });
  };

  return (
    <form className="input-panel" onSubmit={handleSubmit}>
      <h2 className="input-title">{TITLES[feature] || '💡 Describe Your Idea'}</h2>

      <textarea
        className="input-textarea"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder={PLACEHOLDERS[feature]}
        rows={4}
        disabled={loading}
      />

      {/* Extra fields for GitHub Issues */}
      {feature === 'github_issues' && (
        <div className="input-extras">
          <div className="input-field">
            <label>Product Name</label>
            <input
              type="text"
              value={productName}
              onChange={(e) => setProductName(e.target.value)}
              placeholder="e.g. MeetingAI"
              disabled={loading}
            />
          </div>
          <div className="input-field">
            <label>Tech Stack (optional)</label>
            <input
              type="text"
              value={techStack}
              onChange={(e) => setTechStack(e.target.value)}
              placeholder="e.g. React, FastAPI, PostgreSQL"
              disabled={loading}
            />
          </div>
        </div>
      )}

      <div className="input-actions">
        {/* Model Selector */}
        <div className="model-selector">
          {MODEL_OPTIONS.map((opt) => (
            <button
              type="button"
              key={opt.value}
              className={`model-btn ${model === opt.value ? 'active' : ''}`}
              onClick={() => setModel(opt.value)}
              disabled={loading}
            >
              <span className="model-label">{opt.label}</span>
              <span className="model-desc">{opt.desc}</span>
            </button>
          ))}
        </div>

        {/* Generate Button */}
        <button
          type="submit"
          className="generate-btn"
          disabled={!input.trim() || loading}
        >
          {loading ? (
            <>
              <HiArrowPath className="spin" />
              Generating...
            </>
          ) : (
            <>
              <HiPaperAirplane />
              Generate
            </>
          )}
        </button>
      </div>
    </form>
  );
}
