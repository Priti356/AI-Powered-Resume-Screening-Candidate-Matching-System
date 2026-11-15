
from flask import Flask, request, render_template_string
from werkzeug.utils import secure_filename
from pathlib import Path
from tempfile import TemporaryDirectory

from resume_parser import (
    extract_resume_text,
    ResumeExtractionError
)

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
            padding: 40px;
            text-align: center;
        }
        .container {
            background: white;
            padding: 30px;
            max-width: 700px;
            margin: auto;
            border-radius: 12px;
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
            text-align: left;
            white-space: pre-wrap;
            overflow-wrap: anywhere;
            background: #f8fafc;
            padding: 15px;
        }
        .error { color: red; }
    </style>
</head>
<body>
    <div class="container">
        <h1>AI-Powered Resume Screening</h1>
        <p>Upload your PDF or DOCX resume.</p>

        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="resume"
                   accept=".pdf,.docx" required>
            <br><br>
            <button type="submit">Analyze Resume</button>
        </form>

        {% if error %}
            <p class="error">{{ error }}</p>
        {% endif %}

        {% if resume_text %}
            <h2>Extracted Resume Text</h2>
            <pre>{{ resume_text }}</pre>
        {% endif %}
    </div>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():
    resume_text = None
    error = None

    if request.method == "POST":
        uploaded_file = request.files.get("resume")

        if not uploaded_file or not uploaded_file.filename:
            error = "Please select a resume."
        else:
            filename = secure_filename(uploaded_file.filename)
            extension = Path(filename).suffix.lower().lstrip(".")

            if extension not in ALLOWED_EXTENSIONS:
                error = "Only PDF and DOCX files are allowed."
            else:
                try:
                    with TemporaryDirectory() as temp_dir:
                        file_path = Path(temp_dir) / filename
                        uploaded_file.save(file_path)

                        resume_text = extract_resume_text(file_path)

                    if not resume_text.strip():
                        error = (
                            "No text found. The PDF may be scanned "
                            "or the document may be empty."
                        )
                        resume_text = None

                except (ResumeExtractionError, ValueError,
                        OSError) as exc:
                    error = str(exc)

    return render_template_string(
        HTML,
        resume_text=resume_text,
        error=error
    )


@app.errorhandler(413)
def file_too_large(error):
    return "File too large. Maximum size is 5 MB.", 413


if __name__ == "__main__":
    app.run(debug=False)
