import os
import sys
import subprocess
import time
import requests
import psutil

API_URL = "http://127.0.0.1:5000"
DISCORD_WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL_HERE"
ROBLOX_SRC = os.path.normpath(os.path.expanduser("~/AppData/Local/Roblox"))
ROBLOX_DEST = r"D:\AI_Factory\game_offload\Roblox"

class IcarusSystemWatchdog:
    def __init__(self):
        self.ram_threshold_pct = 85.0
        print("🪐 ICARUS WATCHDOG READY // RUNNING ENVIRONMENT DIAGNOSTICS")

    def log_alert(self, msg):
        print(f"📡 [WATCHDOG]: {msg}")
        if DISCORD_WEBHOOK_URL and "YOUR_DISCORD" not in DISCORD_WEBHOOK_URL:
            try: requests.post(DISCORD_WEBHOOK_URL, json={"content": f"🚨 **Icarus Watchdog Alert:** {msg}"})
            except: pass

    def check_system_metrics(self):
        ram = psutil.virtual_memory()
        print(f"📊 Current RAM Usage: {ram.percent}% | Available: {ram.available / (1024**2):.0f}MB")
        if ram.percent > self.ram_threshold_pct:
            self.log_alert(f"High RAM Overhead Detected ({ram.percent}%). Recommending background task pruning.")
            return True
        return False

    def check_docker_status(self):
        print("🐳 Interrogating local Docker Daemon state...")
        try:
            result = subprocess.run(["docker", "info"], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print("✔ Docker Engine Status: ONLINE // READY")
                return True
        except:
            pass
        print("❌ Docker Engine Status: OFFLINE // STALLED")
        return False

    def force_roblox_offload(self):
        if os.path.exists(ROBLOX_SRC) and not os.path.islink(ROBLOX_SRC):
            print(f"🧹 Force-migrating remaining Roblox cache assets ({ROBLOX_SRC})...")
            if os.path.exists(ROBLOX_DEST):
                subprocess.run(f'rmdir /s /q "{ROBLOX_DEST}"', shell=True)
            subprocess.run(f'robocopy "{ROBLOX_SRC}" "{ROBLOX_DEST}" /E /MOVE /NFL /NDL /R:1 /W:1', shell=True)
            try: subprocess.run(f'rmdir /s /q "{ROBLOX_SRC}"', shell=True)
            except: pass
            if not os.path.exists(ROBLOX_SRC):
                subprocess.run(f'mklink /J "{ROBLOX_SRC}" "{ROBLOX_DEST}"', shell=True)
                self.log_alert("Roblox offload and junction link successfully completed.")

    def auto_git_push(self):
        print("🐙 Checking Git repository tracking status...")
        try:
            os.chdir(r"D:\AI_Factory")
            status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
            if status.stdout.strip():
                print("🔄 Uncommitted code drift located. Executing global synchronization push...")
                subprocess.run(["git", "add", "."], check=True)
                subprocess.run(["git", "commit", "-m", "Autonomous system checkpoint update via Icarus Watchdog"], check=True)
                subprocess.run(["git", "push"], check=True)
                self.log_alert("GitHub repository sync successful.")
            else:
                print("✔ Git repository status: fully synchronized.")
        except Exception as e:
            print(f"⚠️ Git tracking pass skipped or uninitialized: {str(e)}")

    def run_diagnostics_loop(self):
        print("=======================================================")
        print("🪐 ICARUS-OMNI // LIVE WATCHDOG ORCHESTRATION CYCLE")
        print("=======================================================")
        self.check_system_metrics()
        self.force_roblox_offload()
        self.auto_git_push()
        if not self.check_docker_status():
            print("🔄 Attempting to wake up background Docker environment containers...")
            if os.path.exists(r"C:\Program Files\Docker\Docker\Docker Desktop.exe"):
                os.startfile(r"C:\Program Files\Docker\Docker\Docker Desktop.exe")

if __name__ == "__main__":
    watchdog = IcarusSystemWatchdog()
    watchdog.run_diagnostics_loop()