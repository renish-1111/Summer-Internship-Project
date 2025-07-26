import React, { useEffect, useState } from 'react';
import axios from 'axios';
import SpotlightCard from '../ui/SpotlightCard';
import { useLocation, Link } from 'react-router-dom';

const getScoreColor = (score: number) => {
  if (score < 50) return '#ef4444'; // red
  if (score < 75) return '#fbbf24'; // yellow
  return '#22c55e'; // green
};

const getScoreLabel = (score: number) => {
  if (score < 50) return 'Poor';
  if (score < 75) return 'Average';
  return 'Excellent';
};

const Meter = ({ score }: { score: number }) => {
  // Animate the needle and number
  const [displayedScore, setDisplayedScore] = React.useState(0);
  React.useEffect(() => {
    let frame: number;
    let start: number | null = null;
    const duration = 1400; // ms
    const animate = (timestamp: number) => {
      if (!start) start = timestamp;
      const progress = Math.min((timestamp - start) / duration, 1);
      // Use easeOutCubic for smoother animation
      const ease = (t: number) => 1 - Math.pow(1 - t, 3);
      const easedProgress = ease(progress);
      const current = Math.round(easedProgress * score);
      setDisplayedScore(current);
      if (progress < 1) {
        frame = requestAnimationFrame(animate);
      }
    };
    setDisplayedScore(0);
    frame = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(frame);
  }, [score]);
  // Clamp score between 0 and 100
  const percent = Math.max(0, Math.min(100, displayedScore));
  const angle = (percent * 180) / 100 - 90; // -90deg (left) to +90deg (right)
  const color = getScoreColor(displayedScore);
  const label = getScoreLabel(displayedScore);
  return (
    <div className="flex flex-col items-center justify-center py-8">
      <span className="mb-4 text-xl font-bold tracking-wide" style={{ color }}>{label}</span>
      <div className="relative w-[340px] h-[180px]">
        <svg viewBox="0 0 300 180" className="w-full h-full">
          <path
            d="M30,150 A120,120 0 0,1 270,150"
            fill="none"
            stroke="#444"
            strokeWidth="22"
          />
          <path
            d="M30,150 A120,120 0 0,1 270,150"
            fill="none"
            stroke="url(#meter-gradient)"
            strokeWidth="16"
            strokeDasharray={Math.PI * 120}
            strokeDashoffset={Math.PI * 120 * (1 - percent / 100)}
            style={{ transition: 'stroke-dashoffset 1s cubic-bezier(.4,2,.6,1)' }}
          />
          <defs>
            <linearGradient id="meter-gradient" x1="0" y1="0" x2="1" y2="0">
              <stop offset="0%" stopColor="#ef4444" />
              <stop offset="50%" stopColor="#fbbf24" />
              <stop offset="100%" stopColor="#22d3ee" />
              <stop offset="100%" stopColor="#22c55e" />
            </linearGradient>
          </defs>
          {/* Needle */}
          <g style={{ transition: 'transform 1s cubic-bezier(.4,2,.6,1)', transform: `rotate(${angle}deg)`, transformOrigin: '150px 150px' }}>
            <polygon
              points="143,150 156,150 150,60"
              fill={color}
              filter="url(#needle-shadow)"
            />
            <circle cx="150" cy="150" r="13" fill={color} stroke="#fff" strokeWidth="4" />
          </g>
          <defs>
            <filter id="needle-shadow" x="0" y="0" width="200%" height="200%">
              <feDropShadow dx="0" dy="2" stdDeviation="2" floodColor={color} floodOpacity="0.5" />
            </filter>
          </defs>
        </svg>
        {/* 0 and 100 at bottom corners */}
        <div className="absolute left-0 bottom-0 text-lg text-gray-300 font-extrabold select-none" style={{transform: 'translateY(10px)'}}>
          0
        </div>
        <div className="absolute right-0 bottom-0 text-lg text-gray-300 font-extrabold select-none" style={{transform: 'translateY(10px)'}}>
          100
        </div>
        {/* 50 at top center */}
        <div className="absolute left-1/2 top-0 text-lg text-gray-300 font-extrabold select-none" style={{transform: 'translate(-50%, -10px)'}}>
          50
        </div>
        <div className="absolute left-0 right-0 top-1/2 flex flex-col items-center">
          <span
            className="text-4xl font-extrabold drop-shadow-lg"
            style={{ color, textShadow: `0 0 16px ${color}, 0 0 32px ${color}88` }}
          >
            {displayedScore}
          </span>
        </div>
      </div>
      <div className="mt-4 text-lg font-semibold text-gray-300">ATS Match Score</div>
    </div>
  );
};

const AtsScore = () => {
  const location = useLocation();
  const params = new URLSearchParams(location.search);
  const jobDescriptionFromQuery = params.get('job_description') || '';

  const [jobDescription, setJobDescription] = useState<string>(
    jobDescriptionFromQuery || localStorage.getItem('job_description') || ''
  );
  const [score, setScore] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const resumeText = localStorage.getItem('resume_text');
  const lastMessage = localStorage.getItem('message');
  const missingResume = !resumeText || !lastMessage;

  if (missingResume) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-gray-900 via-gray-800 to-black text-white pt-24 px-2">
        <SpotlightCard className="w-full max-w-lg bg-gray-900/80 rounded-2xl shadow-2xl p-8 border border-gray-800 flex flex-col items-center">
          <h1 className="text-3xl font-bold text-purple-400 mb-6 text-center">Resume Analysis Required</h1>
          <p className="text-lg text-gray-200 mb-6 text-center max-w-2xl">
            Please analyze your resume first on the <span className="text-purple-300 font-semibold">Analysis</span> page before using the ATS Score feature.
          </p>
          <Link to="/analys">
            <button className="bg-purple-600 hover:bg-purple-700 text-white font-bold py-2 px-8 rounded shadow-lg transition text-lg">
              Go to Analysis
            </button>
          </Link>
        </SpotlightCard>
      </div>
    );
  }

  useEffect(() => {
    if (jobDescriptionFromQuery) {
      setJobDescription(jobDescriptionFromQuery);
    }
  }, [jobDescriptionFromQuery]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setScore(null);
    
    const resumeText = localStorage.getItem('resume_text');
    if (!resumeText) {
      setError('Please analyze your resume first on the Analysis page.');
      setLoading(false);
      return;
    }
    if (!jobDescription) {
      setError('Please enter a job description.');
      setLoading(false);
      return;
    }
    localStorage.setItem('job_description', jobDescription);
    try {
      const formData = new FormData();
      formData.append('resume_text', resumeText);
      const res = await axios.post(
        `/api/ats?job_description=${encodeURIComponent(jobDescription)}`,
        formData
      );
      if (res.data && typeof res.data.ats_score === 'number') {
        setScore(res.data.ats_score);
      } else {
        setError('Failed to get ATS score.');
      }
    } catch (err: any) {
      setError(err.response?.data?.message || err.message || 'An error occurred.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-gray-900 via-gray-800 to-black text-white pt-24 px-2">
      <SpotlightCard className={`w-full ${score !== null ? 'max-w-6xl' : 'max-w-lg'} bg-gray-900/80 rounded-2xl shadow-2xl p-8 border border-gray-800`}>
        {score === null ? (
          // Centered form before score
          <div className="flex flex-col items-center">
            <h1 className="text-3xl font-bold text-purple-400 mb-6 text-center">ATS Score</h1>
            <form onSubmit={handleSubmit} className="w-full flex flex-col gap-6 mb-8">
              <label className="font-semibold text-lg text-gray-200">
                Job Description
                <textarea
                  className="mt-2 w-full min-h-[100px] rounded-lg bg-gray-800 border border-purple-700 text-white p-3 focus:outline-none focus:ring-2 focus:ring-purple-500 transition"
                  value={jobDescription}
                  onChange={e => setJobDescription(e.target.value)}
                  placeholder="Paste the job description here..."
                  required
                />
              </label>
              <button
                type="submit"
                className="bg-purple-600 hover:bg-purple-700 text-white font-bold py-3 px-8 rounded shadow-lg transition text-lg disabled:opacity-60"
                disabled={loading}
              >
                {loading ? 'Calculating...' : 'Get ATS Score'}
              </button>
            </form>
            {error && <div className="text-center text-lg text-red-400 font-semibold py-4">{error}</div>}
            {loading && <div className="text-center text-lg text-purple-300 font-semibold py-12 animate-pulse">Calculating ATS Score...</div>}
          </div>
        ) : (
          // Side-by-side meter and form after score
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-stretch">
            {/* Meter on the left */}
            <div className="flex-1 min-w-0 flex items-start justify-center mb-8 lg:mb-0">
              <Meter score={score} />
            </div>
            {/* Form on the right */}
            <div className="flex-1 min-w-0 flex flex-col justify-start">
              <h1 className="text-3xl font-bold text-purple-400 mb-6 text-center lg:text-left">ATS Score</h1>
              <form onSubmit={handleSubmit} className="w-full flex flex-col gap-6 mb-8">
                <label className="font-semibold text-lg text-gray-200">
                  Job Description
                  <textarea
                    className="mt-2 w-full min-h-[100px] rounded-lg bg-gray-800 border border-purple-700 text-white p-3 focus:outline-none focus:ring-2 focus:ring-purple-500 transition"
                    value={jobDescription}
                    onChange={e => setJobDescription(e.target.value)}
                    placeholder="Paste the job description here..."
                    required
                  />
                </label>
                <button
                  type="submit"
                  className="bg-purple-600 hover:bg-purple-700 text-white font-bold py-3 px-8 rounded shadow-lg transition text-lg disabled:opacity-60"
                  disabled={loading}
                >
                  {loading ? 'Calculating...' : 'Get ATS Score'}
                </button>
              </form>
              {error && <div className="text-center text-lg text-red-400 font-semibold py-4">{error}</div>}
              {loading && <div className="text-center text-lg text-purple-300 font-semibold py-12 animate-pulse">Calculating ATS Score...</div>}
            </div>
          </div>
        )}
      </SpotlightCard>
    </div>
  );
};

export default AtsScore;