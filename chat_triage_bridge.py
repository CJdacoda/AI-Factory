import os
import json
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

DUMP_DIR = r"D:\AI_Factory\captured_intelligence"
os.makedirs(DUMP_DIR, exist_ok=True)

# 📡 DISCORD MOBILE TRIAGE CONFIGURATION
# Paste your unique Discord Webhook URL between the quotes below:
DISCORD_WEBHOOK_URL = "PASTE_YOUR_COPIED_DISCORD_WEBHOOK_URL_HERE"

# Central Memory Matrices
latest_triage_payload = "Awaiting synchronized automated data stream..."
pending_questionnaire = {
    "active": False,
    "project_context": "None",
    "suggested_actions": [],
    "file_vector_status": "PENDING"
}

def dispatch_mobile_alert(project_domain, priority, file_source):
    """Broadcasts real-time priority signals directly to your mobile device."""
    if DISCORD_WEBHOOK_URL == "PASTE_YOUR_COPIED_DISCORD_WEBHOOK_URL_HERE" or not DISCORD_WEBHOOK_URL:
        print("⚠️ [DISCORD STANDBY] Webhook URL not set. Skipping mobile alert push.")
        return

    payload = {
        "content": "🪐 **ICARUS REVENANT MATRIX ALERT // MOVEMENT DETECTED**",
        "embeds": [{
            "title": f"🚨 High Priority Ingestion Queued ({priority}/10)",
            "color": 12352351,  # Purple matrix theme glow
            "fields": [
                {"name": "📁 Target Domain", "value": project_domain, "inline": True},
                {"name": "📄 Source Origin", "value": file_source, "inline": True},
                {"name": "⚡ Phone Intercept State", "value": "Awaiting Operator confirmation pass via HUD platform.", "inline": False}
            ],
            "footer": {"text": "Icarus Factory Automated Systems Engine"}
        }]
    }
    
    try:
        requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=5)
        print("📱 [MOBILE DISPATCH] Real-time triage metrics broadcasted to Discord portal.")
    except Exception as e:
        print(f"❌ Mobile dispatch communication link failed: {str(e)}")

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
        
    # Manual Input / Ingestion Processing Lane from Watchdog or Browser
    if choice == "automated_watcher_extraction" or payload:
        print(f"\n[📡 ICARUS INGESTION] Processing raw text thread packet ({len(payload)} characters)...")
        
        # Capture the full string for the dashboard viewport safely
        latest_triage_payload = payload
        
        # Setup defaults for intelligence analysis
        priority_rank = 5
        project_domain = "General Studies // Infrastructure"
        file_source_name = "Tampermonkey_Manual_Snipe.txt"
        
        # If incoming from watchdog, we parse out our custom tags
        if "File Trace Source:" in payload:
            for line in payload.split("\n"):
                if "Domain Cluster:" in line: project_domain = line.replace("Domain Cluster:", "").strip()
                if "Priority Rank:" in line: 
                    try: priority_rank = int(line.replace("Priority Rank:", "").split("/")[0].strip())
                    except: pass
                if "File Trace Source:" in line: file_source_name = line.replace("File Trace Source:", "").strip()

        # Auto-Organization & Serialization Layer
        filename = os.path.join(DUMP_DIR, "synced_intelligence_log.txt")
        try:
            with open(filename, "a", encoding="utf-8") as f:
                f.write(f"\n\n=== LOG SEGMENT INITIALIZED: {len(payload)} CHARS ===\n{payload}")
            
            # --- AUTOMATED QUESTIONNAIRE LOGIC ENGINE ---
            if "venv" in payload.lower() or "script" in payload.lower() or "elevenlabs" in payload.lower():
                pending_questionnaire = {
                    "active": True,
                    "project_context": project_domain,
                    "suggested_actions": [
                        "Optimize Watchdog Directory Watchers",
                        "Sync ElevenLabs Audio Briefing Loops",
                        "Engage Local Qdrant Core Storage Indexes"
                    ],
                    "file_vector_status": "READY TO INDEX"
                }
                
                # 🔥 DISPATCH AUTOMATED ALERT STRAIGHT TO YOUR PHONE VIA DISCORD
                dispatch_mobile_alert(project_domain, priority_rank, file_source_name)
                
        except Exception as e:
            print(f"❌ File serialization exception: {str(e)}")
            
    if choice in ["0", "1", "2"]:
        print(f"🎮 [HUD INPUT REGISTERED] Operator deployed path choice: {choice}")
        pending_questionnaire["active"] = False  # Clear task block once resolved
        
    return jsonify({"status": "AUTHORIZED", "message": "Data stream successfully routed and parsed."})

if __name__ == '__main__':
    print(f"\n" + "="*50)
    print(f"🛰️ ICARUS REAL-TIME WEBHOOK APPARATUS INITIALIZED")
    print(f"📁 REPOSITORY LOG TARGET: {DUMP_DIR}")
    print("="*50 + "\n")
    app.run(host='127.0.0.1', port=5000, debug=False)