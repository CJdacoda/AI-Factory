import os
import sys
import shutil
import subprocess

# Global Configuration Tiers
USER_PROFILE = os.path.expanduser("~")
SCAN_TARGET = os.path.normpath(os.path.join(USER_PROFILE, "Downloads"))
DESTINATION_ROOT = r"D:\AI_Factory\game_offload"

# Target heavy installer and archive files that clutter C drive space
HEAVY_EXTENSIONS = (".zip", ".exe", ".msi", ".rar", ".7z", ".tar.gz", ".iso")
SIZE_THRESHOLD_MB = 50.0  # Dropped threshold so it actively finds optimization targets

class IcarusDeepHunter:
    def __init__(self):
        self.security_key = "SEC-OPERATOR-99X"
        os.makedirs(DESTINATION_ROOT, exist_ok=True)

    def execute_deep_crawl(self):
        print("=======================================================")
        print("🪐 ICARUS-OMNI // RECURSIVE DEEP FILE HUNTER & ROUTER")
        print(f"Scanning target path: {SCAN_TARGET} for files > {SIZE_THRESHOLD_MB}MB...")
        print("=======================================================")

        found_files = []

        # Walk recursively through all subdirectories inside your target path
        try:
            for root, dirs, files in os.walk(SCAN_TARGET):
                for file in files:
                    if file.lower().endswith(HEAVY_EXTENSIONS):
                        full_path = os.path.join(root, file)
                        if os.path.exists(full_path):
                            size_mb = os.path.getsize(full_path) / (1024 * 1024)
                            if size_mb >= SIZE_THRESHOLD_MB:
                                found_files.append({"name": file, "path": full_path, "size": size_mb})
        except Exception as e:
            print(f"❌ Scan interrupted: {str(e)}")

        if not found_files:
            print(f"✔ Scan complete. No unique heavy installer assets exceeding {SIZE_THRESHOLD_MB}MB located.")
            return

        print(f"⚡ Isolated {len(found_files)} heavy assets waiting for optimization review.\n")

        for item in found_files:
            print("-------------------------------------------------------")
            print(f"🎯 FILE IDENTIFIED: {item['name']}")
            print(f"📁 Source Location : {item['path']}")
            print(f"📊 Storage Weight  : {item['size']:.2f} MB")
            print("-------------------------------------------------------")
            
            # AUTOMATION LINK: Highlight the exact file visually inside its directory
            print("📂 Popping open Windows File Explorer to spotlight this specific file...")
            try:
                # Opens file explorer with the specific file pre-selected
                subprocess.run([r'explorer.exe', '/select,', item['path']])
            except Exception:
                os.startfile(os.path.dirname(item['path']))

            print("\n❓ Interactive Questionnaire Directives:")
            print("  [1] Offload and safely shift this specific file weight to your D: drive storage.")
            print("  [2] Aggressively purge and permanently delete this asset from C: drive.")
            print("  [3] Skip and protect this file.")

            choice = input("\nSelect optimization action (1/2/3): ").strip()

            if choice == "1":
                auth = input("🔒 [HITL GATE] Enter security token key: ").strip()
                if auth == self.security_key:
                    self.offload_file(item['path'], item['name'])
            elif choice == "2":
                auth = input("🔒 [HITL GATE] Enter security token key: ").strip()
                if auth == self.security_key:
                    self.purge_file(item['path'])
            else:
                print("Skipping asset file track cleanly.")

    def offload_file(self, src_path, file_name):
        dest_path = os.path.join(DESTINATION_ROOT, file_name)
        print(f"📦 Transferring file package to: {dest_path}...")
        try:
            if os.path.exists(dest_path):
                os.remove(dest_path)
            shutil.move(src_path, dest_path)
            print("✔ Offload migration complete! C: partition space reclaimed.")
        except Exception as e:
            print(f"❌ System block: File is actively being read by another app. {str(e)}")

    def purge_file(self, src_path):
        print(f"💥 Vaporizing asset completely from disk sectors: {src_path}...")
        try:
            os.remove(src_path)
            print("✔ File destroyed cleanly.")
        except Exception as e:
            print(f"❌ Deletion failed: {str(e)}")

if __name__ == "__main__":
    hunter = IcarusDeepHunter()
    hunter.execute_deep_crawl()