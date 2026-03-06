/**
 * History Sidebar Component
 * Shows previously generated outputs.
 */
import React from 'react';
import {
  HiLightBulb,
  HiCpuChip,
  HiCodeBracket,
  HiPresentationChartBar,
  HiTrash,
  HiClock,
} from 'react-icons/hi2';
import './History.css';

const FEATURE_ICONS = {
  startup_plan: HiLightBulb,
  tech_architecture: HiCpuChip,
  github_issues: HiCodeBracket,
  pitch_deck: HiPresentationChartBar,
};

const FEATURE_COLORS = {
  startup_plan: '#6c63ff',
  tech_architecture: '#00d2ff',
  github_issues: '#4ade80',
  pitch_deck: '#ff6b9d',
};

const FEATURE_NAMES = {
  startup_plan: 'Startup Plan',
  tech_architecture: 'Tech Architecture',
  github_issues: 'GitHub Issues',
  pitch_deck: 'Pitch Deck',
};

export default function History({ items, onSelect, onClear }) {
  if (!items || items.length === 0) return null;

  return (
    <div className="history-panel">
      <div className="history-header">
        <div className="history-title">
          <HiClock />
          <span>History</span>
        </div>
        <button className="history-clear" onClick={onClear}>
          <HiTrash />
          Clear
        </button>
      </div>
      <div className="history-list">
        {items.map((item, index) => {
          const Icon = FEATURE_ICONS[item.feature] || HiLightBulb;
          const color = FEATURE_COLORS[item.feature] || '#6c63ff';
          return (
            <button
              key={index}
              className="history-item"
              onClick={() => onSelect(item)}
              style={{ '--item-color': color }}
            >
              <div className="history-item-icon">
                <Icon />
              </div>
              <div className="history-item-info">
                <span className="history-item-type">
                  {FEATURE_NAMES[item.feature]}
                </span>
                <span className="history-item-preview">
                  {item.input?.slice(0, 60)}...
                </span>
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
}
