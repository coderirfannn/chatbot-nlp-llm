# Viva Notes

## Project Definition

PrepLens is an ML-powered AI interview preparation chatbot. It asks Artificial Intelligence syllabus-based questions, evaluates student answers, gives feedback, and recommends weak topics.

## Problem Statement

Students often revise AI theory passively and do not know whether their answers are interview-ready. This chatbot creates an interactive practice environment where answers are scored and improved.

## Objectives

- Build an interview chatbot for INT428.
- Use ML to classify user intent.
- Use NLP similarity to evaluate answers.
- Use Groq API to generate feedback.
- Track student progress and recommend weak topics.

## ML Algorithm Used

The project uses Multinomial Naive Bayes for intent classification.

Why Naive Bayes:

- It is simple and explainable.
- It works well for small text classification tasks.
- It is easy to demonstrate in a college viva.

Feature extraction:

- Bag-of-words token counts convert text into numerical features for intent classification.
- TF-IDF converts answers into numerical vectors for similarity scoring.

## Answer Evaluation Method

The answer score combines:

- TF-IDF cosine similarity with the reference answer
- Keyword coverage

This gives a measurable score instead of only subjective chatbot feedback.

## Role of Groq API

Groq is used for natural language feedback. It receives the question, reference answer, student answer, and ML score. Then it returns practical coaching feedback.

## Limitations

- Current progress is stored only during the active session.
- The question bank can be expanded.
- The scoring method is useful for short answers but not perfect for long essays.
- Final evaluation should still involve a teacher for marks.

## Future Scope

- Add login and database storage.
- Add charts for topic-wise progress.
- Add voice-based interview mode.
- Add more datasets for stronger intent classification.
- Add admin panel for faculty to add questions.
