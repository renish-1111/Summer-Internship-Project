import { useNavigate } from 'react-router-dom';
import { FiArrowLeft, FiCheckCircle, FiClipboard, FiAward, FiStar, FiTrendingUp, FiTarget } from 'react-icons/fi';
import SpotlightCard from '../ui/SpotlightCard';

const LearnMore = () => {
  const navigate = useNavigate();

  const workflowSteps = [
    {
      icon: <FiClipboard className="text-pink-400" />,
      text: 'Analyze your resume with our AI-powered tool to extract and optimize your content.',
    },
    {
      icon: <FiTrendingUp className="text-pink-400" />,
      text: 'Check your Match Score to see how well your resume fits a job description.',
    },
    {
      icon: <FiAward className="text-pink-400" />,
      text: 'Generate a Cover Letter tailored to your resume and the job you want.',
    },
  ];

  const improvementTips = [
    {
      icon: <FiTarget className="text-purple-400" />,
      text: 'Use keywords from the job description throughout your resume.',
    },
    {
      icon: <FiStar className="text-purple-400" />,
      text: 'Include relevant skills, certifications, and experience.',
    },
    {
      icon: <FiCheckCircle className="text-purple-400" />,
      text: 'Use standard section headings (e.g., Experience, Education, Skills).',
    },
    {
      icon: <FiClipboard className="text-purple-400" />,
      text: 'Avoid graphics, tables, or unusual fonts that may not be read by all systems.',
    },
    {
      icon: <FiTrendingUp className="text-purple-400" />,
      text: 'Quantify achievements with numbers and results where possible.',
    },
    {
      icon: <FiAward className="text-purple-400" />,
      text: 'Tailor your resume for each job application.',
    },
  ];

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-gray-900 via-black to-gray-900 text-white p-4 sm:p-6 md:p-20">
      <SpotlightCard className="w-full max-w-4xl bg-black/50 backdrop-blur-xl rounded-3xl shadow-2xl p-6 sm:p-8 md:p-10 border border-purple-500/30">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 md:gap-12">
          {/* Left Column: Workflow and Guidance */}
          <div className="flex flex-col gap-8">
            <div className="bg-gradient-to-br from-purple-900/50 to-pink-900/40 border border-purple-600/50 rounded-2xl p-6 shadow-lg">
              <h2 className="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-pink-400 to-purple-400 mb-4 text-center">
                How to Use ResumeAI
              </h2>
              <ul className="space-y-4">
                {workflowSteps.map((step, index) => (
                  <li key={index} className="flex items-start gap-4 p-3 rounded-lg hover:bg-white/5 transition-colors duration-300">
                    <div className="text-2xl mt-1">{step.icon}</div>
                    <p className="text-gray-200 text-lg">{step.text}</p>
                  </li>
                ))}
              </ul>
              <p className="mt-5 text-sm text-gray-400 text-center">
                Start with resume analysis to unlock the full power of our platform!
              </p>
            </div>

            <div className="bg-purple-900/40 border border-purple-700/40 rounded-2xl p-6 shadow-md">
              <h2 className="text-2xl font-bold text-purple-300 mb-3 text-center">Why Optimize Your Resume?</h2>
              <p className="text-lg text-gray-300 text-center">
                A well-optimized resume helps you stand out to both automated systems and human recruiters, increasing your chances of landing interviews.
              </p>
            </div>
          </div>

          {/* Right Column: Tips */}
          <div className="bg-gray-900/50 border border-gray-700 rounded-2xl p-6 shadow-xl">
            <h2 className="text-3xl font-bold text-purple-300 mb-6 text-center">Tips to Improve Your Resume</h2>
            <ul className="space-y-4">
              {improvementTips.map((tip, index) => (
                <li key={index} className="flex items-center gap-4 p-3 rounded-lg hover:bg-white/10 transition-colors duration-300">
                  <div className="text-xl text-purple-400">{tip.icon}</div>
                  <span className="text-gray-200 text-base">{tip.text}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Back Button */}
        <div className="flex justify-center mt-10">
          <button
            className="flex items-center gap-2 bg-purple-600 hover:bg-purple-700 text-white font-bold py-3 px-8 rounded-full shadow-lg hover:shadow-purple-500/50 transform hover:-translate-y-1 transition-all text-lg"
            onClick={() => navigate('/')}
          >
            <FiArrowLeft />
            Back to Home
          </button>
        </div>
      </SpotlightCard>
    </div>
  );
};

export default LearnMore;