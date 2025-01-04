from flask import Flask, render_template, request, jsonify
# Import fungsi untuk mendapatkan chat
from youtube_chat import get_live_chat_messages, get_live_chat_id, predict_toxicity

app = Flask(__name__)

# Route untuk Homepage


@app.route("/")
def index():
    return render_template("index.html")

# Route untuk Mendapatkan Live Chat secara berkala


@app.route("/get_chats", methods=["POST"])
def get_chats():
    video_id = request.json.get("video_id")
    if not video_id:
        return jsonify({"error": "Video ID is required"}), 400

    try:
        # Ambil live chat ID dari video
        live_chat_id = get_live_chat_id(video_id)
        # Ambil chat messages untuk live chat ID
        messages = get_live_chat_messages(live_chat_id)
        # Prediksi toxicitas pada setiap pesan
        results = []
        for message in messages:
            toxicity = predict_toxicity(message["message"])
            results.append({
                "author": message["author"],
                "message": message["message"],
                "toxicity": toxicity
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(results)


# Jalankan aplikasi Flask
if __name__ == "__main__":
    app.run(debug=True)
