/**
 * Feature Card Selector Component
 * Displays the 4 feature options as clickable cards.
 */
import React from 'react';
import { motion } from 'framer-motion';
import {
  HiLightBulb,
  HiCpuChip,
  HiCodeBracket,
  HiPresentationChartBar,
  HiMegaphone,
  HiRocketLaunch,
} from 'react-icons/hi2';
import './FeatureCards.css';

const FEATURES = [
  {
    id: 'startup_plan',
    title: 'Startup Plan',
    description: 'Turn your idea into a comprehensive startup strategy with roadmap and metrics',
    icon: HiLightBulb,
    color: '#6c63ff',
    gradient: 'linear-gradient(135deg, #6c63ff 0%, #5a52e0 100%)',
  },
  {
    id: 'tech_architecture',
    title: 'Tech Architecture',
    description: 'Get a complete tech stack, database schema, API design, and system architecture',
    icon: HiCpuChip,
    color: '#00d2ff',
    gradient: 'linear-gradient(135deg, #00d2ff 0%, #3a7bd5 100%)',
  },
  {
    id: 'github_issues',
    title: 'GitHub Issues',
    description: 'Generate a prioritized development backlog with detailed issues and estimates',
    icon: HiCodeBracket,
    color: '#4ade80',
    gradient: 'linear-gradient(135deg, #4ade80 0%, #22c55e 100%)',
  },
  {
    id: 'pitch_deck',
    title: 'Pitch Deck',
    description: 'Create an investor-ready pitch deck outline with 12 professional slides',
    icon: HiPresentationChartBar,
    color: '#ff6b9d',
    gradient: 'linear-gradient(135deg, #ff6b9d 0%, #c44569 100%)',
  },
  {
    id: 'marketing_strategy',
    title: 'Marketing Strategy',
    description: 'Full go-to-market plan with personas, content calendar, growth tactics, and KPIs',
    icon: HiMegaphone,
    color: '#f59e0b',
    gradient: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
  },
];

const FOUNDER_PACKAGE = {
  id: 'founder_package',
  title: '🚀 Full Founder Package',
  description: 'Run all 5 AI agents in sequence — get your complete startup kit in one click',
  icon: HiRocketLaunch,
  color: '#a855f7',
  gradient: 'linear-gradient(135deg, #a855f7 0%, #7c3aed 100%)',
  isSpecial: true,
};

export default function FeatureCards({ selected, onSelect }) {
  return (
    <div className="feature-cards-wrapper">
      {/* Individual feature cards */}
      <div className="feature-cards">
        {FEATURES.map((feature, index) => {
          const Icon = feature.icon;
          const isSelected = selected === feature.id;
          return (
            <motion.button
              key={feature.id}
              className={`feature-card ${isSelected ? 'selected' : ''}`}
              onClick={() => onSelect(feature.id)}
              style={{
                '--card-color': feature.color,
                '--card-gradient': feature.gradient,
              }}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, delay: index * 0.08 }}
              whileHover={{ scale: 1.03 }}
              whileTap={{ scale: 0.97 }}
            >
              <div className="feature-card-icon">
                <Icon />
              </div>
              <h3 className="feature-card-title">{feature.title}</h3>
              <p className="feature-card-desc">{feature.description}</p>
              {isSelected && <div className="feature-card-check">✓</div>}
            </motion.button>
          );
        })}
      </div>

      {/* Full Founder Package — special CTA */}
      <motion.button
        className={`founder-package-card ${selected === FOUNDER_PACKAGE.id ? 'selected' : ''}`}
        onClick={() => onSelect(FOUNDER_PACKAGE.id)}
        style={{
          '--card-color': FOUNDER_PACKAGE.color,
          '--card-gradient': FOUNDER_PACKAGE.gradient,
        }}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3, delay: 0.45 }}
        whileHover={{ scale: 1.01 }}
        whileTap={{ scale: 0.98 }}
      >
        <div className="fp-card-left">
          <div className="fp-card-agents">
            <span>💡 CEO</span>
            <span className="fp-arrow">→</span>
            <span>🏗️ CTO</span>
            <span className="fp-arrow">→</span>
            <span>👩‍💻 Eng Lead</span>
            <span className="fp-arrow">→</span>
            <span>🎤 IR</span>
            <span className="fp-arrow">→</span>
            <span>📣 CMO</span>
          </div>
          <h3 className="fp-card-title">{FOUNDER_PACKAGE.title}</h3>
          <p className="fp-card-desc">{FOUNDER_PACKAGE.description}</p>
        </div>
        <div className="fp-card-right">
          <HiRocketLaunch className="fp-card-icon" />
          {selected === FOUNDER_PACKAGE.id && <div className="feature-card-check">✓</div>}
        </div>
      </motion.button>
    </div>
  );
}
