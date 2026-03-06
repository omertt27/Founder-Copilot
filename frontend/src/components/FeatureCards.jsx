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
];

export default function FeatureCards({ selected, onSelect }) {
  return (
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
  );
}
