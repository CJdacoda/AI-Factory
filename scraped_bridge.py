import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Bypasses browser cross-origin locks

@app.route('/ingest', methods=['POST'])
def ingest_chat_data():
    payload = request.json
    thread_text = payload.get("text", "")
    
    if thread_text:
        stream_path = "active_chat_stream.txt"
        with open(stream_path, "a", encoding="utf-8") as f:
            f.write(f"\n\n=== AUTOMATED TAMPERMONKEY INGESTION ===\n{thread_text}\n========================================")
        return jsonify({"status": "success", "message": "Thread piped to RAG stream."}), 200
    return jsonify({"status": "error", "message": "Empty data packet."}), 400

if __name__ == "__main__":
    # Runs locally on port 5000
    app.run(host='127.0.0.1', port=5000)