from flask import Blueprint, render_template, session, request, jsonify
from utils.decorators import login_required
import requests
import os
chat = Blueprint(
    "chat", __name__,
    static_folder="static",
    template_folder="template"
)
ai_api_url = os.environ.get("AI_API_URL")

@chat.route("/chat")
@login_required
def chat_page():
    return render_template("chat.html", username=session.get("username"))

@chat.route("/chat/send", methods=["POST"])
@login_required
def send_message():
    user_message = request.json.get("message", "").strip()
    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    try:
        response = requests.post(
            ai_api_url,
            json={"query": user_message},
            timeout=90 
        )
        response.raise_for_status()
        data = response.json()

        assistant_reply = data["messages"][-1]["content"] if data.get("messages") else "Sorry, something went wrong."
    except requests.exceptions.RequestException as e:
        assistant_reply = "Try again."

    return jsonify({"reply": assistant_reply})