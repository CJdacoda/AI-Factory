import os
from flask import Flask, request, jsonify
from flask_cors import CORS  

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  

# Create a local directory for captured data dumps if it doesn't exist
DUMP_DIR = r"D:\AI_Factory\captured_intelligence"
os.makedirs(DUMP_DIR, exist_ok=True)

# Local state tracking variables for active terminal operations
pending_questionnaire = {
    "active": False,
    "folder_name": "",
    "full_path": "",
    "size_gb": 0.0,
    "user_choice": None
}

@app.route('/api/status', methods=['GET'])
def get_system_status():
    """Your HTML dashboard calls this on a loop to check for real-time terminal tasks."""
    return jsonify({
        "status": "ONLINE",
        "bridge_pid": os.getpid(),
        "task_pending": pending_questionnaire
    })

@app.route('/api/webhook_register_task', methods=['POST'])
def register_task_webhook():
    """Terminal scripts hit this webhook to send a folder to your web browser."""
    global pending_questionnaire
    data = request.json
    pending_questionnaire = {
        "active": True,
        "folder_name": data.get("folder_name"),
        "full_path": data.get("full_path"),
        "size_gb": data.get("size_gb"),
        "user_choice": None
    }
    return jsonify({"status": "SUCCESS", "message": "Task piped to Web HUD"})

@app.route('/api/web_action', methods=['POST'])
def web_action_receiver():
    """Triggered when you click the 🪐 SYNC TO ICARUS button in your browser."""
    global pending_questionnaire
    data = request.json or {}
    choice = data.get("choice")
    auth_key = data.get("security_key")
    payload = data.get("payload", "")
    
    if auth_key != "SEC-OPERATOR-99X":
        print("⚠️ UNAUTHORIZED PACKET DROPPED: Invalid Token")
        return jsonify({"status": "DENIED", "message": "Invalid Security Key Token"})
        
    # --- 🌌 DATA INTERCEPTION LAYER ---
    if payload:
        print(f"\n[📡 ICARUS INCOMING STACK] Intercepted payload payload block! ({len(payload)} chars)")
        
        # Save the captured conversation cleanly to a local file
        filename = os.path.join(DUMP_DIR, "synced_intelligence_log.txt")
        try:
            with open(filename, "a", encoding="utf-8") as f:
                f.write("\n\n=========================================\n")
                f.write(f"🛰️ SYNCHRONIZED CAPTURE PASS\n")
                f.write("=========================================\n")
                f.write(payload)
            print(f"💾 SUCCESSFULLY SERIALIZED: Appended to {filename}")
        except Exception as e:
            print(f"❌ LOG SERIALIZATION FAILURE: {str(e)}")
    # ----------------------------------
        
    pending_questionnaire["user_choice"] = choice
    pending_questionnaire["active"] = False  # Clear the task block once resolved
    return jsonify({"status": "AUTHORIZED", "message": f"Action {choice} queued and data serialized safely."})

@app.route('/api/webhook_poll_choice', methods=['GET'])
def poll_choice_webhook():
    """Terminal scripts call this to wait until you click a button on the website."""
    global pending_questionnaire
    return jsonify({"user_choice": pending_questionnaire["user_choice"]})

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🛰️ ICARUS REAL-TIME WEBHOOK APPARATUS INITIALIZED")
    print(f"📁 INTELLIGENCE REPOSITORY LOCATION: {DUMP_DIR}")
    print("="*50 + "\n")
    app.run(host='127.0.0.1', port=5000, debug=False)