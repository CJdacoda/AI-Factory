import os
import sys
import time
import datetime
import requests

API_URL = "http://127.0.0.1:5000"
WORKSPACE_DIR = r"D:\AI_Factory"
OUTPUT_RAG_FILE = r"D:\AI_Factory\miscellaneous_rag.txt"

class IcarusBatchSyncEngine:
    def __init__(self):
        self.seven_days_ago = time.time() - (7 * 24 * 60 * 60)

    def extract_recent_project_metadata(self):
        print("🔍 Scanning D:\\AI_Factory for past week file metadata...")
        recent_activity_logs = []
        
        if not os.path.exists(WORKSPACE_DIR):
            print("❌ Target workspace directory not found.")
            return ""

        try:
            for root, dirs, files in os.walk(WORKSPACE_DIR):
                # Skip virtual environment folders to avoid heavy noise
                if "venv" in root or ".git" in root:
                    continue
                for file in files:
                    file_path = os.path.join(root, file)
                    if os.path.exists(file_path):
                        stat = os.stat(file_path)
                        # Check if file was modified within the last 7 days
                        if stat.st_mtime > self.seven_days_ago:
                            mod_time = datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                            size_kb = stat.st_size / 1024
                            recent_activity_logs.append(f"- FILE: {file} | Path: {file_path} | Modified: {mod_time} | Size: {size_kb:.2f} KB")
        except Exception as e:
            print(f"⚠ Metadata aggregation exception: {str(e)}")

        return "\n".join(recent_activity_logs)

    def execute_batch_sync(self):
        print("=======================================================")
        print("🪐 ICARUS-OMNI // AUTOMATED METADATA BATCH SYNC ENGINE")
        print("=======================================================")
        
        # 1. Compile project metadata
        metadata_payload = self.extract_recent_project_metadata()
        
        if not metadata_payload:
            print("✔ No file metadata modifications detected in workspace paths over the last 7 days.")
            metadata_payload = "- No recent macro file alterations recorded in the 7-day lookback window."

        # 2. Package structured documentation block
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        structured_context = (
            f"\n=======================================================\n"
            f"⚡ AUTOMATED BATCH SYNC ENTRY // DATE: {timestamp}\n"
            f"=======================================================\n"
            f"METADATA AND RECENT WORKSPACE CHANGES (PAST 7 DAYS):\n"
            f"{metadata_payload}\n"
            f"=======================================================\n"
        )

        # 3. Save directly to local offline knowledge database file
        try:
            with open(OUTPUT_RAG_FILE, "a", encoding="utf-8") as f:
                f.write(structured_context)
            print(f"💾 Locally appended context blocks to: {OUTPUT_RAG_FILE}")
        except Exception as e:
            print(f"❌ Failed to commit local file update: {str(e)}")

        # 4. Transmit webhook payload directly to the running Web HUD Flask Bridge
        print("📡 Broadcasting batch vector context block down to Port 5000 Bridge...")
        webhook_data = {
            "folder_name": "AUTOMATED BATCH SYNC MATRIX",
            "full_path": OUTPUT_RAG_FILE,
            "size_gb": os.path.getsize(OUTPUT_RAG_FILE) / (1024 ** 3) if os.path.exists(OUTPUT_RAG_FILE) else 0.0
        }
        
        try:
            # We register this task to instantly trigger your visual log streams on the GUI
            requests.post(f"{API_URL}/api/webhook_register_task", json=webhook_data)
            print("🚀 SUCCESS! Batch metadata sync successfully integrated into the Icarus network.")
        except Exception:
            print("⚠️ Webhook transmission bypassed. (Ensure your Quickstart stack option 1 is running).")

if __name__ == "__main__":
    engine = IcarusBatchSyncEngine()
    engine.execute_batch_sync()