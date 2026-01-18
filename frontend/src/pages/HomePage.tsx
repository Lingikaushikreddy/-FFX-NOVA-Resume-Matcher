/**
 * Premium Home Page (Landing Page) - FFX NOVA
 * Stunning landing with hero, features, and CTAs
 */

import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { HeroSection } from '../components/HeroSection';
import { FileUploadZone } from '../components/FileUploadZone';
import { Footer } from '../components/layout/Footer';
import {
  Shield,
  BarChart3,
  Target,
  Zap,
  Award,
  ArrowRight,
  Building2,
  Briefcase,
  GraduationCap,
} from 'lucide-react';

interface HomePageProps {
  onMatchesComplete?: () => void;
}

const features = [
  {
    icon: Shield,
    title: 'Security Clearance Matching',
    description:
      'Automatically matches your clearance level with job requirements, from Public Trust to TS/SCI.',
    gradient: 'from-blue-500 to-indigo-500',
  },
  {
    icon: BarChart3,
    title: 'Skill Gap Analysis',
    description:
      'Identify missing skills and get personalized upskilling recommendations to boost your match score.',
    gradient: 'from-purple-500 to-pink-500',
  },
  {
    icon: Target,
    title: 'FFX-Score Algorithm',
    description:
      'Our proprietary scoring combines semantic matching, skills analysis, and experience to find your best fits.',
    gradient: 'from-orange-500 to-red-500',
  },
];

const stats = [
  { value: '10,000+', label: 'Jobs Matched', icon: Briefcase },
  { value: '95%', label: 'Match Accuracy', icon: Target },
  { value: '500+', label: 'Employers', icon: Building2 },
  { value: '24hrs', label: 'Avg Response', icon: Zap },
];

const testimonials = [
  {
    quote:
      "FFX NOVA helped me land my dream job at a defense contractor. The skill matching was incredibly accurate.",
    author: 'Sarah M.',
    role: 'Cloud Architect',
    company: 'Northrop Grumman',
  },
  {
    quote:
      "As a veteran transitioning to civilian work, this platform understood my skills better than any other.",
    author: 'James K.',
    role: 'DevOps Engineer',
    company: 'SAIC',
  },
  {
    quote:
      "The clearance-aware matching saved me hours of filtering through jobs I wasn't eligible for.",
    author: 'Maria L.',
    role: 'Cybersecurity Analyst',
    company: 'Leidos',
  },
];

export function HomePage({ onMatchesComplete }: HomePageProps) {
  return (
    <div className="min-h-screen bg-white dark:bg-slate-900 selection:bg-primary-100 selection:text-primary-900">
      <main>
        <HeroSection />

        {/* Upload Section */}
        <section className="py-20 bg-white dark:bg-slate-900 relative">
          <div className="container mx-auto px-4">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="text-center mb-12"
            >
              <span className="inline-block px-4 py-2 rounded-full bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-400 text-sm font-semibold mb-4">
                Get Started in Seconds
              </span>
              <h2 className="text-3xl md:text-4xl font-bold text-slate-900 dark:text-white mb-4">
                Start Your Journey
              </h2>
              <p className="text-lg text-slate-600 dark:text-slate-400 max-w-2xl mx-auto">
                Upload your resume to instantly match with Federal, Military, and Private sector
                jobs that fit your true potential.
              </p>
            </motion.div>

            <FileUploadZone onMatchesComplete={onMatchesComplete} />
          </div>
        </section>

        {/* Features Section */}
        <section className="py-20 bg-slate-50 dark:bg-slate-800/50 relative overflow-hidden">
          {/* Background Elements */}
          <div className="absolute inset-0 overflow-hidden">
            <div className="absolute -top-24 -right-24 w-96 h-96 bg-primary-500/5 rounded-full blur-3xl" />
            <div className="absolute -bottom-24 -left-24 w-96 h-96 bg-secondary-500/5 rounded-full blur-3xl" />
          </div>

          <div className="container mx-auto px-4 relative">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="text-center mb-16"
            >
              <span className="inline-block px-4 py-2 rounded-full bg-secondary-100 dark:bg-secondary-900/30 text-secondary-700 dark:text-secondary-400 text-sm font-semibold mb-4">
                Why Choose Us
              </span>
              <h2 className="text-3xl md:text-4xl font-bold text-slate-900 dark:text-white mb-4">
                Why FFX NOVA?
              </h2>
              <p className="text-lg text-slate-600 dark:text-slate-400 max-w-2xl mx-auto">
                Our AI-powered platform goes beyond keyword matching to find your perfect career
                fit.
              </p>
            </motion.div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
              {features.map((feature, index) => (
                <motion.div
                  key={feature.title}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.1 }}
                  whileHover={{ y: -8, transition: { duration: 0.2 } }}
                  className="group bg-white dark:bg-slate-900 p-8 rounded-3xl shadow-sm border border-slate-200 dark:border-slate-700 hover:shadow-xl transition-all duration-300"
                >
                  <div
                    className={`w-14 h-14 rounded-2xl bg-gradient-to-br ${feature.gradient} flex items-center justify-center mb-6 group-hover:scale-110 transition-transform`}
                  >
                    <feature.icon className="w-7 h-7 text-white" />
                  </div>
                  <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-3">
                    {feature.title}
                  </h3>
                  <p className="text-slate-600 dark:text-slate-400 leading-relaxed">
                    {feature.description}
                  </p>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* Stats Section */}
        <section className="py-16 bg-white dark:bg-slate-900">
          <div className="container mx-auto px-4">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8 max-w-4xl mx-auto">
              {stats.map((stat, index) => (
                <motion.div
                  key={stat.label}
                  initial={{ opacity: 0, scale: 0.8 }}
                  whileInView={{ opacity: 1, scale: 1 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.1 }}
                  className="text-center"
                >
                  <div className="w-12 h-12 mx-auto mb-4 rounded-xl bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center">
                    <stat.icon className="w-6 h-6 text-primary-600 dark:text-primary-400" />
                  </div>
                  <div className="text-3xl md:text-4xl font-bold text-slate-900 dark:text-white mb-1">
                    {stat.value}
                  </div>
                  <div className="text-sm text-slate-500 dark:text-slate-400 uppercase tracking-wide">
                    {stat.label}
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* How It Works */}
        <section className="py-20 bg-slate-50 dark:bg-slate-800/50">
          <div className="container mx-auto px-4">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="text-center mb-16"
            >
              <span className="inline-block px-4 py-2 rounded-full bg-accent-100 dark:bg-accent-900/30 text-accent-700 dark:text-accent-400 text-sm font-semibold mb-4">
                Simple Process
              </span>
              <h2 className="text-3xl md:text-4xl font-bold text-slate-900 dark:text-white mb-4">
                How It Works
              </h2>
            </motion.div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
              {[
                {
                  step: '01',
                  title: 'Upload Resume',
                  description: 'Drop your PDF or DOCX resume and our AI will extract your skills and experience.',
                  icon: GraduationCap,
                },
                {
                  step: '02',
                  title: 'AI Analysis',
                  description: 'Our algorithm analyzes your profile against thousands of federal and contractor jobs.',
                  icon: Zap,
                },
                {
                  step: '03',
                  title: 'Get Matches',
                  description: 'Receive personalized job recommendations ranked by your unique match score.',
                  icon: Target,
                },
              ].map((item, index) => (
                <motion.div
                  key={item.step}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.15 }}
                  className="relative"
                >
                  {index < 2 && (
                    <div className="hidden md:block absolute top-12 left-full w-full h-0.5 bg-gradient-to-r from-primary-500 to-transparent -translate-x-8" />
                  )}
                  <div className="bg-white dark:bg-slate-900 p-8 rounded-3xl border border-slate-200 dark:border-slate-700 relative">
                    <div className="absolute -top-4 -left-4 w-12 h-12 rounded-xl bg-gradient-to-br from-primary-500 to-secondary-500 flex items-center justify-center text-white font-bold shadow-lg">
                      {item.step}
                    </div>
                    <div className="pt-4">
                      <div className="w-12 h-12 rounded-xl bg-slate-100 dark:bg-slate-800 flex items-center justify-center mb-4">
                        <item.icon className="w-6 h-6 text-primary-600 dark:text-primary-400" />
                      </div>
                      <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-2">
                        {item.title}
                      </h3>
                      <p className="text-slate-600 dark:text-slate-400">{item.description}</p>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* Testimonials */}
        <section className="py-20 bg-white dark:bg-slate-900">
          <div className="container mx-auto px-4">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="text-center mb-16"
            >
              <span className="inline-block px-4 py-2 rounded-full bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400 text-sm font-semibold mb-4">
                Success Stories
              </span>
              <h2 className="text-3xl md:text-4xl font-bold text-slate-900 dark:text-white mb-4">
                Trusted by Professionals
              </h2>
            </motion.div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
              {testimonials.map((testimonial, index) => (
                <motion.div
                  key={testimonial.author}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.1 }}
                  className="bg-slate-50 dark:bg-slate-800 p-8 rounded-3xl"
                >
                  <div className="flex gap-1 mb-4">
                    {[...Array(5)].map((_, i) => (
                      <Award key={i} className="w-5 h-5 text-yellow-500 fill-yellow-500" />
                    ))}
                  </div>
                  <p className="text-slate-700 dark:text-slate-300 mb-6 italic">
                    "{testimonial.quote}"
                  </p>
                  <div>
                    <div className="font-bold text-slate-900 dark:text-white">
                      {testimonial.author}
                    </div>
                    <div className="text-sm text-slate-500 dark:text-slate-400">
                      {testimonial.role} at {testimonial.company}
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-20 bg-gradient-to-br from-primary-600 via-secondary-600 to-accent-600 relative overflow-hidden">
          {/* Background Elements */}
          <div className="absolute inset-0">
            <div className="absolute top-0 right-0 w-96 h-96 bg-white/10 rounded-full blur-3xl" />
            <div className="absolute bottom-0 left-0 w-64 h-64 bg-white/10 rounded-full blur-3xl" />
          </div>

          <div className="container mx-auto px-4 text-center relative">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
            >
              <h2 className="text-3xl md:text-5xl font-bold text-white mb-4">
                Ready to Find Your Perfect Match?
              </h2>
              <p className="text-xl text-white/80 max-w-2xl mx-auto mb-8">
                Join thousands of professionals who've found their dream careers through FFX NOVA.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
                  <Link
                    to="/register"
                    className="inline-flex items-center justify-center gap-2 px-8 py-4 text-lg font-semibold text-primary-600 bg-white rounded-2xl hover:bg-slate-100 transition-colors shadow-lg"
                  >
                    Get Started Free
                    <ArrowRight className="w-5 h-5" />
                  </Link>
                </motion.div>
                <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
                  <Link
                    to="/jobs"
                    className="inline-flex items-center justify-center px-8 py-4 text-lg font-semibold text-white border-2 border-white/50 rounded-2xl hover:bg-white/10 transition-colors"
                  >
                    Browse Jobs
                  </Link>
                </motion.div>
              </div>
            </motion.div>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
}
