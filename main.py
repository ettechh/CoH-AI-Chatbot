import os
import logging
import requests
from flask import Flask, render_template, request, jsonify, redirect, url_for
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# ------------------ Mistral ------------------
MISTRAL_URL = "https://api.mistral.ai/v1/chat/completions"

SYSTEM_PROMPT = """You are a supportive assistant for foster care and incarcerated youth.
Be warm, clear, and brief. Only share specific resources, phone numbers, or
eligibility details if you're confident they're accurate; otherwise say you're
not sure and suggest contacting a caseworker, 211, or the resource directly.
If someone may be in crisis or danger, encourage them to call or text 988
(or 911 in an emergency) and to reach out to a trusted adult."""

# ------------------ Tips Storage ------------------
anonymous_tips = []
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "supersecret")


# ------------------ Helpers ------------------
def reply(text):
    # Same text under several common key names so the page can find it
    return jsonify({"response": text, "reply": text, "answer": text, "message": text})


# ------------------ Routes ------------------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.form.get("question", "").strip()
    if not user_input:
        return reply("Please type a question.")

    try:
        r = requests.post(
            MISTRAL_URL,
            headers={
                "Authorization": f"Bearer {os.getenv('MISTRAL_API_KEY')}",
                "Content-Type": "application/json",
            },
            json={
                "model": "mistral-large-latest",
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_input},
                ],
            },
            timeout=60,
        )
        if r.status_code != 200:
            logging.error("Mistral %s: %s", r.status_code, r.text)
            return reply(f"[DEBUG] Mistral returned {r.status_code}: {r.text[:300]}")
        return reply(r.json()["choices"][0]["message"]["content"])
    except Exception as e:
        logging.exception("Mistral call failed")
        return reply(f"[DEBUG] {type(e).__name__}: {e}")


@app.route("/tip", methods=["POST"])
def receive_tip():
    tip = request.form.get("tip")
    if tip:
        anonymous_tips.append(tip)
    return redirect(url_for("index"))


@app.route("/tips", methods=["GET", "POST"])
def view_tips():
    if request.method == "POST":
        password = request.form.get("password")
        if password == ADMIN_PASSWORD:
            return render_template("tips.html", tips=anonymous_tips)
        return render_template("login.html", error="Incorrect password")

    return render_template("login.html")


@app.route("/delete_tip", methods=["POST"])
def delete_tip():
    tip = request.form.get("tip")
    if tip in anonymous_tips:
        anonymous_tips.remove(tip)
    return redirect(url_for("view_tips"))


if __name__ == "__main__":
    app.run(debug=False)
