from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from resume_parser import parse_resume
from utils import open_json_file
from skill_matcher import match_skills
import sys
import subprocess

OUTPUT_JSON_FILE = "final_jobs_list.json"
MAX_PAGES = 1


app = FastAPI()

# Allow React frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change "*" to your React app URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload/")
async def upload_file(
    role: str = Form(...),
    location: str = Form(...),
    file: UploadFile = File(...)
):
    # Extracting skills from resume
    resume_skills = parse_resume(file)

    try:
        job_search_scripts = ["naukri_jobs_search.py", "microsoft_jobs_search.py"]
        for script_name in job_search_scripts:
            s_process = subprocess.run(
                [sys.executable, script_name, "--role", role, "--location", location, "--pages", str(MAX_PAGES), 
                    "--output", OUTPUT_JSON_FILE],
                timeout=60,
                capture_output=True,
                text=True
            )

            job_portal_name = script_name.replace("_jobs_search.py","")
            if s_process.returncode != 0:
                print(f"❌ {job_portal_name} Job Search failed!")
                print(s_process.stderr)
            else:
                print(f"✅ {job_portal_name} Subprocess completed successfully.")


    except Exception as e:
        print(f"⏱️ Something wrong while finding jobs. Exception: {e}")

    # getting jobs from json file
    jobs_list = open_json_file(OUTPUT_JSON_FILE)

    updated_jobs_list = []
    for job in jobs_list:
        matched_data = match_skills(resume_skills, job["description"])
        job.update(matched_data)
        
        # Removing Job Description as it is too large and not needed further
        del job["description"] 

        updated_jobs_list.append(job)
    
    return updated_jobs_list







    # # Mock: returning multiple dictionaries
    # response_data = [
    #     {
    #         "role": role,
    #         "location": location,
    #         "filename": file.filename,
    #         "size": len(resume_skills),
    #         "resume_skills": resume_skills
    #     },
    #     {
    #         "name": f"{role} - copy",
    #         "description": f"{location} (duplicate)",
    #         "filename": f"copy_{file.filename}",
    #         "size": len(resume_skills) // 2,
    #         "resume_skills": resume_skills
    #     }
    # ]

    # return response_data
