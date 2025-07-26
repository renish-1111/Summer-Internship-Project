import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import SpotlightCard from '../ui/SpotlightCard';

const Analys = () => {
  const [pdfFile, setPdfFile] = useState<File | null>(null);
  const [jobDescription, setJobDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  // const [apiData, setApiData] = useState<any>(null);
  const [lastMessage, setLastMessage] = useState<string | null>(null);
  const [lastFileName, setLastFileName] = useState<string | null>(null);
  // const [lastResumeText, setLastResumeText] = useState<string | null>(null);

  // On mount, load last result and file name from localStorage
  useEffect(() => {
    const savedMessage = localStorage.getItem('message');
    const savedFileName = localStorage.getItem('last_pdf_filename');
    const savedResumeText = localStorage.getItem('resume_text');
    if (savedMessage && savedResumeText && savedFileName) {
      setLastMessage(savedMessage);
      setLastFileName(savedFileName);
      // setLastResumeText(savedResumeText);
    }
  }, []);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPdfFile(e.target.files?.[0] || null);
    setError(null);
  };

  const handleDescriptionChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setJobDescription(e.target.value);
  };

  const handleDragOver = (e: React.DragEvent<HTMLLabelElement>) => {
    e.preventDefault();
    setDragActive(true);
  };

  const handleDragLeave = (e: React.DragEvent<HTMLLabelElement>) => {
    e.preventDefault();
    setDragActive(false);
  };

  const handleDrop = (e: React.DragEvent<HTMLLabelElement>) => {
    e.preventDefault();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setPdfFile(e.dataTransfer.files[0]);
      setError(null);
    }
  };

  const handleBrowseClick = () => {
    fileInputRef.current?.click();
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    // setApiData(null);
    if (!pdfFile) {
      setError("Please upload a PDF file.");
      setLoading(false);
      return;
    }
    try {
      const formData = new FormData();
      formData.append("pdf_file", pdfFile);
      formData.append("job_description", jobDescription);
      const response = await axios.post("http://localhost:5000/api/pdf-analysis", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      // setApiData(response.data);
      // Store message and file name in localStorage
      localStorage.setItem('message', response.data.message || '');
      localStorage.setItem('last_pdf_filename', pdfFile.name);
      localStorage.setItem('resume_text', response.data.resume_text || '');
      setLastMessage(response.data.message || '');
      setLastFileName(pdfFile.name);
      // setLastResumeText(response.data.resume_text || '');
    } catch (err: any) {
      setError(err.response?.data?.message || err.message || "An error occurred.");
    } finally {
      setLoading(false);
    }
  };

  // Custom markdown parser (basic)
  function simpleMarkdownToHtml(md: string): string {
    let html = md;
    // Headings
    html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
    html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
    html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');
    // Bold
    html = html.replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>');
    // Italic
    html = html.replace(/\*(.*?)\*/gim, '<em>$1</em>');
    // Unordered lists
    html = html.replace(/^\s*\* (.*$)/gim, '<ul><li>$1</li></ul>');
    // Ordered lists
    html = html.replace(/^\s*\d+\. (.*$)/gim, '<ol><li>$1</li></ol>');
    // Paragraphs
    html = html.replace(/^(?!<h\d|<ul|<ol|<li|<strong|<em)([^\n]+)\n/gim, '<p>$1</p>');
    // Line breaks
    html = html.replace(/\n/g, '<br />');
    // Merge adjacent <ul> and <ol>
    html = html.replace(/(<\/ul>)(<ul>)/g, '');
    html = html.replace(/(<\/ol>)(<ol>)/g, '');
    return html;
  }

  // Download last analysis message as .txt file

  // Add this function below handleDownloadResult:
  const handleDownloadHtmlResult = () => {
    if (!lastMessage) return;
    const htmlContent = `
      <!DOCTYPE html>
      <html lang="en">
      <head>
        <meta charset="UTF-8" />
        <title>Resume Analysis Result</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <style>
          body {
            background: linear-gradient(135deg, #232526 0%, #414345 100%);
            color: #fff;
            font-family: 'Segoe UI', Arial, sans-serif;
            margin: 0;
            padding: 0;
          }
          .container {
            max-width: 700px;
            margin: 40px auto;
            background: rgba(30, 30, 40, 0.95);
            border-radius: 18px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            padding: 32px 28px;
            border: 1.5px solid #7c3aed;
          }
          h1, h2, h3 {
            color: #a78bfa;
          }
          .file-info {
            color: #fbbf24;
            margin-bottom: 18px;
          }
          .result-content {
            background: rgba(55, 48, 163, 0.12);
            border-radius: 12px;
            padding: 18px;
            margin-top: 18px;
            color: #fff;
          }
          .badge {
            display: inline-block;
            background: #7c3aed;
            color: #fff;
            border-radius: 8px;
            padding: 2px 10px;
            font-size: 0.95em;
            margin-right: 8px;
          }
        </style>
      </head>
      <body>
        <div class="container">
          <h1>Resume Analysis Result</h1>
          <div class="file-info">
            <span class="badge">File</span> ${(lastFileName || 'N/A')}<br/>
          </div>
          <div class="result-content">
            ${simpleMarkdownToHtml(lastMessage)}
          </div>
        </div>
      </body>
      </html>
    `;
    const blob = new Blob([htmlContent], { type: 'text/html' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = (lastFileName || 'resume_analysis') + '.html';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-gray-900 via-gray-800 to-black text-white pt-24 px-2">
      <SpotlightCard className="w-full max-w-5xl bg-gray-900/80 rounded-2xl shadow-2xl p-8 border border-gray-800">
        <div className="grid grid-cols-1 lg:grid-cols-2 md:gap-8 items-stretch">
          {/* Left: Intro Text */}
          <div className="h-full flex flex-col justify-center items-center text-center lg:text-left lg:items-start px-2">
            <h1 className="text-3xl md:text-4xl font-extrabold mb-2 text-purple-400 tracking-tight">Resume Analysis</h1>
            <p className="text-gray-300 mb-4 text-lg">
              Upload your resume and the job description to receive a detailed, AI-powered analysis. Our advanced algorithms will help you optimize your application and increase your chances of landing your dream job.
            </p>
          </div>
          {/* Right: Form and Result */}
          <div className="h-full flex flex-col justify-center py-8 px-2">
            <form
              className="flex flex-col gap-8"
              onSubmit={handleSubmit}
              encType="multipart/form-data"
            >
              {/* PDF Upload */}
              <label className="text-left font-semibold text-white block mb-1">Upload your resume (PDF)</label>
              <label
                className={`flex flex-col items-center justify-center border-2 border-dashed rounded-xl p-5 cursor-pointer transition-all duration-200 ${dragActive ? 'border-purple-500 bg-purple-900/20' : 'border-gray-700 bg-gray-800/40'} hover:border-purple-400`}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
              >
                <input
                  type="file"
                  name="pdf_file"
                  accept="application/pdf"
                  required
                  className="hidden"
                  ref={fileInputRef}
                  onChange={handleFileChange}
                />
                <span className="text-gray-400 text-sm mb-2">Drag & drop or <span className="underline text-purple-400 cursor-pointer" onClick={handleBrowseClick}>browse</span></span>
                {pdfFile ? (
                  <span className="text-green-400 font-semibold mt-2">{pdfFile.name}</span>
                ) : lastFileName ? (
                  <span className="text-green-400 font-semibold mt-2">Last analyzed: {lastFileName}</span>
                ) : (
                  <span className="text-gray-500 mt-2">No file selected</span>
                )}
              </label>
              {/* Job Description */}
              <div>
                <label className="text-left font-semibold text-white block mb-2">Job Description</label>
                <textarea
                  name="job_description"
                  required
                  rows={3}
                  className="block w-full text-sm text-gray-200 bg-gray-900 border border-gray-700 rounded-lg p-2 focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-all duration-200"
                  value={jobDescription}
                  onChange={handleDescriptionChange}
                  maxLength={2000}
                />
                <div className="text-right text-xs text-gray-400 mt-1">{jobDescription.length} / 2000 characters</div>
              </div>
              {/* Submit Button */}
              <button
                type="submit"
                className="bg-gradient-to-r from-purple-600 to-pink-500 hover:from-purple-700 hover:to-pink-600 text-white font-bold py-3 rounded-full transition-all duration-300 flex items-center justify-center gap-2 text-lg shadow-lg disabled:opacity-60 disabled:cursor-not-allowed"
                disabled={loading || !pdfFile}
              >
                {loading && (
                  <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"></path>
                  </svg>
                )}
                {loading ? "Analyzing..." : "Analyze Resume"}
              </button>
              {error && <div className="text-red-400 font-semibold text-center">{error}</div>}
            </form>
          </div>
        </div>
      </SpotlightCard>
      {/* Show last result and file name if available */}
      {lastMessage && (
        <div className="relative bg-gradient-to-br from-gray-900/90 via-gray-950/90 to-black/90 border border-purple-700 rounded-2xl shadow-2xl mt-8 w-full max-w-5xl mx-auto">
          <div className="flex items-center gap-2 px-6 py-3 rounded-t-2xl bg-gradient-to-r from-purple-700 via-purple-500 to-pink-500">
            <svg className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m2 0a8 8 0 11-16 0 8 8 0 0116 0z" /></svg>
            <h2 className="text-lg font-bold text-white tracking-wide">Last Analysis Result</h2>
          </div>
          <div className="px-6 py-6">
            <div className="mb-3 text-base text-gray-400 flex items-center gap-2">
              <span className="font-semibold text-gray-300">File:</span> {lastFileName || 'N/A'}
              <button
                className="ml-2 px-3 py-1 bg-purple-500 hover:bg-purple-700 text-white text-xs font-semibold rounded shadow transition"
                onClick={handleDownloadHtmlResult}
              >
                Download
              </button>
            </div>
            <div className="prose prose-invert prose-lg max-w-none text-white bg-gray-900/60 rounded-xl p-6">
              <div
                className="markdown-tailwind"
                dangerouslySetInnerHTML={{ __html: simpleMarkdownToHtml(lastMessage) }}
              />
            </div>
            <div className="flex justify-center">
              <button
                className="mt-6 bg-purple-500 hover:bg-purple-700 text-white font-bold py-2 px-6 rounded shadow-lg transition"
                onClick={handleDownloadHtmlResult}
              >
                Download
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Analys;