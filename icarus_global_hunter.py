import os
import sys
import shutil
import subprocess

USER_PROFILE = os.path.expanduser("~")

# Dynamic global array targeting the real storage hoarder locations on Windows
GLOBAL_HOARDER_ROOTS = [
    os.path.normpath(os.path.join(USER_PROFILE, "AppData", "Local", "Riot Games")),
    os.path.normpath(os.path.join(USER_PROFILE, "AppData", "Local", "Docker")),
    os.path.normpath(os.path.join(USER_PROFILE, "Saved Games")),
    r"C:\Riot Games",
    # Captures non-system root developer paths if any exist
    r"C:\src" 
]

# Heavy deployment, archive, and media/game engine asset extensions
HEAVY_EXTENSIONS = (".zip", ".exe", ".msi", ".pak", ".vmdk", ".iso", ".rar", ".tar", ".bkp")
SIZE_THRESHOLD_MB = 100.0  # Captures pure multi-megabyte and gigabyte weights

class IcarusGlobalHunter:
    def __init__(self):
        self.security_key = "SEC-OPERATOR-99X"
        self.destination_root = r"D:\AI_Factory\game_offload"
        os.makedirs(self.destination_root, exist_ok=True)

    def execute_global_grid_crawl(self):
        print("=======================================================")
        print("🪐 ICARUS-OMNI // SYSTEM-WIDE GLOBAL TARGET HUNTER")
        print("Scanning multi-drive hoarder paths for heavy asset nodes...")
        print("=======================================================")

        found_assets = []

        for root_path in GLOBAL_HOARDER_ROOTS:
            if not os.path.exists(root_path):
                continue
                
            print(f"📡 Scanning hoarder sector: {root_path}...")
            try:
                for root, dirs, files in os.walk(root_path):
                    for file in files:
                        if file.lower().endswith(HEAVY_EXTENSIONS) or any(ext in file.lower() for ext in [".assets", "cache"]):
                            full_path = os.path.join(root, file)
                            if os.path.exists(full_path):
                                size_mb = os.path.getsize(full_path) / (1024 * 1024)
                                if size_mb >= SIZE_THRESHOLD_MB:
                                    found_assets.append({
                                        "name": file,
                                        "path": full_path,
                                        "size": size_mb,
                                        "sector": root_path
                                    })
            except Exception as e:
                print(f" ⚠ Sector pass bypassed: {str(e)}")

        if not found_assets:
            print("\n✔ Global sweep complete. No unique unmonitored assets exceeding 100MB detected in tracking zones.")
            return

        print(f"\n⚡ Isolated {len(found_assets)} major system blocks waiting for review.\n")

        for item in found_assets:
            print("-------------------------------------------------------")
            print(f"🎯 ASSET ISOLATED : {item['name']}")
            print(f"📁 Full Path       : {item['path']}")
            print(f"📊 Storage Weight   : {item['size']:.2f} MB")
            print("-------------------------------------------------------")
            
            print("📂 Launching Windows File Explorer and spotlighting this file...")
            try:
                subprocess.run([r'explorer.exe', '/select,', item['path']])
            except Exception:
                os.startfile(os.path.dirname(item['path']))

            print("\n❓ Interactive Questionnaire Directives:")
            print("  [1] Offload and shift this asset dynamically to D: Drive workspace.")
            print("  [2] Aggressively purge and delete this asset permanently.")
            print("  [3] Skip and protect this file track.")

            choice = input("\nSelect optimization action (1/2/3): ").strip()

            if choice == "1":
                auth = input("🔒 [HITL GATE] Enter validation token key: ").strip()
                if auth == self.security_key:
                    self.offload_target_file(item['path'], item['name'])
            elif choice == "2":
                auth = input("🔒 [HITL GATE] Enter validation token key: ").strip()
                if auth == self.security_key:
                    self.purge_target_file(item['path'])
            else:
                print("Skipping node pass safely.")

    def offload_target_file(self, src_path, file_name):
        dest_path = os.path.join(self.destination_root, file_name)
        print(f"📦 Transferring target package to: {dest_path}...")
        try:
            if os.path.exists(dest_path):
                os.remove(dest_path)
            shutil.move(src_path, dest_path)
            print("✔ Offload complete! Space recovered on C: drive.")
        except Exception as e:
            print(f"❌ System block: File is currently locked or in use by another task. {str(e)}")

    def purge_target_file(self, src_path):
        print(f"💥 Permanent deletion executed over: {src_path}...")
        try:
            os.remove(src_path)
            print("✔ Asset destroyed safely.")
        except Exception as e:
            print(f"❌ Deletion failed: {str(e)}")

if __name__ == "__main__":
    hunter = IcarusGlobalHunter()
    hunter.execute_global_grid_crawl()