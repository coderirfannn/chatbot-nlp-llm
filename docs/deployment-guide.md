# Deployment Guide

## Option 1: Render

Create a web service and use:

Build command:

```bash
pip install -r requirements.txt
```

Start command:

```bash
gunicorn app:app
```

Before deploying on Render, add this line to `requirements.txt`:

```text
gunicorn
```

Environment variables:

```text
GROQ_API_KEY
GROQ_MODEL
GROQ_BASE_URL
```

## Option 2: PythonAnywhere

1. Upload the project files.
2. Create a Flask web app.
3. Set the WSGI entry to use the Flask object named `app` from `app.py`.
4. Add environment variables for Groq.
5. Reload the web app.

## Option 3: Local College Demo

For practical evaluation, local demo is often enough.

Run:

```powershell
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## Deployment Notes

- Do not upload `.env` to GitHub.
- Add API keys only through deployment secrets.
- Keep `requirements.txt` updated.
- If the Groq model changes, update `GROQ_MODEL`.
- The local ML model trains at startup from `data/intents.csv`, so no separate model file is required.

