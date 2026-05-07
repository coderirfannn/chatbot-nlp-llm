# Syllabus Mapping

Project title: **PrepLens AI Interview Coach**

Project idea: An AI chatbot that conducts interview/viva practice for Artificial Intelligence Essentials. It asks syllabus-based questions, evaluates student answers using ML, gives feedback using Groq, and recommends weak topics.

## Course Outcome Mapping

| Course Outcome | How the Project Covers It |
|---|---|
| CO1: Explain foundations, characteristics, evolution, and applications of AI | The question bank includes AI foundations and application-based interview questions. |
| CO2: Apply state-space modeling and search techniques | Practice questions include state-space search, A* search, heuristics, and CSP. |
| CO3: Apply ML algorithms, evaluation methods, and probabilistic reasoning | The chatbot uses Naive Bayes for intent classification, TF-IDF features, similarity scoring, and questions on Bayes/model evaluation. |
| CO4: Use deep learning and NLP models for language-based applications | The chatbot itself is an NLP application. It also includes questions on neural networks, transformers, BERT, GPT, and attention. |
| CO5: Explain generative AI and prompt engineering with responsible use | Groq-based feedback demonstrates LLM usage. The system prompt controls feedback style and includes responsible boundaries. |
| CO6: Apply data and AI workflows, visualization, deployment, troubleshooting, MLOps | The app has a complete workflow: dataset, model training, UI, API integration, deployment guide, and lifecycle explanation. |

## Unit Mapping

| Unit | Project Connection |
|---|---|
| Unit I: Foundations and Applications of AI | Interview questions explain AI, intelligence, state space, and real-world AI use. |
| Unit II: Problem Solving and Search | Questions cover A*, heuristics, CSP, state-space search, and problem formulation. |
| Unit III: Machine Learning | Intent classifier uses supervised ML. Answer scoring uses TF-IDF and similarity. |
| Unit IV: Deep Learning and NLP | The chatbot is an NLP application and includes transformer/neural network questions. |
| Unit V: Generative AI and Prompt Engineering | Groq API is used for generative feedback. The prompt is structured with role, task, context, and output format. |
| Unit VI: Data Analysis, Tools, Lifecycle | Progress tracking, deployment, environment setup, troubleshooting, and app lifecycle are documented. |

## Where ML Is Included

The ML component is in `src/ml_engine.py`.

1. **Intent Classification**
   - Dataset: `data/intents.csv`
   - Algorithm: Multinomial Naive Bayes
   - Feature extraction: bag-of-words token counts
   - Output: predicted intent and confidence

2. **Answer Scoring**
   - Compares student answer with reference answer
   - Uses TF-IDF cosine similarity
   - Checks keyword coverage
   - Produces a numeric score out of 100

3. **Recommendation**
   - Uses student score history
   - Finds weak topics
   - Suggests revision areas

## Why This Is Better Than a Basic Chatbot

A basic chatbot only sends a message to an API and prints the response. This project has a local ML decision layer before the LLM response:

- The chatbot understands user intent using a trained local ML model.
- It scores answers using ML/NLP.
- It tracks performance.
- It recommends revision topics.
- The Groq API is used only for natural feedback, not for every important decision.
