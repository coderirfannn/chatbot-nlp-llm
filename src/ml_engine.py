from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from collections import Counter, defaultdict
import csv
import math
import re


@dataclass
class AnswerScore:
    score: float
    similarity: float
    keyword_coverage: float
    covered_keywords: list[str]
    missing_keywords: list[str]


class IntentModel:
    """Pure-Python Multinomial Naive Bayes intent classifier."""

    def __init__(self, csv_path: str | Path = "data/intents.csv") -> None:
        self.csv_path = Path(csv_path)
        self.class_counts: Counter[str] = Counter()
        self.token_counts: dict[str, Counter[str]] = defaultdict(Counter)
        self.total_tokens: Counter[str] = Counter()
        self.vocabulary: set[str] = set()
        self._train()

    def _train(self) -> None:
        with self.csv_path.open("r", encoding="utf-8", newline="") as file:
            rows = list(csv.DictReader(file))

        for row in rows:
            intent = row["intent"]
            tokens = _tokens(row["text"])
            self.class_counts[intent] += 1
            self.token_counts[intent].update(tokens)
            self.total_tokens[intent] += len(tokens)
            self.vocabulary.update(tokens)

    def predict(self, text: str) -> tuple[str, float]:
        tokens = _tokens(text)
        if not tokens:
            return "greeting", 0.0

        scores: dict[str, float] = {}
        total_docs = sum(self.class_counts.values())
        vocab_size = max(len(self.vocabulary), 1)

        for intent, count in self.class_counts.items():
            log_prob = math.log(count / total_docs)
            denominator = self.total_tokens[intent] + vocab_size
            for token in tokens:
                token_count = self.token_counts[intent][token]
                log_prob += math.log((token_count + 1) / denominator)
            scores[intent] = log_prob

        best_intent = max(scores, key=scores.get)
        confidence = _softmax_confidence(scores, best_intent)
        return best_intent, confidence


class AnswerScorer:
    """Scores answer quality using pure-Python TF-IDF cosine similarity."""

    def score(self, student_answer: str, ideal_answer: str, keywords: list[str]) -> AnswerScore:
        student_answer = student_answer.strip()
        if not student_answer:
            return AnswerScore(0.0, 0.0, 0.0, [], keywords)

        similarity = _tfidf_cosine(student_answer, ideal_answer)
        normalized = _normalize(student_answer)
        covered = [keyword for keyword in keywords if _normalize(keyword) in normalized]
        missing = [keyword for keyword in keywords if keyword not in covered]
        keyword_coverage = len(covered) / max(len(keywords), 1)

        final_score = (similarity * 65.0) + (keyword_coverage * 35.0)
        return AnswerScore(
            score=round(final_score, 1),
            similarity=round(similarity * 100, 1),
            keyword_coverage=round(keyword_coverage * 100, 1),
            covered_keywords=covered,
            missing_keywords=missing,
        )


def recommend_topics(history: list[dict[str, object]]) -> list[str]:
    if not history:
        return [
            "Start with Unit III model evaluation because it is easy to demonstrate with ML metrics.",
            "Then revise Unit II search algorithms because interviewers often ask A* and CSP basics.",
        ]

    topic_scores: dict[str, list[float]] = {}
    for item in history:
        topic = str(item["topic"])
        topic_scores.setdefault(topic, []).append(float(item["score"]))

    weak_topics = sorted(
        ((topic, sum(scores) / len(scores)) for topic, scores in topic_scores.items()),
        key=lambda item: item[1],
    )

    recommendations = []
    for topic, average in weak_topics[:3]:
        if average < 70:
            recommendations.append(
                f"Revise {topic}: your average score is {average:.1f}/100. Practice definitions, examples, and one real use case."
            )

    if not recommendations:
        recommendations.append("Your scores are stable. Move to harder questions and practice concise viva-style answers.")
    return recommendations


def _tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def _normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def _tfidf_cosine(text_a: str, text_b: str) -> float:
    docs = [_tokens(text_a), _tokens(text_b)]
    vocabulary = sorted(set(docs[0]) | set(docs[1]))
    if not vocabulary:
        return 0.0

    vectors = []
    for doc in docs:
        counts = Counter(doc)
        length = max(len(doc), 1)
        vector = []
        for token in vocabulary:
            tf = counts[token] / length
            doc_frequency = sum(1 for item in docs if token in item)
            idf = math.log((1 + len(docs)) / (1 + doc_frequency)) + 1
            vector.append(tf * idf)
        vectors.append(vector)

    dot = sum(a * b for a, b in zip(vectors[0], vectors[1]))
    norm_a = math.sqrt(sum(a * a for a in vectors[0]))
    norm_b = math.sqrt(sum(b * b for b in vectors[1]))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def _softmax_confidence(scores: dict[str, float], best_intent: str) -> float:
    max_score = max(scores.values())
    exp_scores = {intent: math.exp(score - max_score) for intent, score in scores.items()}
    total = sum(exp_scores.values())
    return round(exp_scores[best_intent] / total, 2)

