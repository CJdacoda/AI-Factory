import os
import sys
import shutil
import subprocess

class IcarusTurboOffloader:
    def __init__(self):
        self.security_key = "SEC-OPERATOR-99X"
        # Targets your heaviest personal user data folders
        self.scan_paths = [
            os.path.expandvars(r"%USERPROFILE%\Downloads"),
            os.path.expandvars(r"%USERPROFILE%\Documents"),
            os.path.expandvars(r"%LOCALAPPDATA%\Docker")
        ]
        self.destination_root = r"D:\AI_Factory\game_offload"
        os.makedirs(self.destination_root, exist_ok=True)

    def execute_turbo_sweep(self):
        print("=======================================================")
        print("🚀 ICARUS-OMNI // TURBO DYNAMIC STORAGE OFFLOADER")
        print("Scanning user directories for immediate multi-gigabyte recovery...")
        print("=======================================================")

        for path in self.scan_paths:
            if not os.path.exists(path):
                continue

            # Calculate directory size
            total_size = 0
            try:
                for dirpath, dirnames, filenames in os.walk(path):
                    for f in filenames:
                        fp = os.path.join(dirpath, f)
                        if os.path.exists(fp):
                            total_size += os.path.getsize(fp)
                size_gb = total_size / (1024 ** 3)
            except Exception:
                size_gb = 0.0

            # Isolate folders choking your SSD (greater than 1.0 GB)
            if size_gb >= 1.0:
                print(f"\n🚨 [HEAVY BLOCK DETECTED]: {path} is holding {size_gb:.2f} GB!")
                print(f"📂 Launching Windows File Explorer window for visual confirmation...")
                
                try:
                    os.startfile(path)
                except Exception:
                    subprocess.run(['explorer', path])

                print("\n🛰️ Dynamic Action Questionnaire:")
                print("  [1] Automatically OFFLOAD and shift this entire directory weight to D: Drive.")
                print("  [2] Skip this folder path safely.")
                
                choice = input("\nSelect execution choice (1/2): ").strip()

                if choice == "1":
                    auth = input("🔒 [HITL GATE] Enter security token key: ").strip()
                    if auth == self.security_key:
                        self.migrate_directory(path)
                    else:
                        print("❌ Invalid token. Shift aborted.")
                else:
                    print("Skipping directory tree node.")

    def migrate_directory(self, src_path):
        folder_name = os.path.basename(src_path)
        dest_path = os.path.join(self.destination_root, folder_name)
        print(f"📦 Shifting files from C: to {dest_path}...")
        
        try:
            # Create subfolder on D drive if it doesn't exist
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)

            # Iteratively move files to handle active locks gracefully
            for item in os.listdir(src_path):
                s_item = os.path.join(src_path, item)
                d_item = os.path.join(dest_path, item)
                try:
                    if os.path.exists(d_item):
                        if os.path.isdir(d_item):
                            shutil.rmtree(d_item)
                        else:
                            os.remove(d_item)
                    shutil.move(s_item, d_item)
                    print(f" ✔ Shifted: {item}")
                except Exception:
                    # Skips locked files silently instead of crashing the automation tool
                    pass
            print("🚀 Offload sequence executed over unlocked assets. C: space recovered!")
        except Exception as e:
            print(f"❌ Structural bottleneck encountered: {str(e)}")

if __name__ == "__main__":
    offloader = IcarusTurboOffloader()
    offloader.execute_turbo_sweep()