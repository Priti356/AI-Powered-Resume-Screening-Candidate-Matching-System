
import re

SKILLS = [
    "Python",
    "Java",
    "C++",
    "SQL",
    "Machine Learning",
    "Deep Learning",
    "Flask",
    "Django",
    "Pandas",
    "NumPy",
    "Scikit-learn",
    "TensorFlow",
    "HTML",
    "CSS",
    "JavaScript",
    "Data Analysis",
    "Power BI",
    "Excel"
]

def extract_skills(resume_text):

    found_skills = []

    text = resume_text.lower()

    for skill in SKILLS:
        pattern = r"(?<!\w)" + re.escape(skill.lower()) + r"(?!\w)"

        if re.search(pattern, text):
            found_skills.append(skill)

    return found_skills
