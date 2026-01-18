import { motion } from 'framer-motion';
import { JobMatchCard } from './JobMatchCard';

export function JobMatchGrid() {
    const dummyJobs = [
        {
            id: '1',
            title: 'Senior AI Engineer',
            company: 'Defense Systems',
            location: 'Arlington, VA',
            salary: '$160k - $210k',
            matchScore: 98,
            semanticScore: 95,
            skillScore: 99,
            experienceScore: 90,
            clearance: 'TS/SCI' as const,
            matchedSkills: ['Python', 'PyTorch', 'Computer Vision'],
            missingSkills: [],
            isRemote: false
        },
        {
            id: '2',
            title: 'Cloud Architect',
            company: 'AWS Federal',
            location: 'Herndon, VA',
            salary: '$150k - $200k',
            matchScore: 94,
            semanticScore: 92,
            skillScore: 95,
            experienceScore: 94,
            clearance: 'Secret' as const,
            matchedSkills: ['AWS', 'Terraform', 'Security'],
            missingSkills: ['Kubernetes'],
            isRemote: true
        },
        {
            id: '3',
            title: 'Cyber Analyst',
            company: 'Booz Allen Hamilton',
            location: 'Washington, DC',
            salary: '$110k - $150k',
            matchScore: 89,
            semanticScore: 88,
            skillScore: 90,
            experienceScore: 85,
            clearance: 'Top Secret' as const,
            matchedSkills: ['SIEM', 'Network Security'],
            missingSkills: ['Penetration Testing'],
            isRemote: false
        }
    ];

    return (
        <div className="py-24 relative z-10">
            <div className="text-center mb-16">
                <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
                    Live <span className="text-gradient-primary">Opportunities</span>
                </h2>
                <p className="text-slate-400 max-w-2xl mx-auto">
                    See who's hiring right now in the NOVA defense and tech corridor.
                </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {dummyJobs.map((job, index) => (
                    <motion.div
                        key={job.id}
                        initial={{ opacity: 0, y: 30 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        transition={{ delay: index * 0.1, duration: 0.6 }}
                    >
                        <div className="h-full glass-card rounded-2xl hover:border-primary-500/30 transition-colors p-1">
                            <JobMatchCard job={job} />
                        </div>
                    </motion.div>
                ))}
            </div>
        </div>
    );
}
