/**
 * Founder Copilot — Main App Component
 * Amazon Nova AI Hackathon Project
 */
import React, { useState, useCallback } from 'react';
import Header from './components/Header.jsx';
import FeatureCards from './components/FeatureCards.jsx';
import InputPanel from './components/InputPanel.jsx';
import OutputPanel from './components/OutputPanel.jsx';
import LoadingSkeleton from './components/LoadingSkeleton.jsx';
import History from './components/History.jsx';
import {
  generateStartupPlan,
  generateTechArchitecture,
  generateGitHubIssues,
  generatePitchDeck,
} from './services/api.js';
import './App.css';

export default function App() {
  const [selectedFeature, setSelectedFeature] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [history, setHistory] = useState(() => {
    try {
      const saved = localStorage.getItem('founder-copilot-history');
      return saved ? JSON.parse(saved) : [];
    } catch {
      return [];
    }
  });

  // Persist history to localStorage
  React.useEffect(() => {
    try {
      localStorage.setItem('founder-copilot-history', JSON.stringify(history));
    } catch {
      // localStorage full or unavailable — ignore
    }
  }, [history]);

  const handleGenerate = useCallback(
    async ({ input, model, productName, techStack }) => {
      setLoading(true);
      setError(null);
      setResult(null);

      try {
        let response;

        switch (selectedFeature) {
          case 'startup_plan':
            response = await generateStartupPlan(input, model);
            break;
          case 'tech_architecture':
            response = await generateTechArchitecture(input, model);
            break;
          case 'github_issues':
            response = await generateGitHubIssues(
              productName,
              input,
              techStack,
              model
            );
            break;
          case 'pitch_deck':
            response = await generatePitchDeck(input, '', model);
            break;
          default:
            throw new Error('Please select a feature first');
        }

        setResult(response);

        // Add to history
        setHistory((prev) => [
          { feature: selectedFeature, input, result: response, timestamp: Date.now() },
          ...prev.slice(0, 9), // Keep last 10
        ]);
      } catch (err) {
        setError(err.message || 'Something went wrong. Please try again.');
      } finally {
        setLoading(false);
      }
    },
    [selectedFeature]
  );

  const handleHistorySelect = (item) => {
    setSelectedFeature(item.feature);
    setResult(item.result);
    setError(null);
  };

  const handleClearHistory = () => {
    setHistory([]);
  };

  return (
    <div className="app">
      <Header />

      <main className="app-main">
        {/* Hero Section */}
        <section className="hero">
          <h2 className="hero-title">
            Turn Your Startup Idea Into
            <span className="hero-gradient"> Reality</span>
          </h2>
          <p className="hero-desc">
            Powered by <strong>Amazon Nova AI</strong> — generate startup plans,
            technical architecture, development backlogs, and pitch decks in
            seconds.
          </p>
        </section>

        {/* Feature Selector */}
        <section>
          <FeatureCards
            selected={selectedFeature}
            onSelect={setSelectedFeature}
          />
        </section>

        {/* Input Panel */}
        {selectedFeature && (
          <section>
            <InputPanel
              feature={selectedFeature}
              onGenerate={handleGenerate}
              loading={loading}
            />
          </section>
        )}

        {/* Error */}
        {error && (
          <div className="error-banner animate-fade-in">
            <span>⚠️</span>
            <p>{error}</p>
          </div>
        )}

        {/* Loading */}
        {loading && <LoadingSkeleton feature={selectedFeature} />}

        {/* Output */}
        {result && !loading && (
          <OutputPanel result={result} feature={selectedFeature} />
        )}

        {/* History */}
        <History
          items={history}
          onSelect={handleHistorySelect}
          onClear={handleClearHistory}
        />
      </main>

      {/* Footer */}
      <footer className="app-footer">
        <p>
          🚀 <strong>Founder Copilot</strong> — Built for the Amazon Nova AI
          Hackathon
        </p>
        <p className="footer-sub">
          Powered by Amazon Bedrock · Nova Premier · Nova Pro · Nova Lite · Nova Micro
        </p>
      </footer>
    </div>
  );
}
