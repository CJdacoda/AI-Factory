import os
import sys
import shutil
import subprocess

# Try to look for Rich for beautiful text formatting, fallback to plain print if missing
try:
    from rich.console import Console
    from rich.panel import Panel
    console = Console()
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

# SAFE GATE: Built-in local fallback to bypass a missing icarus_logger module
try:
    from icarus_logger import log_action
except ImportError:
    def log_action(module, action, message, status="SUCCESS"):
        if not HAS_RICH:
            print(f"[{module.upper()}] {action}: {message}")
        pass

# High-yield targets to investigate for massive gigabyte hoarding on C drive
TARGETS_TO_SCAN = [
    os.path.expandvars(r"%USERPROFILE%\Downloads"),
    os.path.expandvars(r"%LOCALAPPDATA%\Temp"),
    os.path.expandvars(r"%LOCALAPPDATA%\Docker"),
    r"C:\Riot Games",
    os.path.expandvars(r"%USERPROFILE%\.config")
]

class IcarusStorageInterrogator:
    def __init__(self):
        self.security_key = "SEC-OPERATOR-99X"

    def get_folder_size_gb(self, path):
        """Calculates the true storage weight of a folder on disk."""
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    if os.path.exists(fp):
                        total_size += os.path.getsize(fp)
            return total_size / (1024 ** 3)
        except Exception:
            return 0.0

    def begin_interrogation_loop(self):
        title = "☠️ ICARUS-OMNI // INTERACTIVE FILE EXPLORER INTERROGATOR"
        subtitle = "Isolating multi-gigabyte targets & launching Windows File Explorer links..."
        
        if HAS_RICH:
            console.print("[bold bright_black]=======================================================[/bold bright_black]")
            console.print(Panel(subtitle, title=title, border_style="red"))
        else:
            print(f"=== {title} ===")
            print(subtitle)

        found_bloat = False

        for target in TARGETS_TO_SCAN:
            if not os.path.exists(target):
                continue
                
            size_gb = self.get_folder_size_gb(target)
            
            # Focus exclusively on high-impact blocks consuming more than 1.0 GB
            if size_gb >= 1.0:
                found_bloat = True
                
                if HAS_RICH:
                    console.print(f"\n[bold yellow]🎯 TARGET ISOLATED:[/bold yellow] [white]{target}[/white] is holding [bold red]{size_gb:.2f} GB[/bold red]")
                else:
                    print(f"\n🎯 TARGET ISOLATED: {target} is holding {size_gb:.2f} GB")

                # AUTOMATION HOOK: Forcefully pop open Windows File Explorer for visual verification
                print(f"📂 [Icarus Action] Launching Windows File Explorer window for: {target}...")
                try:
                    os.startfile(target)
                except Exception:
                    # Fallback method if host permissions restrict direct startfile hooks
                    subprocess.run(['explorer', target])
                    
                print("\n❓ Question: Review the popped-up folder window. How do you want to handle this block?")
                print("  [1] Aggressively PURGE and permanently delete this folder from C: drive.")
                print("  [2] OFFLOAD and shift this entire directory to your D: Drive partition.")
                print("  [3] SKIP and protect this folder.")
                
                choice = input("\nSelect action input option (1/2/3): ").strip()
                
                if choice == "1":
                    auth = input(f"🔒 [SECURITY GATE] Enter key to authorize permanent deletion: ").strip()
                    if auth == self.security_key:
                        self.purge_directory(target)
                    else:
                        print("⚠ Invalid security token. Purge skipped.")
                        
                elif choice == "2":
                    auth = input(f"🔒 [SECURITY GATE] Enter key to authorize drive relocation: ").strip()
                    if auth == self.security_key:
                        self.offload_directory(target)
                    else:
                        print("⚠ Invalid security token. Offload skipped.")
                else:
                    print("Skipping target path layout. Moving to next array node...")

        if not found_bloat:
            print("✔ No unmonitored target folders exceeding 1.0 GB detected in primary scan paths.")

    def purge_directory(self, path):
        try:
            print(f"💥 Executing total system wipe on: {path}...")
            shutil.rmtree(path)
            print("✔ Target destroyed cleanly.")
            log_action("interrogator", "MANUAL_PURGE", f"Permanently deleted locked target path: {path}")
        except Exception as e:
            print(f"❌ System block encountered: Partial deletion only. Reason: {str(e)}")

    def offload_directory(self, path):
        try:
            folder_name = os.path.basename(path)
            destination = os.path.join(r"D:\AI_Factory\game_offload", folder_name)
            print(f"📦 Relocating asset weights to: {destination}...")
            
            if os.path.exists(destination):
                shutil.rmtree(destination)
                
            shutil.move(path, destination)
            print("✔ Offload shift successful. Local space reclaimed!")
            log_action("interrogator", "MANUAL_OFFLOAD", f"Shifted file paths from C to D partition: {path}")
        except Exception as e:
            print(f"❌ Migration roadblock: Ensure no apps are using this folder. {str(e)}")

if __name__ == "__main__":
    interrogator = IcarusStorageInterrogator()
    interrogator.begin_interrogation_loop()