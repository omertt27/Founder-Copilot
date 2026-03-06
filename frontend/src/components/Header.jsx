/**
 * Header Component
 */
import React from 'react';
import { HiSparkles } from 'react-icons/hi2';
import './Header.css';

export default function Header() {
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
        <div className="header-badge">
          <span className="badge-dot" />
          Amazon Nova Hackathon
        </div>
      </div>
    </header>
  );
}
