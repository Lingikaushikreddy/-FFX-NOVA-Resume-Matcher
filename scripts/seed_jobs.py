import sys
import os
import json
import uuid
from datetime import datetime

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import get_db_session, init_db
from models.db_models import JobDB

SAMPLE_JOBS = [
    {
        "title": "Senior AI Engineer (TS/SCI)",
        "company": "Defense AI Systems",
        "location": "Arlington, VA",
        "raw_text": "We are seeking a Senior AI Engineer to lead the development of next-generation situational awareness systems. You will work with large language models, computer vision, and sensor fusion. Requires TS/SCI clearance. Experience with PyTorch, TensorFlow, and deploying models to edge devices is essential.",
        "required_skills": ["Python", "PyTorch", "Computer Vision", "TS/SCI Clearance", "Docker"],
        "preferred_skills": ["Kubernetes", "Ray", "C++", "Sensor Fusion"],
        "job_json": {
            "salary": "$160k - $210k",
            "clearance": "TS/SCI",
            "remote": False,
            "posted_date": datetime.now().isoformat()
        }
    },
    {
        "title": "Full Stack Developer - Mission Systems",
        "company": "Northrop Grumman",
        "location": "McLean, VA",
        "raw_text": "Join our Mission Systems team building critical command and control interfaces. You will build modern React frontends and robust Python backends. Secret clearance required. Must have experience with React, TypeScript, and FastAPI or Django.",
        "required_skills": ["React", "TypeScript", "Python", "FastAPI", "Secret Clearance"],
        "preferred_skills": ["PostgreSQL", "Redis", "AWS", "UI/UX Design"],
        "job_json": {
            "salary": "$130k - $170k",
            "clearance": "Secret",
            "remote": True,
            "posted_date": datetime.now().isoformat()
        }
    },
    {
        "title": "Cloud Architect (Secret)",
        "company": "AWS Federal",
        "location": "Herndon, VA",
        "raw_text": "Architect secure cloud solutions for federal agencies. Deep knowledge of AWS services, GovCloud, and security compliance (FedRAMP) is required. You will guide agencies in their cloud migration journey.",
        "required_skills": ["AWS", "Cloud Architecture", "Security", "FedRAMP", "Terraform"],
        "preferred_skills": ["Python", "Networking", "DevOps", "Secret Clearance"],
        "job_json": {
            "salary": "$150k - $200k",
            "clearance": "Secret",
            "remote": True,
            "posted_date": datetime.now().isoformat()
        }
    },
    {
        "title": "Cybersecurity Analyst",
        "company": "Booz Allen Hamilton",
        "location": "Washington, DC",
        "raw_text": "Analyze threats and vulnerabilities in critical infrastructure. Experience with SIEM tools, penetration testing, and incident response. Top Secret clearance is preferred.",
        "required_skills": ["Cybersecurity", "SIEM", "Incident Response", "Network Security"],
        "preferred_skills": ["Penetration Testing", "Python", "Top Secret Clearance", "CISSP"],
        "job_json": {
            "salary": "$110k - $150k",
            "clearance": "Top Secret",
            "remote": False,
            "posted_date": datetime.now().isoformat()
        }
    },
    {
        "title": "Data Scientist - Intelligence Community",
        "company": "Palantir Technologies",
        "location": "Palo Alto, CA (Remote Option)",
        "raw_text": "Work with massive datasets to uncover insights for national security. Strong background in statistics, machine learning, and data visualization. Experience with Spark, Hadoop, and SQL.",
        "required_skills": ["Data Science", "Machine Learning", "SQL", "Python", "Statistics"],
        "preferred_skills": ["Spark", "Hadoop", "Visualization", "TS/SCI Clearance"],
        "job_json": {
            "salary": "$170k - $240k",
            "clearance": "TS/SCI",
            "remote": True,
            "posted_date": datetime.now().isoformat()
        }
    }
]

def seed_jobs():
    print("Initializing database...")
    init_db()

    with get_db_session() as session:
        # Check count
        count = session.query(JobDB).count()
        if count > 0:
            print(f"Database already has {count} jobs. Skipping seed.")
            return

        print(f"Seeding {len(SAMPLE_JOBS)} sample jobs...")
        
        for job_data in SAMPLE_JOBS:
            job = JobDB(
                id=str(uuid.uuid4()),
                title=job_data["title"],
                company=job_data["company"],
                location=job_data["location"],
                raw_text=job_data["raw_text"],
                required_skills=job_data["required_skills"],
                preferred_skills=job_data["preferred_skills"],
                job_json=job_data["job_json"],
                embedding="[]",  # Placeholder if no embedding generated here
                is_active=True
            )
            session.add(job)
        
        print("Seeding complete!")

if __name__ == "__main__":
    seed_jobs()
