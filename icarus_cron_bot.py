import os
import subprocess
import win32com.client  # Run 'pip install pywin32' inside your environment

def execute_audio_alert(message):
    """Uses internal low-latency Windows SAPI speech to give Cron Bot a clean vocal interface."""
    try:
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        speaker.Speak(message)
    except Exception:
        pass

def manage_storage_allocations():
    """Enforces absolute deployment priority onto storage node D: instead of drive C:"""
    target_drive = "D:\\"
    if os.path.exists(target_drive):
        # Enforce destination directory parameters for download dumps
        os.makedirs("D:\\AI_Factory\\download_dumps", exist_ok=True)
        return "D:\\AI_Factory\\download_dumps"
    return ".\\download_dumps"

def run_automated_pipeline():
    execute_audio_alert("Icarus Cron Bot initializing scheduled background operations block.")
    
    target_path = manage_storage_allocations()
    python_executable = os.path.join("venv", "Scripts", "python.exe")
    
    try:
        execute_audio_alert("Prioritizing storage node D for automated downloads. Initiating high-speed workspace radar.")
        subprocess.run([python_executable, "smart_cleaner.py"], check=True)
        execute_audio_alert("Background directory optimization parameters successfully updated.")
    except Exception as e:
        execute_audio_alert("Scheduled operational sequence encountered an execution exception.")

if __name__ == "__main__":
    run_automated_pipeline()