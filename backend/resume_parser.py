import re
import docx2txt
import PyPDF2
from skill_set import MASTER_SKILLS

def normalize(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9+/#&.\- ]", " ", text)
    return text

def extract_skills(text):
    text = normalize(text)
    found = set()
    for skill in MASTER_SKILLS:
        if re.search(rf"\b{re.escape(skill.lower())}\b", text):
            found.add(skill)
    return found

def extract_text_from_resume(uploaded_file):
    text = ""
    if uploaded_file.filename.endswith(".pdf"):
        reader = PyPDF2.PdfReader(uploaded_file.file)
        text = " ".join(page.extract_text() for page in reader.pages if page.extract_text())
    elif uploaded_file.filename.endswith(".docx"):
        text = docx2txt.process(uploaded_file.file)
    
    return text

def parse_resume(uploaded_file):
    text = extract_text_from_resume(uploaded_file)
    return extract_skills(text)