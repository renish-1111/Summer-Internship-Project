import { BrowserRouter, Routes, Route, Link, useLocation } from "react-router-dom";
import { useState } from "react";
import Home from "./pages/Home";
import Analys from "./pages/Analys";
import CoverLatter from "./pages/cover_latter";
import AtsScore from "./pages/AtsScore";
import LearnMore from "./pages/LearnMore";




function Navbar() {
  const location = useLocation();
  const [menuOpen, setMenuOpen] = useState(false);
  const navLinks = [
    { to: "/", label: "Home" },
    { to: "/analys", label: "Analys" },
    { to: "/cover_latter", label: "Cover Latter" },
    { to: "/ats_score", label: "ATS Score" },
  ];
  const navPositionClass = "fixed top-0 w-full";
  return (
    <nav className={`backdrop-blur-lg bg-gradient-to-r from-gray-900/80 via-gray-800/80 to-black/80 border-b border-gray-700 shadow-lg z-50 ${navPositionClass} `}>
      <div className="max-w-6xl mx-auto flex items-center justify-between px-5 py-3">
        <span className="text-2xl font-bold text-purple-400 tracking-tight">ResumeAI</span>
        {/* Hamburger for mobile */}
        <button
          className="md:hidden flex flex-col justify-center items-center w-10 h-10 focus:outline-none"
          onClick={() => setMenuOpen(!menuOpen)}
          aria-label="Toggle menu"
        >
          <span className={`block w-6 h-0.5 bg-purple-400 mb-1 transition-all duration-300 ${menuOpen ? 'rotate-45 translate-y-1.5' : ''}`}></span>
          <span className={`block w-6 h-0.5 bg-purple-400 mb-1 transition-all duration-300 ${menuOpen ? 'opacity-0' : ''}`}></span>
          <span className={`block w-6 h-0.5 bg-purple-400 transition-all duration-300 ${menuOpen ? '-rotate-45 -translate-y-1.5' : ''}`}></span>
        </button>
        {/* Desktop menu */}
        <div className="hidden md:flex gap-6">
          {navLinks.map(link => (
            <Link
              key={link.to}
              to={link.to}
              className={`px-4 py-2 rounded-full font-semibold transition-all duration-200 text-white hover:bg-purple-700/70 hover:text-purple-200 focus:outline-none focus:ring-2 focus:ring-purple-400/50 md:${location.pathname === link.to ? 'bg-purple-600/80 text-purple-100 shadow-md' : ''}`}
              onClick={() => setMenuOpen(false)}
            >
              {link.label}
            </Link>
          ))}
        </div>
      </div>
      {/* Mobile menu */}
      {menuOpen && (
        <div className="md:hidden px-5 pb-4 bg-gradient-to-r from-gray-900/95 via-gray-800/95 to-black/95 border-b border-gray-700 shadow-lg animate-fade-in-down">
          <div className="flex flex-col gap-2">
            {navLinks.map(link => (
              <Link
                key={link.to}
                to={link.to}
                className={`block px-4 py-3 rounded-xl font-semibold transition-all duration-200 text-white hover:bg-purple-700/70 hover:text-purple-200 focus:outline-none focus:ring-2 focus:ring-purple-400/50`}
                onClick={() => setMenuOpen(false)}
              >
                {link.label}
              </Link>
            ))}
          </div>
        </div>
      )}
    </nav>
  );
}

export default function App() {
  return (
    
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/analys" element={<Analys />} />
        <Route path="/cover_latter" element={<CoverLatter />} />
        <Route path="/ats_score" element={<AtsScore />} />
        <Route path="/learn-more" element={<LearnMore />} />
      </Routes>
    </BrowserRouter>
  );

}

