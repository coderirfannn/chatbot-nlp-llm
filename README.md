# PrepLens AI Interview Coach

PrepLens is an AI interview preparation chatbot for **INT428: Artificial Intelligence Essentials**. It helps students practice viva questions, evaluate answers, and identify weak topics before exams or project evaluation.

The project intentionally uses two layers:

1. **Local ML layer**: intent classification and answer scoring.
2. **Groq API layer**: human-like interview feedback and concept explanations.

This keeps the project academically valid because the chatbot does not depend only on an LLM API. The ML pipeline is visible, explainable, and easy to demonstrate.

## Main Features

- AI syllabus-based interview question practice
- ML intent detection using a pure-Python Naive Bayes classifier
- ML answer scoring using TF-IDF semantic similarity and keyword coverage
- Groq-powered feedback for answer improvement
- Progress tracking with weak-topic recommendation
- Practical coverage of AI, search, ML, NLP, GenAI, prompt engineering, and MLOps

## Tech Stack

- Python
- Flask
- Pure-Python Naive Bayes classifier
- Pure-Python TF-IDF answer scorer
- Groq OpenAI-compatible Chat Completions API

## Project Structure

```text
.
|-- app.py
|-- data/
|   |-- intents.csv
|   `-- questions.json
|-- docs/
|   |-- deployment-guide.md
|   |-- setup-guide.md
|   |-- syllabus-mapping.md
|   |-- viva-notes.md
|   `-- workflow.md
|-- src/
|   |-- config.py
|   |-- groq_client.py
|   |-- ml_engine.py
|   `-- question_bank.py
|-- .env.example
`-- requirements.txt
```

## Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Open `.env` and add your Groq API key:

```text
GROQ_API_KEY=your_actual_key
```

Run the app:

```powershell
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## Groq API

The project uses Groq's OpenAI-compatible endpoint:


```

Default model:

```text
llama-3.3-70b-versatile
```

You can change the model in `.env`.

## What to Explain to Faculty

This is not only a prompt-based chatbot. It includes:

- A supervised Naive Bayes classifier for chatbot intent detection.
- Feature extraction using bag-of-words and TF-IDF.
- Model evaluation concepts through confidence and answer scoring.
- NLP-based answer similarity.
- LLM-based feedback using Groq.
- Topic recommendation based on student performance.

## Useful Commands

Run app:

```powershell
python app.py
```

Check Python syntax:

```powershell
python -m compileall app.py src
```

# chatbot-nlp-llm
