/**
 * Loading Skeleton Component
 * Shows an animated placeholder while generating content.
 */
import React from 'react';
import './LoadingSkeleton.css';

const LOADING_MESSAGES = [
  '🧠 Amazon Nova is thinking...',
  '🚀 Analyzing your idea...',
  '📊 Generating insights...',
  '✨ Crafting your plan...',
  '🔮 Almost there...',
];

export default function LoadingSkeleton({ feature }) {
  const [messageIndex, setMessageIndex] = React.useState(0);

  React.useEffect(() => {
    const interval = setInterval(() => {
      setMessageIndex((i) => (i + 1) % LOADING_MESSAGES.length);
    }, 2500);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="loading-skeleton">
      <div className="loading-header">
        <div className="loading-spinner" />
        <span className="loading-message">{LOADING_MESSAGES[messageIndex]}</span>
      </div>
      <div className="skeleton-lines">
        <div className="skeleton-line w-80" />
        <div className="skeleton-line w-60" />
        <div className="skeleton-line w-90" />
        <div className="skeleton-line w-45" />
        <div className="skeleton-line w-70" />
        <div className="skeleton-line w-55" />
        <div className="skeleton-line w-85" />
        <div className="skeleton-line w-40" />
      </div>
    </div>
  );
}
