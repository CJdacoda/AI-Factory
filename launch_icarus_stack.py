import os
import subprocess
import sys
import time
import webbrowser

def launch_complete_stack():
    print("🪐 INITIALIZING ICARUS FACTORY PLATFORM STACK...")
    print("=======================================================")
    
    # 1. Establish absolute pathing to the active directory structure
    base_dir = os.path.dirname(os.path.abspath(__file__))
    venv_python = os.path.join(base_dir, "venv", "Scripts", "python.exe")
    
    if not os.path.exists(venv_python):
        print(f"❌ Error: Virtual environment python.exe not found at {venv_python}")
        print("Please verify your venv folder exists in this directory.")
        sys.exit(1)

    # 2. Spin up the Qdrant Vector DB container via Docker
    print("🐳 Step 1: Booting local Qdrant Vector Core Engine...")
    try:
        # Run docker-compose explicitly from the project root directory
        subprocess.run(["docker-compose", "up", "-d"], cwd=base_dir, check=True)
        print("✔ Qdrant Core container is verified and online.")
    except Exception as e:
        print(f"⚠️ Warning: Could not auto-start Docker container: {e}")

    # 3. Handle Windows console flags safely across CMD/PowerShell/Runtimes
    creation_flag = 0
    if sys.platform == "win32":
        # Force a fresh console window to isolate background loops cleanly
        creation_flag = subprocess.CREATE_NEW_CONSOLE

    # 4. Spin up the Icarus System Watchdog
    print("🐙 Step 2: Launching Icarus Orchestration Watchdog...")
    watchdog_script = os.path.join(base_dir, "icarus_watchdog.py")
    subprocess.Popen(
        [venv_python, watchdog_script],
        cwd=base_dir,
        creationflags=creation_flag
    )
    time.sleep(2)  # Secure binding window to prevent parameter collisons

    # 5. Spin up the Chat Triage Bridge API server (chat_triage_bridge.py)
    print("📡 Step 3: Launching Real-Time Webhook Triage Bridge...")
    bridge_script = os.path.join(base_dir, "chat_triage_bridge.py")
    subprocess.Popen(
        [venv_python, bridge_script],
        cwd=base_dir,
        creationflags=creation_flag
    )
    time.sleep(2)

    # 6. Automatically open the Front-End Control Dashboard
    gui_path = os.path.join(base_dir, "revenant_gui.html")
    print(f"🖥️ Step 4: Spawning Command Center Control HUD: file:///{gui_path}")
    webbrowser.open(f"file:///{gui_path}")
    
    print("\n=======================================================")
    print("🚀 ICARUS MASTER STACK IS RUNNING LIVE IN THE BACKGROUND")
    print("Close the individual terminal consoles to spin down modules.")

if __name__ == "__main__":
    launch_complete_stack()
