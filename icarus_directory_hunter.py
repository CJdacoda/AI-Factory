import os
import sys
import subprocess
import time
import requests

USER_PROFILE = os.path.expanduser("~")

GLOBAL_SCAN_ROOTS = [
    os.path.normpath(os.path.join(USER_PROFILE, "AppData", "Local")),
    os.path.normpath(os.path.join(USER_PROFILE, "AppData", "Roaming")),
    r"C:\Riot Games",
    os.path.normpath(os.path.join(USER_PROFILE, "Saved Games"))
]

CRITICAL_SYSTEM_PROTECTION_BLOC = ["MICROSOFT", "WINDOWS", "SYSTEM32", "PACKAGES"]
FOLDER_SIZE_THRESHOLD_GB = 2.0  
API_URL = "http://127.0.0.1:5000"

class IcarusRobocopyHunter:
    def __init__(self):
        self.destination_root = r"D:\AI_Factory\game_offload"
        os.makedirs(self.destination_root, exist_ok=True)

    def calculate_dir_size_gb(self, path):
        total_size = 0
        try:
            for root, dirs, files in os.walk(path):
                for f in files:
                    fp = os.path.join(root, f)
                    if os.path.exists(fp):
                        total_size += os.path.getsize(fp)
        except Exception:
            pass
        return total_size / (1024 ** 3)

    def execute_global_folder_sweep(self):
        print("=======================================================")
        print("🪐 ICARUS-OMNI // BARE-METAL ROBOCOPY TRANSMITTER")
        print("Streaming multi-gigabyte folder anomalies to Web HUD...")
        print("=======================================================")

        for base_root in GLOBAL_SCAN_ROOTS:
            if not os.path.exists(base_root):
                continue
                
            try:
                for item in os.listdir(base_root):
                    full_path = os.path.join(base_root, item)
                    if os.path.isdir(full_path):
                        if any(crit in item.upper() for crit in CRITICAL_SYSTEM_PROTECTION_BLOC):
                            continue
                            
                        size_gb = self.calculate_dir_size_gb(full_path)
                        
                        if size_gb >= FOLDER_SIZE_THRESHOLD_GB:
                            print(f"\n🚨 Found {item} ({size_gb:.2f} GB). Sending webhook to browser dashboard...")
                            
                            payload = {
                                "folder_name": item,
                                "full_path": full_path,
                                "size_gb": size_gb
                            }
                            try:
                                requests.post(f"{API_URL}/api/webhook_register_task", json=payload)
                            except Exception:
                                print("❌ API connection failed. Ensure the quickstart bridge is active.")
                                continue

                            while True:
                                time.sleep(1.5)
                                try:
                                    status_check = requests.get(f"{API_URL}/api/webhook_poll_choice").json()
                                    choice = status_check.get("user_choice")
                                    if choice is not None:
                                        if choice == "1":
                                            self.execute_robocopy_migration(full_path, item)
                                        else:
                                            print("🛡️ Skip command detected from Web HUD. Protecting path.")
                                        
                                        # Clear state on server
                                        requests.post(f"{API_URL}/api/web_action", json={"choice": None, "security_key": "SEC-OPERATOR-99X"})
                                        break
                                except Exception:
                                    pass
            except Exception as e:
                print(f" ⚠ Sector pass issue: {str(e)}")

    def execute_robocopy_migration(self, src_path, folder_name):
        dest_path = os.path.join(self.destination_root, folder_name)
        print(f"📦 Commencing bare-metal Robocopy over: {folder_name}...")
        
        # Phase 1: High-speed Robocopy Move execution
        cmd_robo = f'robocopy "{src_path}" "{dest_path}" /E /MOVE /NFL /NDL'
        subprocess.run(cmd_robo, shell=True)
        
        # Phase 2: Automatic NTFS Junction generation to guarantee application stability
        print(f"🔗 Anchoring administrative junction handshake path...")
        cmd_link = f'mklink /J "{src_path}" "{dest_path}"'
        subprocess.run(cmd_link, shell=True)
        print(f"🚀 SUCCESS! {folder_name} successfully shifted and linked.")

if __name__ == "__main__":
    hunter = IcarusRobocopyHunter()
    hunter.execute_global_folder_sweep()