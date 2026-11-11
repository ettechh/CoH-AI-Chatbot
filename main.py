import os
import logging
from flask import Flask, render_template, request, jsonify, redirect, url_for
from dotenv import load_dotenv
from mistralai import Mistral

load_dotenv()

app = Flask(__name__)

# ------------------ Mistral ------------------
client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

SYSTEM_PROMPT = """You are a supportive assistant for foster care and incarcerated youth.
Be warm, clear, and brief. Only share specific resources, phone numbers, or
eligibility details if you're confident they're accurate; otherwise say you're
not sure and suggest contacting a caseworker, 211, or the resource directly.
If someone may be in crisis or danger, encourage them to call or text 988
(or 911 in an emergency) and to reach out to a trusted adult."""

# ------------------ Tips Storage ------------------
anonymous_tips = []
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "supersecret")

# ------------------ Routes ------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.form.get("question", "").strip()
    if not user_input:
        return jsonify({"error": "No question provided"}), 400

    try:
        response = client.chat.complete(
            model="mistral-large-latest",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input},
            ],
        )
        return jsonify({"response": response.choices[0].message.content})
    except Exception:
        logging.exception("Mistral call failed")
        return jsonify({"error": "Something went wrong. Please try again."}), 500


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
