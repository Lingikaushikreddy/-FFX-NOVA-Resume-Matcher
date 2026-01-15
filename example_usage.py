#!/usr/bin/env python3
"""
Example usage script for FFX NOVA Resume Parser.

This script demonstrates how to use the resume parser module
to extract structured information from resume files.
"""

from resume_parser import ResumeParser, parse_resume_text


def example_parse_text():
    """Example: Parse resume from text string."""
    print("=" * 60)
    print("Example 1: Parsing resume from text")
    print("=" * 60)

    sample_resume = """
John Doe
john.doe@email.com
(555) 123-4567
San Francisco, CA
linkedin.com/in/johndoe

PROFESSIONAL SUMMARY

Experienced software engineer with 8+ years of experience in full-stack
development. Passionate about building scalable applications and leading
engineering teams.

EXPERIENCE

Senior Software Engineer
Tech Company Inc., San Francisco, CA
January 2020 - Present

• Led development of microservices architecture serving 10M+ users
• Implemented CI/CD pipelines using Jenkins and GitHub Actions
• Mentored team of 5 junior developers
• Technologies: Python, React, AWS, Docker, Kubernetes

Software Engineer
StartUp Corp, Mountain View, CA
June 2016 - December 2019

• Built RESTful APIs using Django and Flask
• Developed React frontend applications
• Managed PostgreSQL and MongoDB databases
• Collaborated with cross-functional teams in Agile environment

EDUCATION

Master of Science in Computer Science
Stanford University
May 2016
GPA: 3.9/4.0

Bachelor of Science in Computer Science
UC Berkeley
May 2014
Magna Cum Laude

SKILLS

Programming Languages: Python, JavaScript, TypeScript, Java, Go
Frameworks: React, Django, Flask, Node.js, Express
Databases: PostgreSQL, MongoDB, Redis, Elasticsearch
Cloud & DevOps: AWS, GCP, Docker, Kubernetes, Terraform
Tools: Git, Jenkins, Jira, Confluence

CERTIFICATIONS

AWS Certified Solutions Architect - Professional
Certified Kubernetes Administrator (CKA)
"""

    # Create parser instance
    parser = ResumeParser()

    # Parse the resume text
    resume = parser.parse_text(sample_resume)

    # Display results
    print("\n--- Contact Information ---")
    print(f"Name: {resume.contact.name}")
    print(f"Email: {resume.contact.email}")
    print(f"Phone: {resume.contact.phone}")
    print(f"Location: {resume.contact.location}")
    print(f"LinkedIn: {resume.contact.linkedin}")

    print("\n--- Skills ({} found) ---".format(len(resume.skills)))
    # Group skills by 5 per line for display
    for i in range(0, len(resume.skills), 5):
        print("  " + ", ".join(resume.skills[i:i+5]))

    print("\n--- Work Experience ({} entries) ---".format(len(resume.experience)))
    for exp in resume.experience:
        print(f"  • {exp.role or 'Unknown Role'}")
        if exp.company:
            print(f"    Company: {exp.company}")
        if exp.start_date or exp.end_date:
            date_str = f"{exp.start_date or '?'} - {exp.end_date or '?'}"
            print(f"    Dates: {date_str}")
        if exp.is_current:
            print("    (Current Position)")
        print()

    print("--- Education ({} entries) ---".format(len(resume.education)))
    for edu in resume.education:
        print(f"  • {edu.degree or 'Degree'}", end="")
        if edu.field_of_study:
            print(f" in {edu.field_of_study}", end="")
        print()
        if edu.institution:
            print(f"    Institution: {edu.institution}")
        if edu.graduation_date:
            print(f"    Graduated: {edu.graduation_date}")
        if edu.gpa:
            print(f"    GPA: {edu.gpa}")
        if edu.honors:
            print(f"    Honors: {edu.honors}")
        print()

    print("--- Sections Identified ---")
    for section_name in resume.sections.keys():
        print(f"  • {section_name}")

    print("\n--- Summary ---")
    summary = resume.get_summary()
    print(f"  Skills found: {summary['skills_count']}")
    print(f"  Experience entries: {summary['experience_count']}")
    print(f"  Education entries: {summary['education_count']}")

    return resume


def example_json_output():
    """Example: Get JSON output from parsed resume."""
    print("\n" + "=" * 60)
    print("Example 2: JSON Output")
    print("=" * 60)

    sample_text = """
Jane Smith
jane.smith@techcorp.com
(415) 987-6543
Seattle, WA

Skills: Python, Machine Learning, TensorFlow, PyTorch, Data Science

Experience:
Data Scientist, Tech Corp, 2021 - Present
- Built ML models for customer prediction

Education:
PhD in Computer Science, MIT, 2021
"""

    resume = parse_resume_text(sample_text)

    print("\nJSON Output (first 500 chars):")
    print("-" * 40)
    json_output = resume.to_json(indent=2)
    print(json_output[:500] + "..." if len(json_output) > 500 else json_output)


def example_custom_skills():
    """Example: Parser with custom skills."""
    print("\n" + "=" * 60)
    print("Example 3: Custom Skills Detection")
    print("=" * 60)

    sample_text = """
Alex Johnson
alex@company.com

Skills: Python, InternalFramework, ProprietaryTool, React

Experience at Custom Corp using our custom InternalFramework.
"""

    # Create parser with custom skills
    parser = ResumeParser(
        custom_skills=["InternalFramework", "ProprietaryTool"]
    )

    resume = parser.parse_text(sample_text)

    print("\nSkills detected (including custom):")
    for skill in resume.skills:
        print(f"  • {skill}")


def example_categorized_skills():
    """Example: Get skills by category."""
    print("\n" + "=" * 60)
    print("Example 4: Categorized Skills")
    print("=" * 60)

    sample_text = """
Full Stack Developer

Skills:
- Languages: Python, JavaScript, TypeScript, Java
- Frontend: React, Vue.js, Angular
- Backend: Django, Flask, Node.js
- Databases: PostgreSQL, MongoDB, Redis
- Cloud: AWS, GCP, Docker, Kubernetes
- Soft Skills: Leadership, Communication, Problem Solving
"""

    parser = ResumeParser()
    resume = parser.parse_text(sample_text)

    # Access skill extractor directly for categorized view
    categories = parser._skill_extractor.extract_by_category(sample_text)

    print("\nSkills by Category:")
    for category, skills in categories.items():
        print(f"\n  {category.replace('_', ' ').title()}:")
        for skill in skills[:5]:  # Show first 5
            print(f"    • {skill}")
        if len(skills) > 5:
            print(f"    ... and {len(skills) - 5} more")


def example_file_parsing():
    """Example: Parse from file (demonstration)."""
    print("\n" + "=" * 60)
    print("Example 5: File Parsing (demonstration)")
    print("=" * 60)

    print("""
To parse a resume file, use:

    from resume_parser import ResumeParser

    parser = ResumeParser()

    # Parse PDF
    resume = parser.parse("path/to/resume.pdf")

    # Parse DOCX
    resume = parser.parse("path/to/resume.docx")

    # Get structured data
    print(resume.to_json())

Supported file formats:
    • PDF (.pdf) - using PyPDF2
    • DOCX (.docx) - using python-docx
""")


def main():
    """Run all examples."""
    print("\n" + "#" * 60)
    print("# FFX NOVA Resume Parser - Example Usage")
    print("#" * 60)

    # Run examples
    example_parse_text()
    example_json_output()
    example_custom_skills()
    example_categorized_skills()
    example_file_parsing()

    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
