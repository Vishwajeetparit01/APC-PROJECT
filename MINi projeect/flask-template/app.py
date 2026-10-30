
from flask import Flask, render_template, request, jsonify
from difflib import SequenceMatcher
from datetime import datetime

app = Flask(__name__)

faqs = {
    "hello": "Hello! Welcome to the College Enquiry Chatbot. How can I help you?",
    "hi": "Hi! Ask me about courses, admissions, fees or scholarships.",
    "courses": "Our college offers various engineering courses. Please check the official college website for the current course list.",
    "fees": "Course fees depend on the branch and admission category. Please contact the college office for the latest fees.",
    "admission": "Admissions depend on eligibility and the applicable admission process. Please check the official admission notice.",
    "departments": "The college has different engineering departments. Ask about a specific department for more information.",
    "scholarship": "Eligible students can check government scholarship schemes through the official scholarship portal.",
    "timing": "Please contact the college office for current lecture timings.",
    "documents": "Common admission documents include marksheets, identity proof, photographs and applicable certificates.",
    "exam": "Please check the official college notice or examination department for the latest exam timetable.",
    "placement": "Contact the college placement cell for current placement statistics and company information.",
    "library": "Please contact the college library for its working hours and available facilities."
}

chat_history = []

def get_answer(message):
    message = message.lower().strip()

    if message in faqs:
        return faqs[message]

    for keyword, answer in faqs.items():
        if keyword in message:
            return answer

    best_match = max(
        faqs,
        key=lambda key: SequenceMatcher(None, message, key).ratio()
    )

    if SequenceMatcher(None, message, best_match).ratio() >= 0.65:
        return faqs[best_match]

    return "Sorry, I don't know the answer yet. Please contact the college office for accurate information."

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()

    if not message:
        return jsonify({"reply": "Please type a question."}), 400

    answer = get_answer(message)

    chat_history.append({
        "question": message,
        "answer": answer,
        "time": datetime.now().strftime("%I:%M %p")
    })

    return jsonify({"reply": answer})

@app.route("/history")
def history():
    return jsonify(chat_history)

if __name__ == "__main__":
    app.run(debug=True)
