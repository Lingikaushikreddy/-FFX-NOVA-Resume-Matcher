"""
Skill synonym dictionary and normalization.

Handles variations in how technical skills are written,
enabling accurate matching between resumes and job descriptions.
"""

from typing import Dict, Set, Optional


# Comprehensive skill synonym mapping
# Key is the canonical (normalized) form, values are alternative forms
SKILL_SYNONYMS: Dict[str, Set[str]] = {
    # Programming Languages
    "javascript": {"js", "ecmascript", "es6", "es2015", "es2020", "vanilla js"},
    "typescript": {"ts"},
    "python": {"python3", "python2", "py", "cpython"},
    "java": {"java8", "java11", "java17", "jdk", "j2ee", "jee"},
    "c#": {"csharp", "c sharp", ".net c#"},
    "c++": {"cpp", "c plus plus", "cplusplus"},
    "c": {"ansi c", "c language"},
    "go": {"golang"},
    "rust": {"rustlang"},
    "ruby": {"ruby on rails", "ror"},
    "php": {"php7", "php8"},
    "swift": {"swift ui", "swiftui"},
    "kotlin": {"kotlin/jvm"},
    "scala": {"scala lang"},
    "r": {"r language", "r programming", "rstats"},
    "matlab": {"mathlab"},
    "perl": {"perl5"},
    "shell": {"bash", "sh", "zsh", "shell scripting", "bash scripting"},
    "powershell": {"ps", "posh", "windows powershell"},
    "sql": {"structured query language", "sql queries"},

    # Frontend Frameworks
    "react": {"reactjs", "react.js", "react js"},
    "angular": {"angularjs", "angular.js", "angular 2+", "ng"},
    "vue": {"vuejs", "vue.js", "vue3"},
    "svelte": {"sveltejs", "svelte.js"},
    "next.js": {"nextjs", "next"},
    "nuxt": {"nuxtjs", "nuxt.js"},
    "jquery": {"jquery.js"},
    "bootstrap": {"twitter bootstrap", "bootstrap css"},
    "tailwind": {"tailwindcss", "tailwind css"},

    # Backend Frameworks
    "node.js": {"nodejs", "node", "express.js", "expressjs"},
    "django": {"django python", "django rest framework", "drf"},
    "flask": {"flask python"},
    "fastapi": {"fast api", "fastapi python"},
    "spring": {"spring boot", "spring framework", "springboot"},
    "rails": {"ruby on rails", "ror"},
    "laravel": {"laravel php"},
    "asp.net": {"aspnet", "asp net", ".net core", "dotnet"},

    # Databases
    "postgresql": {"postgres", "psql", "pg"},
    "mysql": {"mariadb", "maria db"},
    "mongodb": {"mongo", "mongo db"},
    "redis": {"redis cache"},
    "elasticsearch": {"elastic", "es", "elk"},
    "dynamodb": {"dynamo db", "aws dynamodb"},
    "cassandra": {"apache cassandra"},
    "sqlite": {"sqlite3"},
    "oracle": {"oracle db", "oracle database", "plsql", "pl/sql"},
    "sql server": {"mssql", "microsoft sql server", "ms sql"},

    # Cloud Platforms
    "aws": {"amazon web services", "amazon aws"},
    "azure": {"microsoft azure", "azure cloud"},
    "gcp": {"google cloud", "google cloud platform"},
    "heroku": {"heroku cloud"},
    "digitalocean": {"digital ocean"},
    "cloudflare": {"cloudflare workers"},

    # DevOps & Infrastructure
    "docker": {"containerization", "docker compose", "docker-compose"},
    "kubernetes": {"k8s", "kube", "k8", "kubectl"},
    "terraform": {"terraform iac", "tf"},
    "ansible": {"ansible automation"},
    "jenkins": {"jenkins ci", "jenkins pipeline"},
    "gitlab ci": {"gitlab-ci", "gitlab ci/cd"},
    "github actions": {"gh actions", "github workflows"},
    "circleci": {"circle ci"},
    "nginx": {"nginx server"},
    "apache": {"apache http", "httpd"},
    "linux": {"unix", "linux administration", "rhel", "centos", "ubuntu"},

    # Data & ML
    "machine learning": {"ml", "statistical learning"},
    "deep learning": {"dl", "neural networks", "nn"},
    "tensorflow": {"tf", "tensorflow 2"},
    "pytorch": {"torch"},
    "scikit-learn": {"sklearn", "scikit learn"},
    "pandas": {"pandas python"},
    "numpy": {"np", "numpy python"},
    "spark": {"apache spark", "pyspark"},
    "hadoop": {"apache hadoop", "hdfs"},
    "kafka": {"apache kafka"},

    # APIs & Protocols
    "rest": {"restful", "rest api", "restful api"},
    "graphql": {"graph ql", "gql"},
    "grpc": {"g rpc"},
    "soap": {"soap api"},
    "websocket": {"websockets", "ws"},

    # Testing
    "jest": {"jestjs"},
    "pytest": {"py.test", "python testing"},
    "junit": {"junit5"},
    "selenium": {"selenium webdriver"},
    "cypress": {"cypress.io"},
    "mocha": {"mochajs"},

    # Version Control
    "git": {"github", "gitlab", "bitbucket", "version control"},
    "svn": {"subversion"},

    # Project Management
    "agile": {"scrum", "kanban", "agile methodology"},
    "jira": {"atlassian jira"},
    "confluence": {"atlassian confluence"},

    # Security
    "cybersecurity": {"cyber security", "infosec", "information security"},
    "penetration testing": {"pen testing", "pentest", "ethical hacking"},
    "oauth": {"oauth2", "oauth 2.0"},
    "jwt": {"json web token", "json web tokens"},

    # Other
    "microservices": {"micro services", "microservice architecture"},
    "ci/cd": {"cicd", "ci cd", "continuous integration", "continuous deployment"},
    "api": {"apis", "api development"},
}

# Build reverse lookup for efficiency
_REVERSE_LOOKUP: Dict[str, str] = {}
for canonical, synonyms in SKILL_SYNONYMS.items():
    _REVERSE_LOOKUP[canonical.lower()] = canonical
    for syn in synonyms:
        _REVERSE_LOOKUP[syn.lower()] = canonical


def normalize_skill(skill: str) -> str:
    """
    Normalize a skill to its canonical form.

    Args:
        skill: Skill name to normalize.

    Returns:
        Canonical (normalized) skill name.

    Example:
        >>> normalize_skill("ReactJS")
        "react"
        >>> normalize_skill("K8s")
        "kubernetes"
    """
    if not skill:
        return ""

    skill_lower = skill.lower().strip()

    # Check if it's a synonym
    if skill_lower in _REVERSE_LOOKUP:
        return _REVERSE_LOOKUP[skill_lower]

    # Return as-is (lowercased) if not in synonym map
    return skill_lower


def get_canonical_skill(skill: str) -> str:
    """
    Get the canonical/display form of a skill.

    Returns the proper-cased canonical form if known,
    otherwise returns the original skill.

    Args:
        skill: Skill name.

    Returns:
        Canonical display form.

    Example:
        >>> get_canonical_skill("js")
        "JavaScript"
    """
    normalized = normalize_skill(skill)

    # Map to proper display names
    display_names = {
        "javascript": "JavaScript",
        "typescript": "TypeScript",
        "python": "Python",
        "java": "Java",
        "c#": "C#",
        "c++": "C++",
        "go": "Go",
        "rust": "Rust",
        "ruby": "Ruby",
        "php": "PHP",
        "swift": "Swift",
        "kotlin": "Kotlin",
        "react": "React",
        "angular": "Angular",
        "vue": "Vue.js",
        "node.js": "Node.js",
        "django": "Django",
        "flask": "Flask",
        "fastapi": "FastAPI",
        "spring": "Spring",
        "postgresql": "PostgreSQL",
        "mysql": "MySQL",
        "mongodb": "MongoDB",
        "redis": "Redis",
        "elasticsearch": "Elasticsearch",
        "aws": "AWS",
        "azure": "Azure",
        "gcp": "GCP",
        "docker": "Docker",
        "kubernetes": "Kubernetes",
        "terraform": "Terraform",
        "ansible": "Ansible",
        "jenkins": "Jenkins",
        "linux": "Linux",
        "git": "Git",
        "machine learning": "Machine Learning",
        "deep learning": "Deep Learning",
        "tensorflow": "TensorFlow",
        "pytorch": "PyTorch",
        "scikit-learn": "scikit-learn",
        "pandas": "Pandas",
        "numpy": "NumPy",
        "rest": "REST API",
        "graphql": "GraphQL",
        "sql": "SQL",
        "agile": "Agile",
        "ci/cd": "CI/CD",
        "microservices": "Microservices",
    }

    return display_names.get(normalized, skill)


def skills_match(skill1: str, skill2: str) -> bool:
    """
    Check if two skills match (including synonyms).

    Args:
        skill1: First skill name.
        skill2: Second skill name.

    Returns:
        True if skills match or are synonyms.

    Example:
        >>> skills_match("JavaScript", "JS")
        True
        >>> skills_match("Python", "Java")
        False
    """
    if not skill1 or not skill2:
        return False

    return normalize_skill(skill1) == normalize_skill(skill2)


def find_matching_skills(
    resume_skills: list[str],
    job_skills: list[str],
) -> tuple[list[str], list[str]]:
    """
    Find matching and missing skills between resume and job.

    Uses synonym matching for accurate comparison.

    Args:
        resume_skills: Skills from resume.
        job_skills: Skills from job posting.

    Returns:
        Tuple of (matched_skills, missing_skills).
    """
    resume_normalized = {normalize_skill(s) for s in resume_skills}

    matched = []
    missing = []

    for skill in job_skills:
        skill_normalized = normalize_skill(skill)
        if skill_normalized in resume_normalized:
            matched.append(get_canonical_skill(skill))
        else:
            missing.append(get_canonical_skill(skill))

    return matched, missing


def get_all_synonyms(skill: str) -> set[str]:
    """
    Get all synonyms for a skill.

    Args:
        skill: Skill name.

    Returns:
        Set of all synonyms including the canonical form.
    """
    normalized = normalize_skill(skill)

    if normalized in SKILL_SYNONYMS:
        return SKILL_SYNONYMS[normalized] | {normalized}

    return {skill.lower()}
