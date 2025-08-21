from resume_parser import extract_skills

# import utils or resume parser here and extract resume skills here itself

# instead of resume skills directly get resume 
def match_skills(resume_skills, job_description_text):

    job_skills = extract_skills(job_description_text)

    matched_skills = resume_skills & job_skills
    missing_skills = job_skills - resume_skills
    match_percentage = round(len(matched_skills) / len(job_skills) * 100, 2) if job_skills else 0
    
    return {
        "matched_skills": sorted(matched_skills),
        "missing_skills": sorted(missing_skills),
        "match_percentage": match_percentage
    }