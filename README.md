# Data Analyst Portfolio (Flask)

A single-page portfolio site with an About, Skills, Projects, Experience,
Blog, and Contact form — styled like an open spreadsheet ("data ledger"
theme): grid-paper backgrounds, cell-reference labels, a formula-bar hero,
and bottom navigation styled like Excel sheet tabs.

## Run it

```bash
pip install -r requirements.txt
python app.py
```

Then open http://127.0.0.1:5000

## Customize

Almost everything lives in `app.py` under the `CONFIG` section near the
top of the file:

- `PROFILE` — your name, title, bio, email, links, resume URL
- `SKILLS` — name + proficiency (0-100) for the skills bar chart
- `PROJECTS` — your project cards
- `EXPERIENCE` — your work/education timeline
- `BLOG_POSTS` — blog posts (title, date, excerpt, body)

Add your real résumé PDF at `static/resume.pdf` — the "Download résumé"
button already points there.

Styling lives in `static/css/style.css`; the color palette and fonts are
defined as CSS variables at the top of that file if you want to adjust
the look.

## Contact form

Submissions are saved to `data/messages.json` (created automatically).
There's no email-sending wired up yet — for production you'd want to
connect an email service (e.g. Flask-Mail, SendGrid) inside the
`contact()` view in `app.py`.

## Deploying

This is a standard Flask app — it deploys to any host that supports
Python (Render, Railway, PythonAnywhere, Fly.io, etc.). For production,
set a real `app.secret_key` via an environment variable instead of the
placeholder in `app.py`, and run behind a WSGI server like gunicorn:

```bash
gunicorn app:app
```
