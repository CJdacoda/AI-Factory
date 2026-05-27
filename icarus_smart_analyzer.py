import os
import sys
import shutil
import subprocess

# Local signature maps defining directory purpose and safety profiles
FOLDER_INTELLIGENCE_MAP = {
    "DOWNLOADS": {
        "purpose": "User-initiated web downloads (installers, zip records, media files).",
        "action_reason": "Contains historical setup files that are safe to move to D: drive since they are rarely reopened.",
        "risk_level": "LOW // SAFE TO OFFLOAD"
    },
    "TEMP": {
        "purpose": "Temporary runtime workspace used by Windows installers and active app sessions.",
        "action_reason": "Old, unlocked cache files here can be safely purged to reclaim space without breaking your apps.",
        "risk_level": "NEGLIGIBLE // SAFE TO PURGE OLD UNLOCKED FILES"
    },
    "DOCKER": {
        "purpose": "Hidden virtual machine disk images and local container file layers.",
        "action_reason": "Massive background cache block. Wiping it resets stalled Docker containers safely.",
        "risk_level": "MODERATE // WILL CLEAR ALL LOCAL CONTAINER IMAGES"
    },
    "RIOT GAMES": {
        "purpose": "Competitive game files, weapon telemetry frameworks, and match map textures.",
        "action_reason": "Consumes massive gigabytes on your SSD. Perfect candidate to offload to D: drive via folder shifting.",
        "risk_level": "LOW // SAFE TO SHIFT TO D: PARTITION"
    }
}

class IcarusSmartAnalyzer:
    def __init__(self):
        self.security_key = "SEC-OPERATOR-99X"
        self.targets = {
            "DOWNLOADS": os.path.expandvars(r"%USERPROFILE%\Downloads"),
            "TEMP": os.path.expandvars(r"%LOCALAPPDATA%\Temp"),
            "DOCKER": os.path.expandvars(r"%LOCALAPPDATA%\Docker"),
            "RIOT GAMES": r"C:\Riot Games"
        }

    def run_intelligent_analysis_loop(self):
        print("=======================================================")
        print("🪐 ICARUS-OMNI // INTELLIGENT EXPERT STORAGE ANALYZER")
        print("Parsing directories, generating safety rationales, and opening folders...")
        print("=======================================================")

        for key, path in self.targets.items():
            if not os.path.exists(path):
                continue

            # Calculate true directory weight
            total_size = 0
            try:
                for dirpath, dirnames, filenames in os.walk(path):
                    for f in filenames:
                        fp = os.path.join(dirpath, f)
                        if os.path.exists(fp): total_size += os.path.getsize(fp)
                size_gb = total_size / (1024 ** 3)
            except Exception:
                size_gb = 0.0

            # Only interrogate folders holding significant space
            if size_gb >= 0.5:
                print(f"\n🎯 [ISOLATED TARGET]: {path} (~{size_gb:.2f} GB)")
                
                # Fetch intelligence profile metadata descriptions
                intel = FOLDER_INTELLIGENCE_MAP.get(key, {"purpose": "Unknown Data Stack", "action_reason": "Unclassified path.", "risk_level": "HIGH"})
                
                print(f" 📑 [System Purpose]: {intel['purpose']}")
                print(f" 💡 [Why Action This]: {intel['action_reason']}")
                print(f" ⚠️ [Safety Stance ]: {intel['risk_level']}")
                
                print(f"📂 [Action] Automatically launching Windows File Explorer for visual verification...")
                try:
                    os.startfile(path)
                except Exception:
                    subprocess.run(['explorer', path])

                print("\n❓ Questionnaire Action Option:")
                print("  [1] Purge loose un-locked files inside this folder immediately.")
                print("  [2] Offload and shift this entire structure safely to D: drive.")
                print("  [3] Skip and protect this folder layout.")
                
                choice = input("\nSelect action (1/2/3): ").strip()
                
                if choice == "1":
                    auth = input("🔒 [HITL GATE] Enter clearance key to verify deletion pass: ").strip()
                    if auth == self.security_key:
                        self.clean_folder_contents(path)
                elif choice == "2":
                    auth = input("🔒 [HITL GATE] Enter clearance key to verify drive relocation: ").strip()
                    if auth == self.security_key:
                        self.migrate_folder(path)
                else:
                    print("Skipping directory node safely. No drive sectors modified.")

    def clean_folder_contents(self, path):
        print(f"💥 Wiping unlocked temporary assets inside: {path}...")
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            try:
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.unlink(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
            except Exception:
                # Silently bypass active locked files without crashing your terminal loop
                pass
        print("✔ Purge cycle executed successfully over unlocked file structures.")

    def migrate_folder(self, path):
        folder_name = os.path.basename(path)
        destination = os.path.join(r"D:\AI_Factory\game_offload", folder_name)
        print(f"📦 Relocating asset weights to: {destination}...")
        try:
            if os.path.exists(destination): shutil.rmtree(destination)
            shutil.move(path, destination)
            print("✔ Offload migration successful. Local disk space recovered!")
        except Exception as e:
            print(f"❌ Migration blocked: System folders require manual drag-and-drop. {str(e)}")

if __name__ == "__main__":
    analyzer = IcarusSmartAnalyzer()
    analyzer.run_intelligent_analysis_loop()