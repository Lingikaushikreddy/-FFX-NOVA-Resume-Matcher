import { useState } from 'react';
import { HeroSection } from './components/HeroSection';
import { FileUploadZone } from './components/FileUploadZone';
import { JobResultsPage } from './components/JobResultsPage';
import { JobMatchGrid } from './components/JobMatchGrid';
import { Shield, Lock, Zap } from 'lucide-react';

function App() {
  const [resumeId, setResumeId] = useState<string | null>(null);

  // If showing results (resumeId exists), render that page
  if (resumeId) {
    return (
      <>
        {/* Simple Nav for Results Page */}
        <nav className="fixed top-0 w-full bg-slate-950/80 backdrop-blur-md border-b border-white/5 z-50">
          <div className="container mx-auto px-4 h-16 flex items-center justify-between">
            <div className="flex items-center gap-2 cursor-pointer" onClick={() => setResumeId(null)}>
              <div className="w-8 h-8 bg-gradient-to-br from-primary-600 to-secondary-600 rounded-lg shadow-lg shadow-primary-500/20" />
              <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary-100 to-white font-display">
                FFX NOVA
              </span>
            </div>
            <div className="flex items-center gap-4">
              <div className="w-8 h-8 rounded-full bg-slate-800 overflow-hidden border border-slate-700">
                <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Felix" alt="User" />
              </div>
            </div>
          </div>
        </nav>
        <JobResultsPage resumeId={resumeId} />
      </>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 selection:bg-primary-500/30 selection:text-primary-100">
      {/* Navigation */}
      <nav className="fixed top-0 w-full bg-slate-950/80 backdrop-blur-md border-b border-white/5 z-50">
        <div className="container mx-auto px-4 h-20 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-gradient-to-br from-primary-600 to-secondary-600 rounded-lg shadow-lg shadow-primary-500/20" />
            <span className="text-xl font-bold text-white font-display tracking-tight">
              FFX NOVA
            </span>
          </div>
          <div className="hidden md:flex items-center gap-8 text-sm font-medium text-slate-400">
            <a href="#" className="hover:text-white transition-colors">Find Jobs</a>
            <a href="#" className="hover:text-white transition-colors">For Employers</a>
            <a href="#" className="hover:text-white transition-colors">Upskilling</a>
            <button className="px-5 py-2.5 text-white bg-white/5 border border-white/10 rounded-lg hover:bg-white/10 transition-all font-semibold">
              Sign In
            </button>
          </div>
        </div>
      </nav>

      <main>
        <HeroSection />

        <section id="upload-zone" className="relative py-20">
          <div className="container mx-auto px-4">
            {/* Section Header */}
            <div className="text-center mb-16 relative z-10">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-secondary-500/10 border border-secondary-500/20 text-secondary-400 text-xs font-bold mb-4 uppercase tracking-wider">
                <Zap className="w-3 h-3" /> Instant Analysis
              </div>
              <h2 className="text-3xl md:text-5xl font-bold text-white mb-6 font-display">
                Upload Your Resume
              </h2>
              <p className="text-lg text-slate-400 max-w-2xl mx-auto font-light">
                Our AI extracts your skills, clearance level, and experience to find hidden matches in the defense sector.
              </p>
            </div>

            <FileUploadZone onMatchesComplete={(id) => setResumeId(id)} />
          </div>
        </section>

        <section className="py-20 bg-slate-900/50 border-t border-white/5 relative overflow-hidden">
          {/* Decorative blurred blobs */}
          <div className="absolute top-0 right-0 w-[600px] h-[600px] bg-primary-900/10 rounded-full blur-[120px] pointer-events-none" />

          <div className="container mx-auto px-4">
            <JobMatchGrid />
          </div>
        </section>

        {/* Footer Stub */}
        <footer className="py-12 border-t border-white/5 bg-slate-950">
          <div className="container mx-auto px-4 text-center text-slate-500 text-sm">
            <div className="flex justify-center items-center gap-2 mb-4">
              <Shield className="w-5 h-5 text-slate-600" />
              <Lock className="w-5 h-5 text-slate-600" />
            </div>
            <p>&copy; 2025 FFX NOVA. Secure Career Intelligence for National Defense.</p>
          </div>
        </footer>

      </main>
    </div>
  );
}

export default App;
