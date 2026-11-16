# AI-Powered Resume Screening and Candidate Matching System

## Project Overview
A Python Flask application that screens multiple resumes against a job description and ranks candidates based on matching skills.

## Features
- Upload multiple resumes.
- Supports PDF and DOCX files.
- Extracts resume text.
- Identifies candidate skills.
- Calculates matching scores.
- Displays matched and missing skills.
- Ranks candidates by matching percentage.
- Supports new job descriptions for new analyses.

## Technologies Used
- Python
- Flask
- PyMuPDF
- python-docx
- HTML and CSS

## Project Structure
- app.py
- resume_parser.py
- skill_extractor.py
- job_matcher.py
- requirements.txt
- README.md

## Installation

Clone the repository:

    git clone https://github.com/Priti356/AI-Powered-Resume-Screening-Candidate-Matching-System.git

Move into the project folder:

    cd AI-Powered-Resume-Screening-Candidate-Matching-System

Install dependencies:

    pip install -r requirements.txt

## Run the Application

    python app.py

Open http://127.0.0.1:5000 in your browser.

## How It Works
1. Upload multiple PDF or DOCX resumes.
2. Enter a job description.
3. Submit the form.
4. The application extracts resume text.
5. It identifies and compares skills.
6. It calculates matching percentages.
7. It ranks candidates from highest to lowest score.

## Matching Score

Matching Score = (Matched Skills / Total Required Skills) * 100

## Limitations
- Skill extraction uses a predefined list of skills.
- Matching is based on skills, not a trained machine learning model.
- Scanned PDFs may require OCR.

## Future Improvements
- Expand the skill database.
- Add machine learning-based matching.
- Improve candidate reporting.

## Author
Priti Kumari
