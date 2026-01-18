import { useRef } from 'react';
import { motion, useScroll, useTransform, useSpring, useMotionValue, useMotionTemplate } from 'framer-motion';
import { FileText, Briefcase, ChevronRight, Upload, CheckCircle, Shield } from 'lucide-react';
import { AtmosphereParticles } from './ui/AtmosphereParticles';

export function HeroSection() {
  const containerRef = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ["start start", "end start"]
  });

  // Parallax & Fade effects
  const yText = useTransform(scrollYProgress, [0, 1], ["0%", "40%"]);
  const opacityText = useTransform(scrollYProgress, [0, 0.4], [1, 0]);
  const scaleCards = useTransform(scrollYProgress, [0, 1], [1, 0.8]);
  const rotateOrbits = useTransform(scrollYProgress, [0, 1], [0, 45]);

  return (
    <div ref={containerRef} className="relative min-h-screen flex items-center justify-center overflow-hidden bg-slate-950 perspective-[2000px]">
      <AtmosphereParticles />

      {/* Cinematic Spotlight */}
      <div className="absolute top-[-20%] left-1/2 -translate-x-1/2 w-[1000px] h-[1000px] bg-primary-500/10 rounded-full blur-[120px] pointer-events-none" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[800px] h-[800px] bg-secondary-600/5 rounded-full blur-[100px] pointer-events-none" />

      {/* Grain Overlay */}
      <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20 brightness-100 pointer-events-none mix-blend-overlay"></div>

      <div className="container relative z-10 px-4 pt-20">
        <div className="grid lg:grid-cols-2 gap-16 items-center">

          {/* Text Content */}
          <motion.div
            style={{ y: yText, opacity: opacityText }}
            initial={{ opacity: 0, x: -30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 1, ease: "easeOut" }}
            className="space-y-8 relative z-20"
          >
            {/* Badge */}
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-slate-800/50 border border-slate-700/50 backdrop-blur-md shadow-lg"
            >
              <div className="flex h-2 w-2 relative">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
              </div>
              <span className="text-xs font-medium text-slate-300 tracking-wide uppercase">AI Career Intelligence</span>
            </motion.div>

            {/* Headline */}
            <h1 className="text-5xl lg:text-7xl font-bold tracking-tight text-white leading-[1.1]">
              Target Your <br />
              <span className="text-gradient-primary animate-gradient bg-[length:200%_auto]">
                Next Mission
              </span>
            </h1>

            <p className="text-lg text-slate-400 max-w-lg leading-relaxed font-light">
              The only AI-powered platform designed for
              <span className="text-slate-200 font-medium mx-1">Federal</span>,
              <span className="text-slate-200 font-medium mx-1">Military</span>, and
              <span className="text-slate-200 font-medium mx-1">Tech</span>
              professionals in Northern Virginia. Match by capability, not just keywords.
            </p>

            {/* Buttons */}
            <div className="flex flex-wrap gap-4 pt-2">
              <button
                onClick={() => document.getElementById('upload-zone')?.scrollIntoView({ behavior: 'smooth' })}
                className="group relative px-8 py-4 bg-primary-600 hover:bg-primary-500 text-white rounded-xl font-semibold shadow-2xl shadow-primary-600/30 transition-all hover:scale-[1.02] active:scale-[0.98] overflow-hidden"
              >
                <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent translate-x-[-200%] group-hover:animate-shimmer" />
                <span className="flex items-center gap-2 relative z-10">
                  Upload Resume <Upload className="w-5 h-5 group-hover:-translate-y-1 transition-transform" />
                </span>
              </button>

              <button className="px-8 py-4 bg-white/5 hover:bg-white/10 text-white border border-white/10 rounded-xl font-semibold backdrop-blur-sm transition-all flex items-center gap-2">
                Explore Jobs <ChevronRight className="w-4 h-4 text-slate-400" />
              </button>
            </div>

            {/* Trust Badges */}
            <div className="pt-8 flex items-center gap-6 text-sm font-medium text-slate-500 border-t border-white/5">
              <div className="flex items-center gap-2">
                <Shield className="w-4 h-4 text-emerald-500" />
                <span>Secret+ Clearance Ready</span>
              </div>
              <div className="flex items-center gap-2">
                <Briefcase className="w-4 h-4 text-blue-500" />
                <span>10k+ Federal Roles</span>
              </div>
            </div>
          </motion.div>

          {/* 3D Visual - Orbiting Cards */}
          <div className="relative h-[600px] w-full hidden lg:flex items-center justify-center perspective-[2000px] z-10">
            <motion.div
              style={{ scale: scaleCards, rotateY: rotateOrbits }}
              className="relative w-full h-full flex items-center justify-center preserve-3d"
            >
              {/* Central Resume Card */}
              <FloatingCard
                delay={0}
                className="z-30 w-80 glass-card p-6 rounded-2xl border-white/10"
              >
                <div className="flex items-center gap-4 mb-6">
                  <div className="w-12 h-12 rounded-full bg-gradient-to-br from-primary-500 to-primary-700 flex items-center justify-center shadow-lg shadow-primary-500/30">
                    <FileText className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <div className="h-2 w-24 bg-white/20 rounded-full mb-2" />
                    <div className="h-1.5 w-16 bg-white/10 rounded-full" />
                  </div>
                </div>
                <div className="space-y-3 opacity-50">
                  <div className="h-1.5 w-full bg-white/20 rounded-full" />
                  <div className="h-1.5 w-5/6 bg-white/20 rounded-full" />
                  <div className="h-1.5 w-4/6 bg-white/20 rounded-full" />
                </div>
                {/* Scanning Line */}
                <motion.div
                  initial={{ top: "0%" }}
                  animate={{ top: "100%" }}
                  transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
                  className="absolute left-0 right-0 h-[2px] bg-gradient-to-r from-transparent via-primary-400 to-transparent shadow-[0_0_15px_rgba(96,165,250,0.8)]"
                />
              </FloatingCard>

              {/* Satellite Job Cards */}
              <SatelliteCard
                x={180} y={-80} z={-50} delay={0.5}
                icon="N" color="bg-emerald-500" score="98%" title="AI Engineer"
              />
              <SatelliteCard
                x={-160} y={60} z={-100} delay={0.8}
                icon="L" color="bg-purple-500" score="94%" title="Cloud Arch"
              />
              <SatelliteCard
                x={140} y={120} z={50} delay={1.1}
                icon="B" color="bg-orange-500" score="89%" title="Cyber Analyst"
              />

            </motion.div>
          </div>

        </div>
      </div>
    </div>
  );
}

function FloatingCard({ children, className, delay = 0 }: { children: React.ReactNode, className?: string, delay?: number }) {
  return (
    <motion.div
      initial={{ y: 20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ delay, duration: 0.8 }}
    >
      <motion.div
        animate={{ y: [-15, 15] }}
        transition={{ duration: 6, repeat: Infinity, repeatType: "mirror", ease: "easeInOut", delay: delay * 2 }}
        className={className}
      >
        {children}
      </motion.div>
    </motion.div>
  );
}

function SatelliteCard({ x, y, z, delay, icon, color, score, title }: any) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0 }}
      animate={{ opacity: 1, scale: 1, x, y, z }}
      transition={{ delay, duration: 0.8, type: "spring" }}
      className="absolute glass-card p-4 rounded-xl flex items-center gap-3 w-48 shadow-xl border-white/5"
    >
      <div className={`w-8 h-8 rounded-lg ${color} flex items-center justify-center text-white font-bold text-xs shadow-lg`}>
        {icon}
      </div>
      <div>
        <div className="text-sm font-semibold text-white">{title}</div>
        <div className="text-xs text-green-400 font-mono">{score} Match</div>
      </div>
    </motion.div>
  );
}
