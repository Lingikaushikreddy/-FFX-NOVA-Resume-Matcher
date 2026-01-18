import React, { useState, useCallback, useRef } from 'react';
import { motion, AnimatePresence, useSpring, useMotionTemplate, useMotionValue } from 'framer-motion';
import { Upload, CheckCircle, Loader2, FileType, AlertCircle } from 'lucide-react';
import { cn } from '../lib/utils';
import { apiClient } from '../api/client';

export function FileUploadZone({ onMatchesComplete }: { onMatchesComplete?: (resumeId: string) => void }) {
  const [isDragging, setIsDragging] = useState(false);
  const [status, setStatus] = useState<'idle' | 'uploading' | 'success' | 'error'>('idle');
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [progress, setProgress] = useState(0);
  const [uploadedResumeId, setUploadedResumeId] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Mouse tilt effect logic
  const ref = useRef<HTMLDivElement>(null);
  const x = useMotionValue(0);
  const y = useMotionValue(0);
  const mouseXSpring = useSpring(x);
  const mouseYSpring = useSpring(y);

  const rotateX = useMotionTemplate`${mouseYSpring}deg`;
  const rotateY = useMotionTemplate`${mouseXSpring}deg`;

  const handleMouseMove = (e: React.MouseEvent) => {
    if (!ref.current) return;
    const rect = ref.current.getBoundingClientRect();
    const width = rect.width;
    const height = rect.height;
    const mouseX = e.clientX - rect.left;
    const mouseY = e.clientY - rect.top;
    const xPct = mouseX / width - 0.5;
    const yPct = mouseY / height - 0.5;
    x.set(xPct * 10); // Tilt strength
    y.set(yPct * -10);
  };

  const handleMouseLeave = () => {
    x.set(0);
    y.set(0);
    setIsDragging(false);
  };

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const droppedFile = e.dataTransfer.files[0];
    validateAndUpload(droppedFile);
  }, []);

  const validateAndUpload = (file: File | undefined) => {
    if (!file) return;
    if (!file.name.toLowerCase().endsWith('.pdf') && !file.name.toLowerCase().endsWith('.docx')) {
      setStatus('error');
      setErrorMessage("Only .pdf and .docx files are supported.");
      return;
    }
    handleUpload(file);
  };

  const handleUpload = async (uploadedFile: File) => {
    setStatus('uploading');
    setProgress(10);
    setErrorMessage(null);

    const interval = setInterval(() => {
      setProgress(prev => (prev >= 90 ? 90 : prev + 10));
    }, 400);

    try {
      const response = await apiClient.uploadResume(uploadedFile);
      clearInterval(interval);
      setProgress(100);
      setStatus('success');
      setUploadedResumeId(response.resume_id);
    } catch (error: any) {
      clearInterval(interval);
      setStatus('error');
      setErrorMessage(error.message || "Upload failed. Please try again.");
    }
  };

  return (
    <div id="upload-zone" className="w-full max-w-xl mx-auto p-4 perspective-[1000px]">
      <AnimatePresence mode="wait">
        {status === 'success' ? (
          <SuccessCard
            onReset={() => { setStatus('idle'); setProgress(0); setUploadedResumeId(null); }}
            onViewMatches={() => uploadedResumeId && onMatchesComplete?.(uploadedResumeId)}
          />
        ) : (
          <motion.div
            ref={ref}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95 }}
            style={{ rotateX, rotateY, transformStyle: "preserve-3d" }}
            onMouseMove={handleMouseMove}
            onMouseLeave={handleMouseLeave}
            className={cn(
              "relative glass-card rounded-3xl p-10 text-center cursor-pointer transition-all duration-300 group",
              isDragging ? "border-primary-400 shadow-[0_0_50px_rgba(59,130,246,0.3)] scale-[1.02]" : "hover:border-white/20"
            )}
            onClick={() => fileInputRef.current?.click()}
            onDragOver={handleDragOver}
            onDragLeave={handleMouseLeave}
            onDrop={handleDrop}
          >
            <input
              ref={fileInputRef}
              type="file"
              className="hidden"
              accept=".pdf,.docx"
              onChange={(e) => validateAndUpload(e.target.files?.[0])}
              disabled={status === 'uploading'}
            />

            {/* Glowing Border Gradient */}
            <div className="absolute inset-0 rounded-3xl bg-gradient-to-r from-primary-500/20 to-secondary-500/20 opacity-0 group-hover:opacity-100 transition-opacity blur-xl pointer-events-none" />

            <div className="relative z-10 flex flex-col items-center gap-6 transform-gpu translate-z-10">

              {/* Icon Container */}
              <div className="relative">
                {/* Ripple effect rings */}
                {status === 'uploading' && (
                  <>
                    <motion.div
                      animate={{ scale: [1, 2], opacity: [0.5, 0] }}
                      transition={{ repeat: Infinity, duration: 2 }}
                      className="absolute inset-0 bg-primary-500 rounded-full z-0"
                    />
                    <motion.div
                      animate={{ scale: [1, 1.5], opacity: [0.5, 0] }}
                      transition={{ repeat: Infinity, duration: 2, delay: 0.5 }}
                      className="absolute inset-0 bg-primary-400 rounded-full z-0"
                    />
                  </>
                )}

                <div className={cn(
                  "w-24 h-24 rounded-2xl flex items-center justify-center transition-all duration-500 shadow-2xl relative z-10",
                  status === 'error' ? "bg-red-500/10 text-red-500 border border-red-500/30" :
                    "bg-gradient-to-br from-slate-800 to-slate-900 border border-white/10 group-hover:scale-110 group-hover:shadow-primary-500/25"
                )}>
                  {status === 'uploading' ? (
                    <span className="text-xl font-bold text-primary-400 font-mono">{progress}%</span>
                  ) : status === 'error' ? (
                    <AlertCircle className="w-10 h-10" />
                  ) : (
                    <Upload className="w-10 h-10 text-slate-300 group-hover:text-white transition-colors" />
                  )}
                </div>
              </div>

              <div className="space-y-2">
                <h3 className="text-2xl font-bold text-white tracking-tight">
                  {status === 'uploading' ? 'Analyzing Resume...' : status === 'error' ? 'Upload Failed' : 'Drop Resume Here'}
                </h3>
                <p className="text-slate-400">
                  {status === 'error' ? errorMessage : "PDF or DOCX (Max 10MB)"}
                </p>
              </div>

              {/* Progress Ring / Button */}
              {status === 'uploading' && (
                <div className="w-full max-w-xs h-1.5 bg-slate-800 rounded-full overflow-hidden relative mt-4">
                  <motion.div
                    className="absolute inset-0 bg-gradient-to-r from-primary-500 to-secondary-500"
                    initial={{ width: 0 }}
                    animate={{ width: `${progress}%` }}
                  />
                  <div className="absolute inset-0 bg-white/20 blur-[2px]" />
                </div>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

function SuccessCard({ onReset, onViewMatches }: { onReset: () => void, onViewMatches: () => void }) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      className="glass-card rounded-3xl p-8 text-center"
    >
      <div className="w-20 h-20 mx-auto bg-green-500/10 rounded-full flex items-center justify-center mb-6 border border-green-500/20">
        <CheckCircle className="w-10 h-10 text-green-400" />
      </div>
      <h3 className="text-2xl font-bold text-white mb-2">Analysis Complete</h3>
      <p className="text-slate-400 mb-8">We've matched your profile to 24 active high-clearance roles.</p>

      <div className="flex flex-col sm:flex-row gap-4 justify-center">
        <button onClick={onReset} className="px-6 py-3 text-slate-400 hover:text-white transition-colors font-medium">
          Upload Another
        </button>
        <button onClick={onViewMatches} className="px-8 py-3 bg-gradient-to-r from-primary-600 to-secondary-600 text-white rounded-xl font-bold shadow-lg shadow-primary-500/20 hover:scale-105 transition-transform">
          View Matches
        </button>
      </div>
    </motion.div>
  );
}
