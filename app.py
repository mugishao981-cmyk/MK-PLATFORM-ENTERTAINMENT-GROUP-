import os
from flask import Flask, request, jsonify, render_template
import whisper
import requests
from gtts import gTTS
import tempfile

app = Flask(__name__)

model = whisper.load_model("base")

# ================= HOME UI =================
@app.route("/")
def home():
    return render_template("index.html")

# ================= YOUTUBE SUMMARY (TEXT INPUT) =================
@app.route("/api/summarize", methods=["GET"])
def summarize():
    text = request.args.get("text")

    if not text:
        return jsonify({"error": "no text provided"})

    summary = "🧠 AI Summary: " + text[:200] + "..."

    return jsonify({
        "original": text,
        "summary": summary
    })

# ================= SPEECH → TEXT (SUBTITLES) =================
@app.route("/api/speech", methods=["POST"])
def speech():
    file = request.files["file"]

    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    file.save(temp.name)

    result = model.transcribe(temp.name)

    return jsonify({
        "text": result["text"]
    })

# ================= AI VOICE (TEXT → SPEECH) =================
@app.route("/api/voice", methods=["GET"])
def voice():
    text = request.args.get("text")

    tts = gTTS(text=text, lang="en")
    file = "voice.mp3"
    tts.save(file)

    return jsonify({
        "voice": file
    })

# ================= KINYARWANDA SUPPORT (SIMPLE) =================
@app.route("/api/rw", methods=["GET"])
def rw():
    text = request.args.get("text")

    return jsonify({
        "message": f"🗣️ (Kinyarwanda AI) Nakumva: {text}"
    })

# ================= RUN =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
