SKILLS = [
    "python",
    "django",
    "django rest framework",
    "rest api",
    "javascript",
    "html",
    "css",
    "react",
    "mysql",
    "sqlite",
    "postgresql",
    "git",
    "github",
    "docker",
    "aws",
    "fastapi",
    "flask",
    "sql",
]

def extract_skills(text):
    text=text.lower()

    found_skills=[]

    for skill in SKILLS:
        if skill in text:
            found_skills.append(skill)

    return found_skills

def calculate_match(resume_text,job_text):
    resume_skills=extract_skills(resume_text)
    job_skills=extract_skills(job_text)

    matched_skills = []

    # Check JOB requirements against resume
    for skill in job_skills:
        if skill in resume_skills:
            matched_skills.append(skill)

    missing_skills = []

    # Find JOB requirements missing from resume
    for skill in job_skills:
        if skill not in resume_skills:
            missing_skills.append(skill)


    if len(job_skills)==0:
        match_score=0
    else:
        match_score=(len(matched_skills)/len(job_skills))*100

    return {
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "match_score": round(match_score, 2),
    }
