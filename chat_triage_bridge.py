from flask import Flask, request, jsonify
from flask_cors import CORS  # <-- Make sure this line is here!

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # <-- This completely destroys the "Link Disconnected" bug!

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
    """Triggered when you click an animated button inside your HTML website layout."""
    global pending_questionnaire
    data = request.json
    choice = data.get("choice")
    auth_key = data.get("security_key")
    
    if auth_key != "SEC-OPERATOR-99X":
        return jsonify({"status": "DENIED", "message": "Invalid Security Key Token"})
        
    pending_questionnaire["user_choice"] = choice
    pending_questionnaire["active"] = False  # Clear the task block once resolved
    return jsonify({"status": "AUTHORIZED", "message": f"Action {choice} queued for terminal deployment"})

@app.route('/api/webhook_poll_choice', methods=['GET'])
def poll_choice_webhook():
    """Terminal scripts call this to wait until you click a button on the website."""
    global pending_questionnaire
    return jsonify({"user_choice": pending_questionnaire["user_choice"]})

if __name__ == '__main__':
    print("🛰️ ICARUS REAL-TIME WEBHOOK APPARATUS INITIALIZED")
    app.run(host='127.0.0.1', port=5000, debug=False)