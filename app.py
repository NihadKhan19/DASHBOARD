"""
Aspiring Data Analyst — Portfolio (Flask app)

Everything you're likely to want to edit lives in the CONFIG section
below: your name, bio, skills, projects, experience, and blog posts.
The templates just render this data — you shouldn't need to touch
HTML for basic content changes.

Run locally:
    pip install flask
    python app.py
Then open http://127.0.0.1:5000
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import json
import os

app = Flask(__name__)
app.secret_key = "change-this-to-a-random-secret-in-production"

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
MESSAGES_FILE = os.path.join(DATA_DIR, "messages.json")

# ---------------------------------------------------------------------------
# CONFIG — edit everything below to make this your own
# ---------------------------------------------------------------------------

PROFILE = {
    "name": "Nihad Khan",
    "title": "Aspiring Data Analyst",
    "tagline": "Turning raw rows into decisions worth making.",
    "location": "Delhi, India",
    "email": "you@example.com",
    "linkedin": "https://linkedin.com/in/yourname",
    "github": "https://github.com/yourname",
    "resume_url": "/static/resume.pdf",  # drop your real resume.pdf into static/
    "about": (
        "I'm a data analyst in training — the kind of person who can't look at a "
        "messy spreadsheet without wanting to clean it up. My background is in "
        "[your degree/field], and over the last year I've been building hands-on "
        "skill with SQL, Python, and visualization tools by working through real "
        "datasets instead of just tutorials. I like problems that start with "
        "'why did this number move' and end with a chart someone actually acts on."
    ),
    "formula_words": ["Curiosity", "Rigor", "Clarity", "Impact"],
}

SKILLS = [
    {"name": "SQL", "level": 80, "group": "Core"},
    {"name": "Excel / Sheets", "level": 90, "group": "Core"},
    {"name": "Python (pandas)", "level": 70, "group": "Core"},
    {"name": "Data Visualization", "level": 75, "group": "Core"},
    {"name": "Power BI / Tableau", "level": 60, "group": "Tools"},
    {"name": "Statistics", "level": 65, "group": "Tools"},
    {"name": "A/B Testing", "level": 50, "group": "Tools"},
    {"name": "Storytelling with Data", "level": 70, "group": "Tools"},
]

PROJECTS = [
    {
        "id": "sales-dashboard",
        "cell": "A1",
        "name": "Regional Sales Dashboard",
        "summary": "An interactive dashboard tracking revenue, churn, and rep performance across five regions.",
        "tags": ["SQL", "Power BI", "DAX"],
        "link": "#",
    },
    {
        "id": "churn-model",
        "cell": "A2",
        "name": "Customer Churn Analysis",
        "summary": "Explored a subscription dataset to find the three strongest predictors of churn and proposed retention actions.",
        "tags": ["Python", "pandas", "scikit-learn"],
        "link": "#",
    },
    {
        "id": "survey-insights",
        "cell": "A3",
        "name": "Survey Insights Report",
        "summary": "Cleaned and analyzed 2,000+ open survey responses, surfacing themes with text analysis and cohort breakdowns.",
        "tags": ["Excel", "NLP basics", "Storytelling"],
        "link": "#",
    },
]

EXPERIENCE = [
    {
        "role": "Data Analytics Trainee",
        "org": "Your Bootcamp / Program",
        "period": "2025 — Present",
        "detail": "Working through applied projects covering SQL joins, dashboarding, and statistical fundamentals.",
    },
    {
        "role": "B.Sc / B.A in [Your Field]",
        "org": "Your University",
        "period": "2021 — 2025",
        "detail": "Coursework in statistics, research methods, and applied computing.",
    },
]

BLOG_POSTS = [
    {
        "slug": "why-i-love-messy-data",
        "title": "Why I Actually Enjoy Messy Data",
        "date": "2026-05-02",
        "excerpt": "Most people dread a dataset full of nulls and inconsistent formatting. Here's why I think that's where the real work begins.",
        "body": (
            "Most people dread opening a dataset full of nulls, inconsistent date "
            "formats, and duplicate rows. I've come to see that mess as the "
            "interesting part of the job.\n\n"
            "Cleaning data isn't just plumbing — it's the first round of analysis. "
            "Every missing value tells you something about how the data was "
            "collected. Every duplicate hints at a process problem upstream. By "
            "the time a dataset is clean, you already understand it better than "
            "someone who was just handed a tidy CSV.\n\n"
            "My approach: profile first (nulls, types, ranges), fix loudly (log "
            "every transformation so it's reversible), and validate against a "
            "sanity check before trusting a single chart."
        ),
    },
    {
        "slug": "first-dashboard-lessons",
        "title": "Three Things I'd Do Differently on My First Dashboard",
        "date": "2026-06-10",
        "excerpt": "My first dashboard had twelve charts. Nobody used it. Here's what I learned about building for an actual audience.",
        "body": (
            "My first dashboard had twelve charts on one page. It looked "
            "impressive in a portfolio screenshot. Nobody on the actual team "
            "used it.\n\n"
            "1. Start with the one decision the dashboard needs to support, not "
            "every metric you can compute.\n"
            "2. Default filters matter more than chart types — most users never "
            "touch a filter, so the default view has to already be useful.\n"
            "3. A dashboard that requires a legend to explain itself has already "
            "lost the reader. Label the data directly wherever you can."
        ),
    },
]

# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


def _load_messages():
    if not os.path.exists(MESSAGES_FILE):
        return []
    with open(MESSAGES_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def _save_message(entry):
    os.makedirs(DATA_DIR, exist_ok=True)
    messages = _load_messages()
    messages.append(entry)
    with open(MESSAGES_FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=2)


@app.route("/")
def index():
    return render_template(
        "index.html",
        profile=PROFILE,
        skills=SKILLS,
        projects=PROJECTS,
        experience=EXPERIENCE,
        posts=BLOG_POSTS[:3],
    )


@app.route("/blog")
def blog():
    return render_template("blog.html", profile=PROFILE, posts=BLOG_POSTS)


@app.route("/blog/<slug>")
def blog_post(slug):
    post = next((p for p in BLOG_POSTS if p["slug"] == slug), None)
    if post is None:
        return redirect(url_for("blog"))
    return render_template("post.html", profile=PROFILE, post=post)


@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    message = request.form.get("message", "").strip()

    if not name or not email or not message:
        flash("Please fill in every field before sending.", "error")
        return redirect(url_for("index") + "#contact")

    _save_message(
        {
            "name": name,
            "email": email,
            "message": message,
            "received_at": datetime.utcnow().isoformat(),
        }
    )
    flash("Message received — thanks for reaching out! I'll reply by email.", "success")
    return redirect(url_for("index") + "#contact")


if __name__ == "__main__":
    app.run(debug=True)
