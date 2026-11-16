
from flask import Flask, request, render_template_string
from werkzeug.utils import secure_filename
from pathlib import Path
from tempfile import TemporaryDirectory

from resume_parser import extract_resume_text, ResumeExtractionError
from skill_extractor import extract_skills
from job_matcher import match_resume_to_job

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

ALLOWED_EXTENSIONS = {"pdf", "docx"}

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Resume Screening System</title>
    <style>
        body {
            font-family: Arial;
            background: #f1f5f9;
            padding: 30px;
        }
        .container {
            background: white;
            padding: 30px;
            max-width: 750px;
            margin: auto;
            border-radius: 12px;
        }
        textarea {
            width: 100%;
            height: 150px;
            padding: 10px;
            box-sizing: border-box;
        }
        button {
            background: #2563eb;
            color: white;
            padding: 12px 25px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
        }
        pre {
            white-space: pre-wrap;
            overflow-wrap: anywhere;
            background: #f1f5f9;
            padding: 15px;
        }
        .error { color: red; }
    </style>
</head>
<body>
<div class="container">

    <h1>AI-Powered Resume Screening</h1>
    <p>Upload your resume and compare it with a job description.</p>

    <form method="POST" enctype="multipart/form-data">

        <h3>Upload Multiple Resumes</h3>
        <input type="file" name="resumes"
               accept=".pdf,.docx" multiple required>
        <p>You can select multiple PDF or DOCX resumes.</p>

        <h3>Enter Job Description for New Analysis</h3>
        <textarea name="job_description"
                  placeholder="Enter a new job description..."
                  required></textarea>

        <br><br>
        <button type="submit">Analyze Resume</button>

    </form>

    {% if error %}
        <p class="error">{{ error }}</p>
    {% endif %}


    {% if errors %}
        <hr>
        <h3>Upload Errors</h3>
        {% for error in errors %}
            <p class="error">{{ error }}</p>
        {% endfor %}
    {% endif %}

    {% if results %}
        <hr>
        <h2>Previous Analysis</h2>

        <h3>Job Description Used:</h3>
        <p>{{ job_description }}</p>

        <h2>Candidate Rankings</h2>

        <table border="1" cellpadding="10" cellspacing="0" width="100%">
            <tr>
                <th>Rank</th>
                <th>Candidate Resume</th>
                <th>Matching Score</th>
                <th>Matched Skills</th>
                <th>Missing Skills</th>
            </tr>

            {% for candidate in results %}
            <tr>
                <td>{{ loop.index }}</td>
                <td>{{ candidate.filename }}</td>
                <td>{{ candidate.match_score }}%</td>
                <td>{{ candidate.matched_skills|join(', ') }}</td>
                <td>{{ candidate.missing_skills|join(', ') }}</td>
            </tr>
            {% endfor %}
        </table>

    {% endif %}


</div>
</body>
</html>
"""



@app.route("/", methods=["GET", "POST"])
def home():

    results = []
    errors = []
    job_description = ""

    if request.method == "POST":

        uploaded_files = request.files.getlist("resumes")
        job_description = request.form.get(
            "job_description", ""
        ).strip()

        if not uploaded_files or not any(f.filename for f in uploaded_files):
            errors.append("Please upload at least one resume.")

        elif not job_description:
            errors.append("Please enter a job description.")

        else:
            with TemporaryDirectory() as temp_dir:

                for uploaded_file in uploaded_files:

                    if not uploaded_file.filename:
                        continue

                    filename = secure_filename(uploaded_file.filename)
                    extension = Path(filename).suffix.lower().lstrip(".")

                    if extension not in ALLOWED_EXTENSIONS:
                        errors.append(f"{filename}: Only PDF and DOCX files are allowed.")
                        continue

                    try:
                        file_path = Path(temp_dir) / f"{len(results)}_{filename}"
                        uploaded_file.save(file_path)

                        resume_text = extract_resume_text(file_path)

                        if not resume_text.strip():
                            errors.append(f"{filename}: No readable text found.")
                            continue

                        result = match_resume_to_job(
                            resume_text,
                            job_description
                        )

                        results.append({
                            "filename": filename,
                            "match_score": result["match_score"],
                            "matched_skills": result["matched_skills"],
                            "missing_skills": result["missing_skills"],
                            "skills": extract_skills(resume_text)
                        })

                    except (ResumeExtractionError, ValueError, OSError) as exc:
                        errors.append(f"{filename}: {exc}")

            results.sort(
                key=lambda candidate: candidate["match_score"],
                reverse=True
            )

    return render_template_string(
        HTML,
        results=results,
        errors=errors,
        job_description=job_description,
        result=None,
        skills=[],
        resume_text=None,
        error=None
    )


@app.errorhandler(413)
def file_too_large(error):
    return "File too large. Maximum size is 5 MB.", 413


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
