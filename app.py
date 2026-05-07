from __future__ import annotations

import os

from flask import Flask, jsonify, render_template_string, request

from src.groq_client import GroqClient, build_feedback_prompt
from src.ml_engine import AnswerScorer, IntentModel, recommend_topics
from src.question_bank import filter_questions, load_questions, pick_question


app = Flask(__name__)

questions = load_questions()
intent_model = IntentModel()
answer_scorer = AnswerScorer()
groq = GroqClient()


PAGE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>PrepLens AI Interview Coach</title>
  <style>
    :root {
      --ink: #172033;
      --muted: #667085;
      --line: #d9e2ef;
      --panel: #f7f9fd;
      --accent: #2156d9;
      --accent-strong: #163f9f;
      --good: #177245;
      --warn: #a15c07;
      --soft-blue: #edf4ff;
      --soft-green: #edf8f2;
      --soft-amber: #fff7e8;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: Inter, "Segoe UI", Arial, Helvetica, sans-serif;
      color: var(--ink);
      background: #f5f7fb;
    }
    header {
      background: #ffffff;
      border-bottom: 1px solid var(--line);
    }
    .topbar {
      max-width: 1180px;
      margin: 0 auto;
      padding: 18px 22px 14px;
      display: flex;
      justify-content: space-between;
      gap: 16px;
      align-items: center;
    }
    h1 { margin: 0; font-size: 28px; letter-spacing: 0; }
    h2 { margin: 0 0 14px; font-size: 20px; letter-spacing: 0; }
    h3 { margin: 0 0 10px; font-size: 15px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.04em; }
    p { line-height: 1.45; }
    .subtitle { margin: 4px 0 0; color: var(--muted); }
    .brand-row { display: flex; align-items: center; gap: 12px; }
    .mark {
      width: 46px;
      height: 46px;
      border-radius: 10px;
      background: var(--accent);
      color: #fff;
      display: grid;
      place-items: center;
      font-weight: 800;
      letter-spacing: 0;
    }
    .status {
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 12px 14px;
      min-width: 220px;
      background: var(--soft-blue);
      font-size: 14px;
    }
    .hero {
      max-width: 1180px;
      margin: 0 auto;
      padding: 22px;
      display: grid;
      grid-template-columns: 1.25fr 0.75fr;
      gap: 18px;
    }
    .hero-panel {
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 20px;
      background: #ffffff;
    }
    .hero-title {
      font-size: 24px;
      font-weight: 800;
      margin: 0 0 8px;
    }
    .hero-copy {
      max-width: 760px;
      margin: 0;
      color: var(--muted);
    }
    .chip-row {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      margin-top: 16px;
    }
    .chip {
      border: 1px solid var(--line);
      border-radius: 999px;
      padding: 7px 10px;
      background: #ffffff;
      color: #344054;
      font-size: 13px;
      font-weight: 700;
    }
    .hero-stats {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 10px;
    }
    .stat {
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 12px;
      background: #ffffff;
    }
    .stat b { display: block; font-size: 22px; margin-bottom: 2px; }
    .stat span { color: var(--muted); font-size: 13px; }
    main {
      max-width: 1180px;
      margin: 0 auto;
      padding: 0 22px 28px;
    }
    .grid {
      display: grid;
      grid-template-columns: 320px 1fr;
      gap: 18px;
      align-items: start;
    }
    section, aside {
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 20px;
      background: #fff;
      box-shadow: 0 8px 22px rgba(15, 23, 42, 0.04);
    }
    label {
      display: block;
      font-weight: 700;
      margin-top: 12px;
      margin-bottom: 6px;
      font-size: 14px;
    }
    select, input, textarea {
      width: 100%;
      border: 1px solid var(--line);
      border-radius: 6px;
      padding: 11px 12px;
      font: inherit;
      background: #fff;
    }
    select:focus, input:focus, textarea:focus {
      outline: 3px solid rgba(33, 86, 217, 0.14);
      border-color: var(--accent);
    }
    textarea { min-height: 145px; resize: vertical; }
    button {
      border: 0;
      border-radius: 6px;
      padding: 11px 15px;
      background: var(--accent);
      color: #fff;
      font-weight: 700;
      cursor: pointer;
      margin-top: 14px;
    }
    button:hover { background: var(--accent-strong); }
    button.secondary {
      background: #334155;
    }
    .wide-button { width: 100%; }
    .question {
      background: linear-gradient(180deg, #ffffff, #f8fbff);
      border: 1px solid var(--line);
      padding: 18px;
      border-radius: 8px;
      margin-bottom: 14px;
    }
    .meta { color: var(--accent); font-size: 14px; margin-bottom: 8px; font-weight: 800; }
    #questionText { font-size: 19px; line-height: 1.45; font-weight: 700; }
    .score-row {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 12px;
      margin: 14px 0;
    }
    .metric {
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 12px;
      background: #fff;
    }
    .metric strong { display: block; font-size: 22px; margin-top: 5px; }
    .metric.good { border-left: 4px solid var(--good); }
    .metric.warn { border-left: 4px solid var(--warn); }
    .metric.bad { border-left: 4px solid #a11; }
    .spinner {
      display: inline-block;
      width: 14px;
      height: 14px;
      border: 2px solid rgba(0,0,0,0.08);
      border-top-color: rgba(0,0,0,0.35);
      border-radius: 50%;
      animation: spin 800ms linear infinite;
      vertical-align: -3px;
      margin-right: 8px;
    }
    @keyframes spin { to { transform: rotate(360deg); } }
    .small-btn { padding: 8px 10px; font-size: 13px; border-radius: 6px; }
    .feedback {
      white-space: pre-wrap;
      border: 1px solid var(--line);
      border-left: 4px solid var(--accent);
      border-radius: 8px;
      padding: 14px;
      background: #fbfcff;
    }
    .pill-box {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin: 10px 0;
    }
    .pill {
      border-radius: 999px;
      padding: 7px 10px;
      font-size: 13px;
      font-weight: 700;
      border: 1px solid var(--line);
      background: #fff;
    }
    .pill.good { background: var(--soft-green); color: var(--good); }
    .pill.warn { background: var(--soft-amber); color: var(--warn); }
    .chat-log {
      border: 1px solid var(--line);
      min-height: 300px;
      max-height: 380px;
      overflow: auto;
      padding: 12px;
      border-radius: 8px;
      background: var(--panel);
    }
    .msg { margin-bottom: 10px; }
    .msg b { display: block; font-size: 13px; color: var(--muted); }
    .trace {
      margin-top: 14px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fff;
      overflow: hidden;
    }
    .trace-head {
      padding: 12px 14px;
      display: flex;
      justify-content: space-between;
      gap: 12px;
      align-items: center;
      border-bottom: 1px solid var(--line);
      background: #f8fbff;
    }
    .trace-head strong { font-size: 14px; }
    .trace-status {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 6px 10px;
      border-radius: 999px;
      background: var(--soft-green);
      color: var(--good);
      font-weight: 700;
      font-size: 13px;
    }
    .trace-body { padding: 12px 14px; }
    .trace-item { margin-bottom: 10px; }
    .trace-item:last-child { margin-bottom: 0; }
    .trace-label { font-size: 12px; text-transform: uppercase; letter-spacing: 0.04em; color: var(--muted); font-weight: 800; margin-bottom: 4px; }
    .trace-code {
      white-space: pre-wrap;
      word-break: break-word;
      background: #0f172a;
      color: #e2e8f0;
      border-radius: 6px;
      padding: 10px 12px;
      font-size: 13px;
      line-height: 1.45;
    }
    .tabs {
      display: flex;
      gap: 8px;
      margin-bottom: 16px;
      flex-wrap: wrap;
      background: #ffffff;
      border: 1px solid var(--line);
      padding: 8px;
      border-radius: 8px;
    }
    .tabs button {
      background: transparent;
      color: var(--ink);
      margin-top: 0;
    }
    .tabs button.active {
      background: var(--accent);
      color: #fff;
    }
    .hidden { display: none; }
    table { width: 100%; border-collapse: collapse; margin-top: 10px; }
    th, td { border-bottom: 1px solid var(--line); padding: 8px; text-align: left; font-size: 14px; }
    .fit-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 14px;
    }
    .fit-item {
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 14px;
      background: var(--panel);
    }
    .fit-item b { display: block; margin-bottom: 6px; }
    @media (max-width: 820px) {
      .topbar, .hero { display: block; }
      .status { margin-top: 12px; }
      .hero-panel { margin-bottom: 12px; }
      .hero-stats { grid-template-columns: 1fr; }
      .grid { grid-template-columns: 1fr; }
      .score-row { grid-template-columns: 1fr; }
      .fit-grid { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  <header>
    <div class="topbar">
      <div class="brand-row">
        <div class="mark">PL</div>
        <div>
          <h1>PrepLens AI Interview Coach</h1>
          <p class="subtitle">ML-powered viva practice for INT428: Artificial Intelligence Essentials</p>
        </div>
      </div>
      <div class="status">
        <b>Groq:</b> {{ "Connected" if groq_ready else "Local ML mode" }}<br>
        <span>ML: Naive Bayes intent + TF-IDF scoring</span>
      </div>
    </div>
    <div class="hero">
      <div class="hero-panel">
        <p class="hero-title">Practice AI viva answers with scoring, feedback, and revision guidance.</p>
        <p class="hero-copy">Built for college evaluation: the chatbot uses a local ML classifier, answer similarity scoring, a syllabus question bank, and optional Groq feedback for improved interview responses.</p>
        <div class="chip-row">
          <span class="chip">Intent Classification</span>
          <span class="chip">Answer Scoring</span>
          <span class="chip">Groq Feedback</span>
          <span class="chip">INT428 Mapped</span>
        </div>
      </div>
      <div class="hero-stats">
        <div class="stat"><b>{{ question_count }}</b><span>Syllabus questions</span></div>
        <div class="stat"><b>6</b><span>Course units</span></div>
        <div class="stat"><b>3</b><span>ML/NLP layers</span></div>
      </div>
    </div>
  </header>

  <main>
    <div class="tabs">
      <button class="active" data-testid="tab-practice" onclick="showTab('practice', this)">Practice</button>
      <button data-testid="tab-chatbot" onclick="showTab('chatbot', this)">Chatbot</button>
      <button data-testid="tab-progress" onclick="showTab('progress', this)">Progress</button>
      <button data-testid="tab-fit" onclick="showTab('fit', this)">Project Fit</button>
    </div>

    <div id="practice">
      <div class="grid">
        <aside>
          <h3>Interview Setup</h3>
          <h2>Question Controls</h2>
          <label for="unit">Unit</label>
          <select id="unit">
            <option>Any</option>
            {% for unit in units %}<option>{{ unit }}</option>{% endfor %}
          </select>
          <label for="difficulty">Difficulty</label>
          <select id="difficulty">
            <option>Any</option><option>Easy</option><option>Medium</option><option>Hard</option>
          </select>
          <label for="topic">Topic search</label>
          <input id="topic" placeholder="A*, NLP, MLOps">
          <button class="wide-button" data-testid="pick-question" onclick="pickQuestion()">Pick question</button>
          
          <p class="subtitle">Tip: define the concept, give an example, then mention one metric or limitation.</p>
        </aside>

        <section>
          <h3>Practice Workspace</h3>
          <h2>Interview Round</h2>
          <div class="question">
            <div id="questionMeta" class="meta"></div>
            <div id="questionText"></div>
          </div>
          <label for="answer">Your answer</label>
          <textarea id="answer" data-testid="answer-input" placeholder="Type your viva answer here..."></textarea>
          <button data-testid="evaluate-answer" onclick="evaluateAnswer()">Evaluate answer</button>
          <div id="evaluation"></div>
          <button id="copyFeedbackBtn" class="small-btn secondary hidden" onclick="copyFeedback()">Copy feedback</button>
        </section>
      </div>
    </div>

    <div id="chatbot" class="hidden">
      <section>
        <h3>Conversation Mode</h3>
        <h2>Chatbot</h2>
        <p class="subtitle">Try: ask me an NLP question, explain A* search, or which unit should I revise?</p>
        <div id="chatLog" class="chat-log"></div>
        <div id="chatTrace" class="trace hidden"></div>
        <label for="chatInput">Message</label>
        <input id="chatInput" data-testid="chat-input" placeholder="Ask the interview chatbot...">
        <button data-testid="send-chat" onclick="sendChat()">Send</button>
      </section>
    </div>

    <div id="progress" class="hidden">
      <section>
        <h3>Performance Review</h3>
        <h2>Progress</h2>
        <div id="progressBox">No evaluated answers yet.</div>
      </section>
    </div>

    <div id="fit" class="hidden">
      <section>
        <h3>Faculty Evaluation</h3>
        <h2>Project Fit</h2>
        <div class="fit-grid">
          <div class="fit-item"><b>Machine Learning</b>Naive Bayes detects user intent from trained examples.</div>
          <div class="fit-item"><b>NLP</b>TF-IDF similarity compares student answers with reference answers.</div>
          <div class="fit-item"><b>Generative AI</b>Groq produces interview-style feedback from the ML score and answer context.</div>
          <div class="fit-item"><b>MLOps Basics</b>Setup, environment variables, troubleshooting, and deployment are documented.</div>
        </div>
      </section>
    </div>
  </main>

  <script>
    let currentQuestion = {{ first_question | tojson }};
    let history = [];

    function showTab(id, button) {
      for (const name of ["practice", "chatbot", "progress", "fit"]) {
        document.getElementById(name).classList.add("hidden");
      }
      document.getElementById(id).classList.remove("hidden");
      for (const item of document.querySelectorAll(".tabs button")) item.classList.remove("active");
      button.classList.add("active");
      if (id === "progress") renderProgress();
    }

    function renderQuestion() {
      document.getElementById("questionMeta").innerText =
        `${currentQuestion.unit} - ${currentQuestion.topic} (${currentQuestion.difficulty})`;
      document.getElementById("questionText").innerText = currentQuestion.question;
      document.getElementById("evaluation").innerHTML = "";
      document.getElementById("answer").value = "";
    }

    async function pickQuestion() {
      const btn = document.querySelector('[data-testid="pick-question"]');
      btn.disabled = true;
      const original = btn.innerText;
      btn.innerHTML = '<span class="spinner"></span>Picking...';
      try {
        const params = new URLSearchParams({
          unit: document.getElementById("unit").value,
          difficulty: document.getElementById("difficulty").value,
          topic: document.getElementById("topic").value
        });
        const res = await fetch(`/api/question?${params}`);
        const data = await res.json();
        if (data.error) {
          alert(data.error);
          return;
        }
        currentQuestion = data;
        renderQuestion();
      } finally {
        btn.disabled = false;
        btn.innerText = original;
      }
    }

    async function evaluateAnswer() {
      const answer = document.getElementById("answer").value;
      const box = document.getElementById("evaluation");
      const btn = document.querySelector('[data-testid="evaluate-answer"]');
      btn.disabled = true;
      const original = btn.innerText;
      btn.innerHTML = '<span class="spinner"></span>Evaluating...';
      box.innerHTML = "";
      try {
        const res = await fetch("/api/evaluate", {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify({question_id: currentQuestion.id, answer})
        });
        const data = await res.json();
        history.push({
          unit: currentQuestion.unit,
          topic: currentQuestion.topic,
          difficulty: currentQuestion.difficulty,
          score: data.score.score,
          similarity: data.score.similarity,
          keyword_coverage: data.score.keyword_coverage
        });

        const scoreClass = data.score.score >= 75 ? 'good' : (data.score.score >= 50 ? 'warn' : 'bad');
        box.innerHTML = `
          <div class="score-row">
            <div class="metric ${scoreClass}">ML score<strong>${data.score.score}/100</strong></div>
            <div class="metric ${scoreClass}">Similarity<strong>${data.score.similarity}%</strong></div>
            <div class="metric ${scoreClass}">Keywords<strong>${data.score.keyword_coverage}%</strong></div>
          </div>
          <p><b>Covered:</b> ${data.score.covered_keywords.join(", ") || "None"}</p>
          <p><b>Missing:</b> ${data.score.missing_keywords.join(", ") || "None"}</p>
          <h2>Coach Feedback</h2>
          <div id="feedbackBox" class="feedback">${escapeHtml(data.feedback)}</div>
        `;

        const copyBtn = document.getElementById('copyFeedbackBtn');
        if (copyBtn) {
          copyBtn.classList.remove('hidden');
        }
      } finally {
        btn.disabled = false;
        btn.innerText = original;
      }
    }

    async function sendChat() {
      const input = document.getElementById("chatInput");
      const prompt = input.value.trim();
      if (!prompt) return;
      appendMessage("You", prompt);
      input.value = "";
      const requestBody = {message: prompt, history};
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(requestBody)
      });
      const data = await res.json();
      appendMessage("PrepLens", `${data.response}\\n\\nIntent: ${data.intent} (${data.confidence})`);
      renderChatTrace(prompt, requestBody, data, res.ok);
    }

    function appendMessage(sender, text) {
      const log = document.getElementById("chatLog");
      const item = document.createElement("div");
      item.className = "msg";
      item.innerHTML = `<b>${sender}</b>${escapeHtml(text)}`;
      log.appendChild(item);
      log.scrollTop = log.scrollHeight;
    }

    function renderChatTrace(prompt, requestBody, data, ok) {
      const trace = document.getElementById("chatTrace");
      trace.classList.remove("hidden");
      trace.innerHTML = `
        <div class="trace-head">
          <strong>API Call Trace</strong>
          <span class="trace-status">${ok ? "Successful execution" : "Execution failed"}</span>
        </div>
        <div class="trace-body">
          <div class="trace-item">
            <div class="trace-label">User prompt</div>
            <div class="trace-code">${escapeHtml(prompt)}</div>
          </div>
          <div class="trace-item">
            <div class="trace-label">API request</div>
            <div class="trace-code">POST /api/chat\n${escapeHtml(JSON.stringify(requestBody, null, 2))}</div>
          </div>
          <div class="trace-item">
            <div class="trace-label">AI-generated response</div>
            <div class="trace-code">${escapeHtml(data.response)}\n\nIntent: ${escapeHtml(data.intent)} (${escapeHtml(String(data.confidence))})</div>
          </div>
        </div>
      `;
    }

    function copyFeedback() {
      const fb = document.getElementById('feedbackBox');
      if (!fb) return;
      navigator.clipboard.writeText(fb.innerText).then(() => {
        const btn = document.getElementById('copyFeedbackBtn');
        const prev = btn.innerText;
        btn.innerText = 'Copied!';
        setTimeout(() => btn.innerText = prev, 1500);
      });
    }

    function renderProgress() {
      const box = document.getElementById("progressBox");
      if (!history.length) {
        box.innerText = "No evaluated answers yet.";
        return;
      }
      const avg = history.reduce((sum, item) => sum + item.score, 0) / history.length;
      let table = `<p><b>Questions evaluated:</b> ${history.length} &nbsp; <b>Average score:</b> ${avg.toFixed(1)}/100</p>`;
      table += "<table><tr><th>Unit</th><th>Topic</th><th>Difficulty</th><th>Score</th></tr>";
      for (const item of history) {
        table += `<tr><td>${item.unit}</td><td>${item.topic}</td><td>${item.difficulty}</td><td>${item.score}</td></tr>`;
      }
      table += "</table>";
      box.innerHTML = table;
    }

    function escapeHtml(text) {
      return String(text)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
    }

    // Keyboard helpers
    document.getElementById('chatInput').addEventListener('keydown', (e) => {
      if (e.key === 'Enter') { e.preventDefault(); sendChat(); }
    });
    document.getElementById('answer').addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && e.ctrlKey) { e.preventDefault(); evaluateAnswer(); }
    });

    renderQuestion();
  </script>
</body>
</html>
"""


@app.get("/")
def index():
    units = sorted({str(question["unit"]) for question in questions})
    return render_template_string(
        PAGE,
        units=units,
        first_question=questions[0],
        groq_ready=groq.is_configured,
    )


@app.get("/api/question")
def api_question():
    try:
        selected = filter_questions(
            questions,
            request.args.get("unit", "Any"),
            request.args.get("difficulty", "Any"),
            request.args.get("topic", ""),
        )
        return jsonify(pick_question(selected))
    except ValueError as error:
        return jsonify({"error": str(error)}), 404


@app.post("/api/evaluate")
def api_evaluate():
    payload = request.get_json(force=True)
    question = next((item for item in questions if item["id"] == payload.get("question_id")), questions[0])
    answer = str(payload.get("answer", ""))
    score = answer_scorer.score(answer, str(question["ideal_answer"]), list(question["keywords"]))

    try:
        feedback = groq.complete(
            build_feedback_prompt(
                str(question["question"]),
                str(question["ideal_answer"]),
                answer,
                score.score,
            )
        )
    except Exception as error:
        feedback = f"Groq feedback failed: {error}"

    return jsonify({"score": score.__dict__, "feedback": feedback})


@app.post("/api/chat")
def api_chat():
    payload = request.get_json(force=True)
    message = str(payload.get("message", ""))
    history = payload.get("history", [])
    intent, confidence = intent_model.predict(message)

    if intent == "question_request":
        question = pick_question(questions)
        response = f"Question from {question['unit']} - {question['topic']}: {question['question']}"
    elif intent == "recommendation":
        response = "\n".join(recommend_topics(history))
    elif intent == "greeting":
        response = "Hi. Tell me a topic, or ask me to start a mock AI interview."
    elif intent == "closing":
        response = "Session ended. Your progress remains visible in the Progress tab."
    elif intent == "explain_concept":
        try:
            response = groq.complete(
                [
                    {
                        "role": "system",
                        "content": "Explain INT428 AI concepts briefly with one interview example.",
                    },
                    {"role": "user", "content": message},
                ]
            )
        except Exception as error:
            response = f"Groq explanation failed: {error}"
    else:
        response = "I can ask questions, evaluate answers, explain concepts, and recommend revision topics."

    return jsonify({"response": response, "intent": intent, "confidence": confidence})


if __name__ == "__main__":
    port = int(os.getenv("FLASK_RUN_PORT", "5000"))
    app.run(debug=False, port=port, use_reloader=False)
