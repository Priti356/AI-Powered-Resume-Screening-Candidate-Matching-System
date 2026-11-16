
from skill_extractor import extract_skills

def match_resume_to_job(resume_text, job_description):

    resume_skills = extract_skills(resume_text)
    required_skills = extract_skills(job_description)

    matched_skills = [
        skill for skill in required_skills
        if skill in resume_skills
    ]

    missing_skills = [
        skill for skill in required_skills
        if skill not in resume_skills
    ]

    if len(required_skills) == 0:
        match_score = 0
    else:
        match_score = (
            len(matched_skills) / len(required_skills)
        ) * 100

    return {
        "match_score": round(match_score, 2),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }
