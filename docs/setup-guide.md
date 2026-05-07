# Setup Guide

This guide is written for a Windows college laptop using PowerShell.

## 1. Install Python

Install Python 3.10 or newer.

Check Python:

```powershell
python --version
```

## 2. Create Virtual Environment

From the project folder:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 3. Install Requirements

```powershell
pip install -r requirements.txt
```

## 4. Create Environment File

```powershell
Copy-Item .env.example .env
```

Open `.env` and set:

```text
GROQ_API_KEY=your_actual_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile
GROQ_BASE_URL=https://api.groq.com/openai/v1
```

## 5. Run the App

```powershell
python app.py
```

Flask will show a local URL, usually:

```text
http://127.0.0.1:5000
```

## 6. Test Without Groq Key

The project still works without a Groq key:

- Intent classification works
- Answer scoring works
- Progress tracking works

Only AI-generated feedback and concept explanation need the Groq API key.

## 7. Troubleshooting

### Problem: `ModuleNotFoundError`

Run:

```powershell
pip install -r requirements.txt
```

### Problem: Groq API key not configured

Check `.env`:

```text
GROQ_API_KEY=your_actual_key
```

Restart the Flask app after changing `.env`.

### Problem: Port already in use

Use:

```powershell
$env:FLASK_RUN_PORT=5001
python app.py
```
