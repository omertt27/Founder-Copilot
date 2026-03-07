/**
 * Header Component
 */
import React, { useState, useEffect } from 'react';
import { HiSparkles, HiBeaker } from 'react-icons/hi2';
import { healthCheck } from '../services/api.js';
import './Header.css';

export default function Header() {
  const [demoMode, setDemoMode] = useState(false);

  useEffect(() => {
    healthCheck()
      .then((data) => setDemoMode(!!data.demo_mode))
      .catch(() => {});
  }, []);

  return (
    <header className="header">
      <div className="header-inner">
        <div className="header-brand">
          <div className="header-logo">
            <HiSparkles />
          </div>
          <div>
            <h1 className="header-title">Founder Copilot</h1>
            <p className="header-subtitle">Powered by Amazon Nova AI</p>
          </div>
        </div>
        <div className="header-badges">
          {demoMode && (
            <div className="header-demo-badge">
              <HiBeaker />
              Demo Mode
            </div>
          )}
          <div className="header-badge">
            <span className="badge-dot" />
            Amazon Nova Hackathon
          </div>
        </div>
      </div>
    </header>
  );
}
