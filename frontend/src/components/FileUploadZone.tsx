/**
 * Premium File Upload Zone - FFX NOVA
 * Beautiful drag-and-drop with animations and progress states
 */

import { useState, useCallback, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Upload,
  FileText,
  CheckCircle,
  AlertCircle,
  Loader2,
  X,
  Sparkles,
  FileUp,
  Zap,
  Shield,
  Target,
} from 'lucide-react';

interface FileUploadZoneProps {
  onMatchesComplete?: () => void;
}

type UploadState = 'idle' | 'dragging' | 'uploading' | 'parsing' | 'success' | 'error';

interface ParsedData {
  name: string;
  email: string;
  skills: string[];
  experience: number;
  clearance?: string;
}

export function FileUploadZone({ onMatchesComplete }: FileUploadZoneProps) {
  const [state, setState] = useState<UploadState>('idle');
  const [progress, setProgress] = useState(0);
  const [file, setFile] = useState<File | null>(null);
  const [parsedData, setParsedData] = useState<ParsedData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setState('dragging');
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setState('idle');
  }, []);

  const simulateUpload = useCallback(async (uploadedFile: File) => {
    setFile(uploadedFile);
    setState('uploading');
    setProgress(0);

    // Simulate upload progress
    for (let i = 0; i <= 100; i += 5) {
      await new Promise((r) => setTimeout(r, 50));
      setProgress(i);
    }

    // Parsing state
    setState('parsing');
    await new Promise((r) => setTimeout(r, 1500));

    // Simulate parsed data
    setParsedData({
      name: 'John Doe',
      email: 'john.doe@example.com',
      skills: ['Python', 'AWS', 'Docker', 'Kubernetes', 'React', 'PostgreSQL', 'CI/CD'],
      experience: 7,
      clearance: 'Secret',
    });

    setState('success');

    // Auto-navigate after success
    setTimeout(() => {
      onMatchesComplete?.();
    }, 2000);
  }, [onMatchesComplete]);

  const handleDrop = useCallback(
    async (e: React.DragEvent) => {
      e.preventDefault();
      const droppedFile = e.dataTransfer.files[0];
      if (droppedFile && (droppedFile.type === 'application/pdf' || droppedFile.name.endsWith('.docx'))) {
        await simulateUpload(droppedFile);
      } else {
        setState('error');
        setError('Please upload a PDF or DOCX file');
      }
    },
    [simulateUpload]
  );

  const handleFileSelect = useCallback(
    async (e: React.ChangeEvent<HTMLInputElement>) => {
      const selectedFile = e.target.files?.[0];
      if (selectedFile) {
        await simulateUpload(selectedFile);
      }
    },
    [simulateUpload]
  );

  const reset = () => {
    setState('idle');
    setFile(null);
    setParsedData(null);
    setError(null);
    setProgress(0);
  };

  return (
    <div className="max-w-3xl mx-auto">
      <AnimatePresence mode="wait">
        {state === 'idle' || state === 'dragging' ? (
          <motion.div
            key="dropzone"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
            className={`relative cursor-pointer rounded-3xl border-2 border-dashed p-12 transition-all duration-300 ${
              state === 'dragging'
                ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20 scale-[1.02]'
                : 'border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800/50 hover:border-primary-400 hover:bg-slate-50 dark:hover:bg-slate-800'
            }`}
          >
            {/* Animated Border Gradient (on drag) */}
            {state === 'dragging' && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="absolute inset-0 rounded-3xl bg-gradient-to-r from-primary-500 via-secondary-500 to-accent-500 opacity-20 blur-sm"
              />
            )}

            <div className="relative text-center">
              <motion.div
                animate={state === 'dragging' ? { scale: 1.1, y: -10 } : { scale: 1, y: 0 }}
                transition={{ type: 'spring', stiffness: 300 }}
                className="mx-auto mb-6"
              >
                <div className="relative inline-flex">
                  <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-primary-500 to-secondary-500 flex items-center justify-center shadow-lg shadow-primary-500/25">
                    <Upload className="w-10 h-10 text-white" />
                  </div>
                  <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 20, repeat: Infinity, ease: 'linear' }}
                    className="absolute -inset-2 rounded-2xl border-2 border-dashed border-primary-300 dark:border-primary-700"
                  />
                </div>
              </motion.div>

              <h3 className="text-xl font-semibold text-slate-900 dark:text-white mb-2">
                {state === 'dragging' ? 'Drop your resume here!' : 'Upload Your Resume'}
              </h3>
              <p className="text-slate-600 dark:text-slate-400 mb-4">
                Drag and drop your resume or{' '}
                <span className="text-primary-600 dark:text-primary-400 font-medium">browse files</span>
              </p>

              {/* File Types */}
              <div className="flex items-center justify-center gap-4">
                <div className="flex items-center gap-2 px-4 py-2 rounded-full bg-slate-100 dark:bg-slate-700">
                  <FileText className="w-4 h-4 text-red-500" />
                  <span className="text-sm font-medium text-slate-700 dark:text-slate-300">PDF</span>
                </div>
                <div className="flex items-center gap-2 px-4 py-2 rounded-full bg-slate-100 dark:bg-slate-700">
                  <FileText className="w-4 h-4 text-blue-500" />
                  <span className="text-sm font-medium text-slate-700 dark:text-slate-300">DOCX</span>
                </div>
              </div>
            </div>

            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf,.docx"
              onChange={handleFileSelect}
              className="hidden"
            />
          </motion.div>
        ) : state === 'uploading' ? (
          <motion.div
            key="uploading"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            className="rounded-3xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 p-12 shadow-xl"
          >
            <div className="text-center">
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
                className="w-16 h-16 mx-auto mb-6 rounded-2xl bg-gradient-to-br from-primary-500 to-secondary-500 flex items-center justify-center"
              >
                <FileUp className="w-8 h-8 text-white" />
              </motion.div>

              <h3 className="text-xl font-semibold text-slate-900 dark:text-white mb-2">
                Uploading {file?.name}
              </h3>

              {/* Progress Bar */}
              <div className="max-w-md mx-auto mt-6">
                <div className="flex justify-between text-sm text-slate-600 dark:text-slate-400 mb-2">
                  <span>Uploading...</span>
                  <span>{progress}%</span>
                </div>
                <div className="h-3 bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${progress}%` }}
                    className="h-full bg-gradient-to-r from-primary-500 to-secondary-500 rounded-full"
                  />
                </div>
              </div>
            </div>
          </motion.div>
        ) : state === 'parsing' ? (
          <motion.div
            key="parsing"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            className="rounded-3xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 p-12 shadow-xl"
          >
            <div className="text-center">
              <motion.div
                animate={{ scale: [1, 1.1, 1] }}
                transition={{ duration: 1.5, repeat: Infinity }}
                className="w-16 h-16 mx-auto mb-6 rounded-2xl bg-gradient-to-br from-secondary-500 to-accent-500 flex items-center justify-center"
              >
                <Sparkles className="w-8 h-8 text-white" />
              </motion.div>

              <h3 className="text-xl font-semibold text-slate-900 dark:text-white mb-2">
                AI is Analyzing Your Resume
              </h3>
              <p className="text-slate-600 dark:text-slate-400">
                Extracting skills, experience, and qualifications...
              </p>

              {/* Animated Dots */}
              <div className="flex justify-center gap-2 mt-6">
                {[0, 1, 2].map((i) => (
                  <motion.div
                    key={i}
                    animate={{ y: [0, -10, 0] }}
                    transition={{ duration: 0.6, repeat: Infinity, delay: i * 0.2 }}
                    className="w-3 h-3 rounded-full bg-gradient-to-r from-primary-500 to-secondary-500"
                  />
                ))}
              </div>
            </div>
          </motion.div>
        ) : state === 'success' ? (
          <motion.div
            key="success"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            className="rounded-3xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 p-8 shadow-xl"
          >
            <div className="text-center mb-8">
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ type: 'spring', stiffness: 200 }}
                className="w-16 h-16 mx-auto mb-4 rounded-full bg-green-100 dark:bg-green-900/30 flex items-center justify-center"
              >
                <CheckCircle className="w-8 h-8 text-green-600 dark:text-green-400" />
              </motion.div>
              <h3 className="text-xl font-semibold text-slate-900 dark:text-white mb-2">
                Resume Analyzed Successfully!
              </h3>
            </div>

            {/* Parsed Data Preview */}
            {parsedData && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
                className="bg-slate-50 dark:bg-slate-900/50 rounded-2xl p-6 space-y-4"
              >
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium text-slate-600 dark:text-slate-400">Candidate</span>
                  <span className="font-semibold text-slate-900 dark:text-white">{parsedData.name}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium text-slate-600 dark:text-slate-400">Experience</span>
                  <span className="font-semibold text-slate-900 dark:text-white">{parsedData.experience}+ years</span>
                </div>
                {parsedData.clearance && (
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium text-slate-600 dark:text-slate-400">Clearance</span>
                    <span className="px-3 py-1 rounded-full bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400 text-sm font-medium">
                      {parsedData.clearance}
                    </span>
                  </div>
                )}
                <div>
                  <span className="text-sm font-medium text-slate-600 dark:text-slate-400 block mb-2">Skills Detected</span>
                  <div className="flex flex-wrap gap-2">
                    {parsedData.skills.map((skill, i) => (
                      <motion.span
                        key={skill}
                        initial={{ opacity: 0, scale: 0.8 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ delay: 0.3 + i * 0.05 }}
                        className="px-3 py-1 rounded-full bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-400 text-sm font-medium"
                      >
                        {skill}
                      </motion.span>
                    ))}
                  </div>
                </div>
              </motion.div>
            )}

            {/* Finding Matches CTA */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.5 }}
              className="mt-6 text-center"
            >
              <div className="flex items-center justify-center gap-2 text-primary-600 dark:text-primary-400">
                <Zap className="w-5 h-5" />
                <span className="font-medium">Finding your best job matches...</span>
                <Loader2 className="w-5 h-5 animate-spin" />
              </div>
            </motion.div>
          </motion.div>
        ) : (
          <motion.div
            key="error"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            className="rounded-3xl bg-white dark:bg-slate-800 border border-red-200 dark:border-red-800 p-12 shadow-xl"
          >
            <div className="text-center">
              <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-red-100 dark:bg-red-900/30 flex items-center justify-center">
                <AlertCircle className="w-8 h-8 text-red-600 dark:text-red-400" />
              </div>
              <h3 className="text-xl font-semibold text-slate-900 dark:text-white mb-2">Upload Failed</h3>
              <p className="text-slate-600 dark:text-slate-400 mb-6">{error || 'Something went wrong'}</p>
              <button
                onClick={reset}
                className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-slate-100 dark:bg-slate-700 hover:bg-slate-200 dark:hover:bg-slate-600 text-slate-900 dark:text-white font-medium transition-colors"
              >
                <X className="w-4 h-4" />
                Try Again
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Features */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6"
      >
        {[
          { icon: Zap, title: 'Instant Analysis', desc: 'AI-powered parsing in seconds' },
          { icon: Shield, title: 'Clearance Aware', desc: 'Matches your security level' },
          { icon: Target, title: 'Smart Matching', desc: '95% accuracy rate' },
        ].map((feature, i) => (
          <motion.div
            key={feature.title}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 + i * 0.1 }}
            className="flex items-center gap-4 p-4 rounded-2xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700"
          >
            <div className="p-3 rounded-xl bg-gradient-to-br from-primary-500/10 to-secondary-500/10">
              <feature.icon className="w-6 h-6 text-primary-600 dark:text-primary-400" />
            </div>
            <div>
              <h4 className="font-semibold text-slate-900 dark:text-white">{feature.title}</h4>
              <p className="text-sm text-slate-600 dark:text-slate-400">{feature.desc}</p>
            </div>
          </motion.div>
        ))}
      </motion.div>
    </div>
  );
}
