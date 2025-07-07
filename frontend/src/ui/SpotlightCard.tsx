import React, { useRef } from 'react';

interface SpotlightCardProps {
  children: React.ReactNode;
  className?: string;
}

const SpotlightCard: React.FC<SpotlightCardProps> = ({ children, className }) => {
  const cardRef = useRef<HTMLDivElement>(null);

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement, MouseEvent>) => {
    const card = cardRef.current;
    if (!card) return;
    const rect = card.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    card.style.setProperty('--spotlight-x', `${x}px`);
    card.style.setProperty('--spotlight-y', `${y}px`);
  };

  const handleMouseLeave = () => {
    const card = cardRef.current;
    if (card) {
      card.style.setProperty('--spotlight-x', `-999px`);
      card.style.setProperty('--spotlight-y', `-999px`);
    }
  };

  return (
    <div
      ref={cardRef}
      className={`relative overflow-hidden group ${className || ''}`}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      style={{
        '--spotlight-x': '-999px',
        '--spotlight-y': '-999px',
      } as React.CSSProperties}
    >
      <div
        className="pointer-events-none absolute inset-0 z-10"
        style={{
          background: 'radial-gradient(600px circle at var(--spotlight-x) var(--spotlight-y), rgba(124,58,237,0.18), transparent 60%)',
          transition: 'background 0.2s',
        }}
      />
      <div className="relative z-20">{children}</div>
    </div>
  );
};

export default SpotlightCard;