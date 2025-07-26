import React, { useState, useEffect } from 'react';
import axios from 'axios';
import SpotlightCard from '../ui/SpotlightCard';
import {Link } from 'react-router-dom';

export default function CoverLatter() {
  const [jobDescription, setJobDescription] = useState('');
  const [companyName, setCompanyName] = useState('');
  const [hiringManagerName, setHiringManagerName] = useState('');
  const [desiredTone, setDesiredTone] = useState('');
  const [resumeText, setResumeText] = useState<string | null>(null);
  const [coverLetter, setCoverLetter] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    const storedResume = localStorage.getItem('resume_text');
    setResumeText(storedResume);
  }, []);

  const missingResume = !localStorage.getItem('resume_text') || !localStorage.getItem('message');
  if (missingResume) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-gray-900 via-gray-800 to-black text-white pt-24 px-2">
        <SpotlightCard className="w-full max-w-lg bg-gray-900/80 rounded-2xl shadow-2xl p-8 border border-gray-800 flex flex-col items-center">
          <h1 className="text-3xl font-bold text-purple-400 mb-6 text-center">Resume Analysis Required</h1>
          <p className="text-lg text-gray-200 mb-6 text-center max-w-2xl">
            Please analyze your resume first on the <span className="text-purple-300 font-semibold">Analysis</span> page before generating a cover letter.
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

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setCoverLetter(null);
    setCopied(false);
    try {
      const params = new URLSearchParams({
        job_description: jobDescription,
        company_name: companyName,
      });
      if (hiringManagerName) params.append('hiring_manager_name', hiringManagerName);
      if (desiredTone) params.append('desired_tone', desiredTone);
      const formData = new FormData();
      formData.append('resume_text', resumeText || '');
      const response = await axios.post(
        `/api/cover_letter?${params.toString()}`,
        formData
      );
      if (response.data && response.data.success) {
        var generatedCoverLetter = response.data.cover_letter;
         //replace * with ""
         //replace "| " with \n

        generatedCoverLetter = generatedCoverLetter.replace(/\*/g, '');
        generatedCoverLetter = generatedCoverLetter.replace(/\| /g, '\n');
       


        setCoverLetter(generatedCoverLetter);
        
      } else {
        setError('Failed to generate cover letter.');
      }
    } catch (err: any) {
      setError(err.response?.data?.message || err.message || 'An error occurred.');
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = () => {
    if (coverLetter) {
      navigator.clipboard.writeText(coverLetter);
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-gray-900 via-gray-800 to-black text-white pt-24 px-2">
      <SpotlightCard className="w-full max-w-3xl bg-gray-900/80 rounded-2xl shadow-2xl p-8 border border-gray-800">
        <h1 className="text-3xl font-bold text-purple-400 mb-6 text-center">Generate Cover Letter</h1>
        {!resumeText ? (
          <div className="text-center text-lg text-red-400 font-semibold py-12">
            Please analyze your resume first on the <a href="/analys" className="underline text-purple-400">Analysis</a> page before generating a cover letter.
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="flex flex-col gap-6">
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
            <label className="font-semibold text-lg text-gray-200">
              Company Name
              <input
                className="mt-2 w-full rounded-lg bg-gray-800 border border-purple-700 text-white p-3 focus:outline-none focus:ring-2 focus:ring-purple-500 transition"
                value={companyName}
                onChange={e => setCompanyName(e.target.value)}
                placeholder="Enter the company name..."
                required
              />
            </label>
            <label className="font-semibold text-lg text-gray-200">
              Hiring Manager Name <span className="text-xs text-gray-400">(optional)</span>
              <input
                className="mt-2 w-full rounded-lg bg-gray-800 border border-purple-700 text-white p-3 focus:outline-none focus:ring-2 focus:ring-purple-500 transition"
                value={hiringManagerName}
                onChange={e => setHiringManagerName(e.target.value)}
                placeholder="Enter the hiring manager's name (optional)..."
              />
            </label>
            <label className="font-semibold text-lg text-gray-200">
              Desired Tone <span className="text-xs text-gray-400">(optional)</span>
              <input
                className="mt-2 w-full rounded-lg bg-gray-800 border border-purple-700 text-white p-3 focus:outline-none focus:ring-2 focus:ring-purple-500 transition"
                value={desiredTone}
                onChange={e => setDesiredTone(e.target.value)}
                placeholder="e.g. Professional, Friendly, Enthusiastic (optional)"
              />
            </label>
            <button
              type="submit"
              className="bg-purple-600 hover:bg-purple-700 text-white font-bold py-3 px-8 rounded shadow-lg transition text-lg disabled:opacity-60"
              disabled={loading}
            >
              {loading ? 'Generating...' : 'Generate Cover Letter'}
            </button>
            {error && <div className="text-red-400 text-center font-semibold mt-2">{error}</div>}
          </form>
        )}
        {coverLetter && (
          <div className="mt-10">
            <h2 className="text-2xl font-bold text-purple-300 mb-4 text-center">Your Cover Letter</h2>
            <div className="relative">
              <pre className="whitespace-pre-wrap break-words bg-gray-900/70 border border-purple-700 rounded-xl p-6 text-lg text-white font-mono shadow-inner max-h-[400px] overflow-auto">
                {coverLetter}
              </pre>
              <button
                onClick={handleCopy}
                className="absolute top-3 right-3 bg-purple-500 hover:bg-purple-700 text-white text-xs font-semibold px-4 py-2 rounded shadow transition"
              >
                {copied ? 'Copied!' : 'Copy'}
              </button>
            </div>
          </div>
        )}
      </SpotlightCard>
    </div>
  );
} 