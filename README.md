# Fit4JobRole-FastAPI
Find your best-fit job roles by analyzing resumes and matching skills — built with FastAPI and React.

**Fit4JobRole** is a smart, resume-based job finder that helps users match their resume skills with real-time job descriptions from sources like Microsoft Careers, Naukri.com, and other platforms.  

It helps job seekers **discover roles they’re qualified for** and **highlights missing skills** for other roles — now with a modern **React + FastAPI web application**.

---

## Features
- Upload your resume (PDF/DOCX)  
- Automatic skill extraction from resume  
- Fetches job listings based on role & location  
- Matches your skills with job descriptions  
- Displays matching percentage & missing skills    

---

## Tech Stack
- **Frontend**: React + TailwindCSS  
- **Backend**: FastAPI (Python)  
- **Job Sources**: Microsoft Careers, Naukri.com  
- **Data Processing**: Pandas, PyPDF2, python-docx   

---

## Why This Project?
Most job seekers apply blindly to jobs. This tool helps:  
- Find roles you actually qualify for  
- Discover what skills you’re missing  
- Boost chances of selection by applying more smartly  

---

## How to Run the App

### 1. Clone the repository
```bash
git clone https://github.com/KSP-2000/Fit4JobRole-FastAPI.git
cd Fit4JobRole-FastAPI

```

### 2. Create and activate virtual environment
```
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3. Backend setup (FastAPI + Playwright)
```
cd backend
pip install -r requirements.txt
pip install playwright
install playwright
uvicorn main:app --reload
```

### 4. Frontend setup (React + Tailwind CSS)
```

# Create React App using CRA
npx create-react-app frontend
cd frontend


# Install dependencies
npm install


# Install Tailwind CSS
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p


# Configure Tailwind in tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}


# Update src/index.css with Tailwind directives
@tailwind base;
@tailwind components;
@tailwind utilities;


# Ensure index.js imports index.css
import './index.css';


# Run the frontend
npm start


```

## Limitations & Future Work
- Current matching logic is keyword-based, not deep NLP
- Scoring logic can be improved using AI/LLMs
- More job sources can be added for broader coverage

## Made by
Kelothu Shivaprasad
Aspiring Software Developer

## ⚠️ Disclaimer
This project is intended for educational and personal use only.
Please ensure compliance with the terms of service of any external websites or platforms you interact with.
The author is not responsible for misuse or legal issues arising from improper use of this project.


