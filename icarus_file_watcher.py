import os
import time
import json
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Target paths to intercept automated browser thread exports
WATCH_DIR = r"C:\Users\Caleb Parker\Downloads"  # Adjust user path if necessary
TARGET_EXTENSION = ".html"  # Captures standard page raw source saves

class IcarusIntelligenceHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        
        filepath = event.src_path
        if filepath.endswith(TARGET_EXTENSION):
            print(f"\n[🛰️ WATCHDOG DETECTED FLIGHT] New thread payload drop located: {os.path.basename(filepath)}")
            
            # Give the browser a split second to finish completely writing the file to disk
            time.sleep(1.5)
            
            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    raw_content = f.read()
                
                # --- 🧠 STRUCTURAL PARSING & INTELLIGENCE SORTING ENGINE ---
                char_count = len(raw_content)
                print(f"🧬 [PROCESSING STACK] Parsing thread data block ({char_count} raw characters)...")
                
                # Intelligent keyword sorting matrices
                priority_rank = 5
                awaken_trigger_notes = "Standard tracking log."
                project_domain = "General Studies // Infrastructure"
                
                if "elevenlabs" in raw_content.lower() or "audio" in raw_content.lower():
                    priority_rank = 10
                    project_domain = "AI Factory // Voice Automation Neural Network"
                    awaken_trigger_notes = "Resurface this data context immediately during the next morning briefing phase."
                elif "docker" in raw_content.lower() or "qdrant" in raw_content.lower():
                    priority_rank = 9
                    project_domain = "Cloud Security & Vector Storage Virtualization"
                    awaken_trigger_notes = "Bring this thread back up when checking system container integrity loops."
                
                print(f"📊 [SORTED ANALYSIS] Domain: {project_domain} | Priority Score: {priority_rank}/10")
                
                # Package clean structured insights for your HUD Portal Dashboard
                hud_payload = {
                    "choice": "automated_watcher_extraction",
                    "security_key": "SEC-OPERATOR-99X",
                    "payload": f"🌌 [AUTO-SORTED RAW STREAM]\nDomain Cluster: {project_domain}\nPriority Rank: {priority_rank}/10\n\nNotes:\n{awaken_trigger_notes}\n\nFile Trace Source: {os.path.basename(filepath)}"
                }
                
                # Asynchronously pass the analyzed data straight over to your local Flask API Bridge
                requests.post("http://127.0.0.1:5000/api/web_action", json=hud_payload)
                print("💾 [PIPELINE SUCCESS] Processed data matrix safely routed down to Matrix Bridge.")
                
            except Exception as e:
                print(f"❌ [WATCHDOG EXCEPTION] Critical ingestion block failed: {str(e)}")

if __name__ == "__main__":
    if not os.path.exists(WATCH_DIR):
        print(f"⚠️ Directory {WATCH_DIR} not found. Creating local playground fallback track...")
        os.makedirs(WATCH_DIR, exist_ok=True)
        
    event_handler = IcarusIntelligenceHandler()
    observer = Observer()
    observer.schedule(event_handler, path=WATCH_DIR, recursive=False)
    
    print("\n" + "="*60)
    print("🪐 ICARUS ASYNCHRONOUS WATCHDOG HARVESTER DEPLOYED")
    print(f"📁 ACTIVELY SCANNED TRACKING SUITE: {WATCH_DIR}")
    print("="*60 + "\n")
    
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()