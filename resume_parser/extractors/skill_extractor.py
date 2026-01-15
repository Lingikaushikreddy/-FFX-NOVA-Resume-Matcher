"""
Skill extraction module.

This module extracts technical and soft skills from resume text
using pattern matching against a comprehensive skills database.
"""

import re
from typing import Optional
import logging

logger = logging.getLogger(__name__)


# Comprehensive skill categories for pattern matching
TECHNICAL_SKILLS: dict[str, list[str]] = {
    "programming_languages": [
        "Python", "Java", "JavaScript", "TypeScript", "C", "C++", "C#",
        "Ruby", "Go", "Golang", "Rust", "Swift", "Kotlin", "Scala",
        "PHP", "Perl", "R", "MATLAB", "Julia", "Haskell", "Erlang",
        "Clojure", "F#", "Objective-C", "Dart", "Lua", "Groovy",
        "Shell", "Bash", "PowerShell", "VBA", "COBOL", "Fortran",
        "Assembly", "SQL", "PL/SQL", "T-SQL",
    ],
    "web_technologies": [
        "HTML", "HTML5", "CSS", "CSS3", "SASS", "SCSS", "LESS",
        "React", "React.js", "ReactJS", "Angular", "AngularJS", "Vue", "Vue.js",
        "Svelte", "Next.js", "NextJS", "Nuxt", "Nuxt.js", "Gatsby",
        "jQuery", "Bootstrap", "Tailwind", "Tailwind CSS", "Material UI",
        "Redux", "MobX", "Vuex", "GraphQL", "REST", "RESTful",
        "Node.js", "NodeJS", "Express", "Express.js", "Fastify",
        "Django", "Flask", "FastAPI", "Spring", "Spring Boot",
        "Ruby on Rails", "Rails", "Laravel", "ASP.NET", ".NET Core",
        "Webpack", "Vite", "Parcel", "Rollup", "Babel",
    ],
    "databases": [
        "MySQL", "PostgreSQL", "Postgres", "MongoDB", "SQLite", "Oracle",
        "SQL Server", "MSSQL", "MariaDB", "Redis", "Cassandra",
        "DynamoDB", "Elasticsearch", "CouchDB", "Neo4j", "Firebase",
        "Firestore", "Supabase", "PouchDB", "InfluxDB", "TimescaleDB",
    ],
    "cloud_platforms": [
        "AWS", "Amazon Web Services", "Azure", "Microsoft Azure",
        "GCP", "Google Cloud", "Google Cloud Platform",
        "Heroku", "DigitalOcean", "Linode", "Vercel", "Netlify",
        "Cloudflare", "IBM Cloud", "Oracle Cloud", "Alibaba Cloud",
    ],
    "devops_tools": [
        "Docker", "Kubernetes", "K8s", "Jenkins", "GitLab CI", "GitHub Actions",
        "CircleCI", "Travis CI", "Ansible", "Terraform", "Puppet", "Chef",
        "Vagrant", "Helm", "ArgoCD", "Prometheus", "Grafana", "Datadog",
        "New Relic", "Splunk", "ELK Stack", "Nginx", "Apache",
    ],
    "version_control": [
        "Git", "GitHub", "GitLab", "Bitbucket", "SVN", "Subversion",
        "Mercurial", "Perforce",
    ],
    "data_science": [
        "Pandas", "NumPy", "SciPy", "Scikit-learn", "TensorFlow",
        "PyTorch", "Keras", "OpenCV", "NLTK", "SpaCy",
        "Matplotlib", "Seaborn", "Plotly", "Tableau", "Power BI",
        "Jupyter", "Apache Spark", "Hadoop", "Airflow", "MLflow",
        "Hugging Face", "LangChain", "OpenAI", "GPT", "LLM",
    ],
    "mobile": [
        "iOS", "Android", "React Native", "Flutter", "Xamarin",
        "Ionic", "Cordova", "SwiftUI", "UIKit", "Jetpack Compose",
    ],
    "testing": [
        "Jest", "Mocha", "Chai", "Jasmine", "Cypress", "Selenium",
        "Playwright", "Puppeteer", "PyTest", "unittest", "JUnit",
        "TestNG", "RSpec", "Capybara", "Postman", "SoapUI",
    ],
    "other_technical": [
        "Linux", "Unix", "Windows Server", "macOS",
        "API", "APIs", "Microservices", "SOA", "WebSocket",
        "OAuth", "JWT", "SAML", "SSO", "LDAP",
        "Agile", "Scrum", "Kanban", "Jira", "Confluence",
        "Figma", "Sketch", "Adobe XD", "InVision",
    ],
}

SOFT_SKILLS: list[str] = [
    "Leadership", "Communication", "Teamwork", "Problem Solving",
    "Critical Thinking", "Time Management", "Project Management",
    "Analytical Skills", "Attention to Detail", "Adaptability",
    "Collaboration", "Creativity", "Decision Making", "Negotiation",
    "Presentation", "Public Speaking", "Conflict Resolution",
    "Strategic Planning", "Mentoring", "Coaching",
    "Customer Service", "Client Relations", "Stakeholder Management",
    "Cross-functional", "Self-motivated", "Results-oriented",
    "Detail-oriented", "Fast learner", "Multi-tasking",
]


class SkillExtractor:
    """
    Extract skills from resume text using pattern matching.

    Identifies technical skills (programming languages, frameworks, tools)
    and soft skills from resume content.

    Example:
        extractor = SkillExtractor()
        skills = extractor.extract("Experienced Python developer with React...")
    """

    def __init__(
        self,
        include_soft_skills: bool = True,
        custom_skills: Optional[list[str]] = None,
    ) -> None:
        """
        Initialize the skill extractor.

        Args:
            include_soft_skills: Whether to extract soft skills.
            custom_skills: Additional custom skills to look for.
        """
        self.include_soft_skills = include_soft_skills
        self.custom_skills = custom_skills or []

        # Build comprehensive skill list
        self._all_skills: set[str] = set()
        for category_skills in TECHNICAL_SKILLS.values():
            self._all_skills.update(category_skills)

        if include_soft_skills:
            self._all_skills.update(SOFT_SKILLS)

        self._all_skills.update(self.custom_skills)

        # Create pattern for each skill (case-insensitive, word boundary)
        self._skill_patterns: dict[str, re.Pattern] = {}
        for skill in self._all_skills:
            # Escape special regex characters
            escaped = re.escape(skill)
            # Create word boundary pattern
            pattern = rf"\b{escaped}\b"
            self._skill_patterns[skill] = re.compile(pattern, re.IGNORECASE)

    def extract(
        self,
        text: str,
        skills_section: Optional[str] = None,
    ) -> list[str]:
        """
        Extract skills from resume text.

        Args:
            text: Full resume text.
            skills_section: Optional skills section content for priority.

        Returns:
            List of unique skills found, sorted alphabetically.
        """
        found_skills: set[str] = set()

        # Search in skills section first if available
        search_text = skills_section if skills_section else text

        # Also search full text to catch skills mentioned elsewhere
        all_text = f"{search_text}\n{text}" if skills_section else text

        for skill, pattern in self._skill_patterns.items():
            if pattern.search(all_text):
                # Use the canonical form of the skill
                found_skills.add(skill)

        return sorted(list(found_skills))

    def extract_by_category(
        self,
        text: str,
        skills_section: Optional[str] = None,
    ) -> dict[str, list[str]]:
        """
        Extract skills organized by category.

        Args:
            text: Full resume text.
            skills_section: Optional skills section content.

        Returns:
            Dictionary mapping category names to lists of skills.
        """
        all_text = f"{skills_section}\n{text}" if skills_section else text

        categorized: dict[str, list[str]] = {}

        # Search technical skill categories
        for category, skills in TECHNICAL_SKILLS.items():
            found = []
            for skill in skills:
                pattern = self._skill_patterns.get(skill)
                if pattern and pattern.search(all_text):
                    found.append(skill)
            if found:
                categorized[category] = sorted(found)

        # Search soft skills
        if self.include_soft_skills:
            soft_found = []
            for skill in SOFT_SKILLS:
                pattern = self._skill_patterns.get(skill)
                if pattern and pattern.search(all_text):
                    soft_found.append(skill)
            if soft_found:
                categorized["soft_skills"] = sorted(soft_found)

        # Search custom skills
        if self.custom_skills:
            custom_found = []
            for skill in self.custom_skills:
                pattern = self._skill_patterns.get(skill)
                if pattern and pattern.search(all_text):
                    custom_found.append(skill)
            if custom_found:
                categorized["custom"] = sorted(custom_found)

        return categorized

    def extract_from_skills_line(self, line: str) -> list[str]:
        """
        Extract skills from a single line (like a comma-separated skills list).

        Args:
            line: Line of text containing skills.

        Returns:
            List of skills found.
        """
        found_skills: set[str] = set()

        # Try to split by common delimiters
        delimiters = [",", ";", "|", "•", "·", "●", "/"]
        items = [line]

        for delimiter in delimiters:
            new_items = []
            for item in items:
                new_items.extend(item.split(delimiter))
            items = new_items

        # Check each item against known skills
        for item in items:
            item = item.strip()
            for skill, pattern in self._skill_patterns.items():
                if pattern.fullmatch(item):
                    found_skills.add(skill)

        return sorted(list(found_skills))

    def get_skill_categories(self) -> list[str]:
        """
        Get list of all skill category names.

        Returns:
            List of category names.
        """
        categories = list(TECHNICAL_SKILLS.keys())
        if self.include_soft_skills:
            categories.append("soft_skills")
        if self.custom_skills:
            categories.append("custom")
        return categories

    def add_skill(self, skill: str, category: Optional[str] = None) -> None:
        """
        Add a custom skill to the extractor.

        Args:
            skill: Skill name to add.
            category: Optional category to add it to.
        """
        self._all_skills.add(skill)
        self.custom_skills.append(skill)

        escaped = re.escape(skill)
        pattern = rf"\b{escaped}\b"
        self._skill_patterns[skill] = re.compile(pattern, re.IGNORECASE)
