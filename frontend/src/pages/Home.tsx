import React from 'react';
import { motion } from 'framer-motion';
import SplitText from "../ui/SplitText.tsx";
import ShinyText from '../ui/ShinyText.tsx';
import SpotlightCard from "../ui/SpotlightCard.tsx";
import { Link } from 'react-router-dom';

const handleAnimationComplete = () => {
  console.log('All letters have animated!');
};

const features = [
  {
    icon: "🤖",
    title: "AI Analysis",
    desc: "Advanced AI algorithms analyze your resume for content, structure, and ATS optimization"
  },
  {
    icon: "📝",
    title: "Cover Letters",
    desc: "Generate personalized cover letters tailored to specific job descriptions"
  },
  {
    icon: "📊",
    title: "ATS Scoring",
    desc: "Get detailed scores and recommendations to pass Applicant Tracking Systems"
  }
];

const steps = [
  {
    num: 1,
    title: "Upload Resume",
    desc: "Upload your PDF resume to our secure platform"
  },
  {
    num: 2,
    title: "AI Analysis",
    desc: "Our AI analyzes content, structure, and optimization"
  },
  {
    num: 3,
    title: "Get Results",
    desc: "Receive detailed feedback and recommendations"
  }
];

const Home = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black text-white pt-32">
      {/* Hero Section */}
      <motion.section
        initial={{ opacity: 0, y: 40 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.7, ease: "easeOut" }}
        viewport={{ once: true, amount: 0.2 }}
        className="text-center content-center justify py-30 max-w-6xl mx-auto my-14"
      >
        {/* Responsive SplitText: "AI-Powered" on one line, "Resume Analysis" below on mobile */}
        <div className="mb-5">
          {/* Mobile: stacked, Desktop: inline */}
          <span className="block md:hidden">
            <SplitText
              text="AI-Powered"
              className="text-5xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text drop-shadow-lg"
              delay={50}
              duration={0.6}
              ease="power3.out"
              splitType="chars"
              from={{ opacity: 0, y: 40 }}
              to={{ opacity: 1, y: 0 }}
              threshold={0.1}
              rootMargin="-100px"
              textAlign="center"
              onLetterAnimationComplete={handleAnimationComplete}
            />
            <SplitText
              text="Resume Analysis"
              className="text-5xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text drop-shadow-lg"
              delay={50}
              duration={0.6}
              ease="power3.out"
              splitType="chars"
              from={{ opacity: 0, y: 40 }}
              to={{ opacity: 1, y: 0 }}
              threshold={0.1}
              rootMargin="-100px"
              textAlign="center"
              onLetterAnimationComplete={handleAnimationComplete}
            />
          </span>
          <span className="hidden md:block">
            <SplitText
              text="AI-Powered Resume Analysis"
              className="text-6xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text drop-shadow-lg"
              delay={50}
              duration={0.6}
              ease="power3.out"
              splitType="chars"
              from={{ opacity: 0, y: 40 }}
              to={{ opacity: 1, y: 0 }}
              threshold={0.1}
              rootMargin="-100px"
              textAlign="center"
              onLetterAnimationComplete={handleAnimationComplete}
            />
          </span>
        </div>
        <p className="text-xl text-gray-300 mb-10 mx-auto max-w-2xl leading-relaxed">
          <ShinyText text="Transform your resume with advanced AI analysis and get personalized feedback to land your dream job" 
          disabled={false} 
          speed={2} 
          className='custom-class' />
        </p>
        <div className="flex flex-col gap-5 justify-center items-center md:flex-row md:gap-5 md:items-stretch md:justify-center">
          <button className="bg-purple-600 hover:bg-purple-700 border-2 border-purple-500 text-white px-8 py-4 text-lg rounded-full font-bold transition-all duration-300 shadow-lg hover:shadow-purple-500/25">
            Get Started
          </button>
          <Link to="/learn-more">
            <button className="bg-transparent hover:bg-gray-800 border-2 border-gray-600 hover:border-purple-400 text-white px-8 py-4 text-lg rounded-full transition-all duration-300">
              Learn More
            </button>
          </Link>
        </div>
      </motion.section>

      {/* Features Section */}
      <section className="bg-gray-900/50 backdrop-blur-lg py-20 px-5 border-y border-gray-700">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-center text-4xl font-bold mb-15 text-white">
            Why Choose ResumeAI?
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-10 mt-15 items-stretch">
            {features.map((feature, idx) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 * idx, duration: 0.6, ease: "easeOut" }}
                viewport={{ once: true, amount: 0.2 }}
                className="h-full flex"
              >
                <SpotlightCard className="h-full flex flex-col justify-between text-center p-6 bg-gray-800/30 rounded-xl backdrop-blur-sm border border-gray-700 hover:border-purple-500 transition-all duration-300">
                  <div>
                    <div className="text-5xl mb-5 bg-purple-600/20 w-20 h-20 rounded-full flex items-center justify-center mx-auto border border-purple-500/30">
                      {feature.icon}
                    </div>
                    <h3 className="text-xl font-semibold mb-4 text-purple-300">{feature.title}</h3>
                    <p className="text-gray-400 leading-relaxed">{feature.desc}</p>
                  </div>
                </SpotlightCard>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-20 px-5">
        <div className="max-w-6xl mx-auto text-center">
          <h2 className="text-4xl font-bold mb-15 text-white">
            How It Works
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-10 mt-15">
            {steps.map((step, idx) => (
              <motion.div
                key={step.num}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 * idx, duration: 0.6, ease: "easeOut" }}
                viewport={{ once: true, amount: 0.2 }}
                className="group"
              >
                <div className="text-2xl font-bold bg-gradient-to-r from-purple-500 to-pink-500 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-5 group-hover:scale-110 transition-transform duration-300">
                  {step.num}
                </div>
                <h3 className="text-xl font-semibold mb-4 text-purple-300">{step.title}</h3>
                <p className="text-gray-400">{step.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <motion.footer
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        transition={{ duration: 1, delay: 0.5 }}
        viewport={{ once: true, amount: 0.2 }}
        className="bg-black/40 py-10 px-5 text-center border-t border-gray-700"
      >
        <div className="max-w-6xl mx-auto">
          <p className="text-gray-400">
            © 2025 ResumeAI. Powered by AI technology to boost your career.
          </p>
        </div>
      </motion.footer>
    </div>
  );
}

export default Home;