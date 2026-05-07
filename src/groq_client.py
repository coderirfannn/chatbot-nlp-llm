from __future__ import annotations

import requests

from .config import config


class GroqClient:
    """Small OpenAI-compatible Groq client for chat completions."""

    def __init__(self) -> None:
        self.api_key = config.groq_api_key
        self.model = config.groq_model
        self.base_url = config.groq_base_url.rstrip("/")

    @property
    def is_configured(self) -> bool:
        return bool(self.api_key and self.api_key != "your_groq_api_key_here")

    def complete(self, messages: list[dict[str, str]], temperature: float = 0.35) -> str:
        if not self.is_configured:
            return (
                "Groq API key is not configured yet. The local ML score is available, "
                "but AI feedback needs GROQ_API_KEY in your .env file."
            )

        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": 550,
            },
            timeout=config.request_timeout,
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()


def build_feedback_prompt(question: str, ideal_answer: str, answer: str, ml_score: float) -> list[dict[str, str]]:
    system = (
        "You are an interview coach for an undergraduate Artificial Intelligence Essentials course. "
        "Give honest, short, human feedback. Do not sound like a generic AI assistant. "
        "Use the syllabus level: foundations, search, ML, deep learning, NLP, GenAI, MLOps. "
        "Return: Score, What worked, What is missing, Improved answer, Follow-up question."
    )
    user = f"""
Interview question:
{question}

Reference answer:
{ideal_answer}

Student answer:
{answer}

Local ML similarity score:
{ml_score:.1f}/100

Evaluate the student answer for a viva/interview. Keep it practical and specific.
"""
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]

