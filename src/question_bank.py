from __future__ import annotations

import json
from pathlib import Path
from random import choice


Question = dict[str, object]


def load_questions(path: str | Path = "data/questions.json") -> list[Question]:
    with Path(path).open("r", encoding="utf-8") as file:
        return json.load(file)


def filter_questions(
    questions: list[Question],
    unit: str | None = None,
    difficulty: str | None = None,
    topic_query: str | None = None,
) -> list[Question]:
    selected = questions
    if unit and unit != "Any":
        selected = [q for q in selected if q["unit"] == unit]
    if difficulty and difficulty != "Any":
        selected = [q for q in selected if q["difficulty"] == difficulty]
    if topic_query:
        query = topic_query.lower().strip()
        selected = [
            q
            for q in selected
            if query in str(q["topic"]).lower() or query in str(q["question"]).lower()
        ]
    return selected


def pick_question(questions: list[Question]) -> Question:
    if not questions:
        raise ValueError("No question matches the selected filters.")
    return choice(questions)

