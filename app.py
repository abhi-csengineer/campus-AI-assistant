import os
import json
import random
from flask import Flask, render_template, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Determine base directory for reliable relative file paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INTENTS_PATH = os.path.join(BASE_DIR, "intents.json")
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

app = Flask(__name__, template_folder=TEMPLATE_DIR)

# 1. Load dataset with error handling
if not os.path.exists(INTENTS_PATH):
    raise FileNotFoundError(f"Could not find intents.json at {INTENTS_PATH}")

with open(INTENTS_PATH, "r", encoding="utf-8") as file:
    data = json.load(file)

# 2. Prepare training data
patterns = []
tags = []
responses_map = {}

for intent in data.get("intents", []):
    tag = intent["tag"]
    responses_map[tag] = intent["responses"]
    for pattern in intent.get("patterns", []):
        patterns.append(pattern)
        tags.append(tag)

if not patterns:
    raise ValueError("No training patterns found in intents.json!")

# 3. Train the NLP Classifier (Offline TF-IDF + Logistic Regression)
# Note: Omitting stop_words="english" ensures key conversational words
# (e.g. "who", "what", "when", "how", "up") are not stripped out.
vectorizer = TfidfVectorizer(ngram_range=(1, 2), lowercase=True)
X = vectorizer.fit_transform(patterns)

# C=10.0 provides a better fit for compact intent pattern datasets
classifier = LogisticRegression(random_state=42, max_iter=1000, C=10.0)
classifier.fit(X, tags)

# 4. Response prediction function with confidence threshold and zero-vector guard
FALLBACK_RESPONSE = (
    "I'm not quite sure I understand. Could you rephrase that, or ask about "
    "library hours, exams, attendance, or campus Wi-Fi?"
)

def get_bot_response(user_message):
    user_message = user_message.strip()
    if not user_message:
        return "Please type a message."

    user_vec = vectorizer.transform([user_message])

    # If none of the words match any trained vocabulary, fallback directly
    if user_vec.nnz == 0:
        return FALLBACK_RESPONSE

    probabilities = classifier.predict_proba(user_vec)[0]
    max_prob = max(probabilities)
    predicted_tag = classifier.classes_[probabilities.argmax()]

    # Fallback if the bot confidence is below 28%
    if max_prob < 0.28:
        return FALLBACK_RESPONSE

    return random.choice(responses_map.get(predicted_tag, [FALLBACK_RESPONSE]))

# 5. Flask Routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    # Safely retrieve JSON payload without raising exceptions
    payload = request.get_json(silent=True) or {}
    user_message = payload.get("message", "").strip()

    if not user_message:
        return jsonify({"reply": "Please type a message."}), 400

    reply = get_bot_response(user_message)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
