import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

DUMP_DIR = r"D:\AI_Factory\captured_intelligence"
os.makedirs(DUMP_DIR, exist_ok=True)

# Central Memory Matrices
latest_triage_payload = "Awaiting synchronized automated data stream..."
pending_questionnaire = {
    "active": False,
    "project_context": "None",
    "suggested_actions": [],
    "file_vector_status": "PENDING"
}

@app.route('/api/status', methods=['GET'])
def get_system_status():
    global latest_triage_payload, pending_questionnaire
    return jsonify({
        "status": "ONLINE",
        "bridge_pid": os.getpid(),
        "task_pending": pending_questionnaire,
        "latest_triage": latest_triage_payload
    })

@app.route('/api/web_action', methods=['POST'])
def web_action_receiver():
    global pending_questionnaire, latest_triage_payload
    data = request.json or {}
    choice = data.get("choice")
    auth_key = data.get("security_key")
    payload = data.get("payload", "")
    
    if auth_key != "SEC-OPERATOR-99X":
        return jsonify({"status": "DENIED", "message": "Invalid Token Matrix"})
        
    # Manual Input / Ingestion Processing Lane
    if choice == "manual_inject" or payload:
        print(f"\n[📡 ICARUS INGESTION] Processing raw text thread packet ({len(payload)} characters)...")
        
        # Capture the FULL string for the dashboard viewport safely without truncation
        latest_triage_payload = payload
        
        # Auto-Organization & Serialization Layer
        filename = os.path.join(DUMP_DIR, "synced_intelligence_log.txt")
        try:
            with open(filename, "a", encoding="utf-8") as f:
                f.write(f"\n\n=== LOG SEGMENT INITIALIZED: {len(payload)} CHARS ===\n{payload}")
            
            # --- AUTOMATED QUESTIONNAIRE LOGIC ENGINE ---
            # Simulate tactical sorting of project requirements from the thread text
            if "venv" in payload.lower() or "script" in payload.lower():
                pending_questionnaire = {
                    "active": True,
                    "project_context": "Environment Architecture & Script Deployment Diagnostics",
                    "suggested_actions": [
                        "Optimize Tampermonkey Match Vectors",
                        "Build Automated Thread Zipping Engine Wrapper",
                        "Establish Local Qdrant Core Vector Storage Ingestion"
                    ],
                    "file_vector_status": "READY TO INDEX"
                }
        except Exception as e:
            print(f"❌ File serialization exception: {str(e)}")
            
    if choice in ["0", "1", "2"]:
        print(f"🎮 [HUD INPUT REGISTERED] Operator deployed path choice: {choice}")
        pending_questionnaire["active"] = False  # Clear task block once resolved
        
    return jsonify({"status": "AUTHORIZED", "message": "Data stream successfully routed and parsed."})

if __name__ == '__main__':
    print(f"🛰️ ICARUS INTELLIGENCE SYSTEM RUNNING AT PORT 5000")
    app.run(host='127.0.0.1', port=5000, debug=False)