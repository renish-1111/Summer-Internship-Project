import { useNavigate } from 'react-router-dom';
import SpotlightCard from '../ui/SpotlightCard';

const LearnMore = () => {
  const navigate = useNavigate();
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-gray-900 via-gray-800 to-black text-white pt-24 px-2">
      <SpotlightCard className="w-full max-w-3xl bg-gray-900/80 rounded-2xl shadow-2xl p-8 border border-gray-800 flex flex-col items-center">
        {/* Workflow Section */}
        <div className="bg-gradient-to-r from-purple-700/30 via-purple-900/30 to-pink-700/20 border border-purple-600 rounded-xl p-4 mb-8 w-full flex flex-col items-center">
          <h2 className="text-2xl font-bold text-pink-300 mb-2 text-center">How to Use ResumeAI</h2>
          <ol className="list-decimal list-inside text-gray-100 text-lg space-y-2 max-w-xl mx-auto text-center">
            <li><span className="font-semibold text-purple-200">Analyze your resume</span> with our AI-powered tool to extract and optimize your content.</li>
            <li><span className="font-semibold text-purple-200">Check your Match Score</span> to see how well your resume fits a job description.</li>
            <li><span className="font-semibold text-purple-200">Generate a Cover Letter</span> tailored to your resume and the job you want.</li>
          </ol>
          <p className="mt-3 text-base text-gray-300">Start with resume analysis to unlock the full power of match scoring and cover letter generation!</p>
        </div>
        {/* General Resume Guidance Section */}
        <div className="bg-purple-900/30 border border-purple-700 rounded-xl p-4 mb-6 w-full">
          <h2 className="text-2xl font-bold text-purple-300 mb-2">Why Optimize Your Resume?</h2>
          <p className="text-lg text-gray-200 text-center">
            A well-optimized resume helps you stand out to both automated systems and human recruiters. It increases your chances of passing initial screenings and landing interviews for your desired roles.
          </p>
        </div>
        <div className="w-full mb-6">
          <h2 className="text-2xl font-bold text-purple-300 mb-2 text-center">Tips to Improve Your Resume</h2>
          <ul className="list-none text-gray-100 text-base space-y-3 mx-auto max-w-xl">
            <li><span className="mr-2">✅</span>Use keywords from the job description throughout your resume.</li>
            <li><span className="mr-2">💡</span>Include relevant skills, certifications, and experience.</li>
            <li><span className="mr-2">📄</span>Use standard section headings (e.g., Experience, Education, Skills).</li>
            <li><span className="mr-2">🚫</span>Avoid graphics, tables, or unusual fonts that may not be read by all systems.</li>
            <li><span className="mr-2">🔢</span>Quantify achievements with numbers and results where possible.</li>
            <li><span className="mr-2">🎯</span>Tailor your resume for each job application.</li>
          </ul>
        </div>
        
        <div className="flex gap-4 mt-8">
          <button
            className="bg-purple-600 hover:bg-purple-700 text-white font-bold py-2 px-8 rounded shadow-lg transition text-lg"
            onClick={() => navigate('/')}
          >
            Back to Home
          </button>
          
        </div>
      </SpotlightCard>
    </div>
  );
};

export default LearnMore; 