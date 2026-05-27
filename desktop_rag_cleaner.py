import os
import zipfile
import time
import shutil
import subprocess
from rich.console import Console
from rich.panel import Panel

console = Console()

# ====================================================================
# TARGET DIRECTORY MAPPING CONFIGURATION (ONEDRIVE COMPLIANT)
# ====================================================================
USER_HOME = os.path.expanduser("~")

LOCAL_DESKTOP = os.path.normpath(os.path.join(USER_HOME, "Desktop"))
ONEDRIVE_DESKTOP = os.path.normpath(os.path.join(USER_HOME, "OneDrive", "Desktop"))

if os.path.exists(ONEDRIVE_DESKTOP):
    DESKTOP_PATH = ONEDRIVE_DESKTOP
else:
    DESKTOP_PATH = LOCAL_DESKTOP

TARGET_EXTENSIONS = (".txt", ".log")
MISC_RAG_FILE = "miscellaneous_rag.txt"
BACKUP_ZIP = "desktop_cleaned_archive.zip"

# New secure landing pad on D drive for high-priority files
D_PROJECTS_VAULT = r"D:\AI_Factory\important_desktop_records"
os.makedirs(D_PROJECTS_VAULT, exist_ok=True)

# Key phrases that trigger the intelligent evaluation questionnaire gate
HIGH_PRIORITY_KEYWORDS = ["IMPORTANT", "RAG", "CODE", "PROJECT", "CLIENT", "SNIPE", "FOREVER", "IMP"]

class DynamicDesktopRouter:
    def __init__(self):
        self.ingested_count = 0
        self.offloaded_count = 0

    def execution_sweep_and_archive(self):
        console.print("[bold bright_black]=======================================================[/bold bright_black]")
        console.print(Panel(
            "[bold cyan]🛰️ ICARUS FACTORY // INTELLIGENT ROUTING DESKTOP CLEANER[/bold cyan]\n"
            f"Scanning path: {DESKTOP_PATH}\n"
            f"Vaulting high-priority assets to: {D_PROJECTS_VAULT}",
            title="ROUTER_CORE", border_style="cyan"
        ))

        loose_files = [
            f for f in os.listdir(DESKTOP_PATH) 
            if f.endswith(TARGET_EXTENSIONS) and f != MISC_RAG_FILE and f != BACKUP_ZIP
        ]

        if not loose_files:
            console.print("[green]✔ Desktop storage environment is clean. No loose fragments detected.[/green]")
            return

        console.print(f"[yellow]⚡ Isolated {len(loose_files)} raw files. Commencing priority keyword analysis...[/yellow]\n")

        with open(MISC_RAG_FILE, "a", encoding="utf-8") as rag_out:
            with zipfile.ZipFile(BACKUP_ZIP, "a", zipfile.ZIP_DEFLATED) as archive:
                
                for file_name in loose_files:
                    full_path = os.path.join(DESKTOP_PATH, file_name)
                    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                    file_upper = file_name.upper()
                    
                    # Check if the filename contains any of our high-value development keywords
                    is_high_priority = any(keyword in file_upper for keyword in HIGH_PRIORITY_KEYWORDS)
                    
                    if is_high_priority:
                        console.print(f"\n[bold yellow]🔍 HIGH-PRIORITY FRAGMENT DETECTED:[/bold yellow] [white]{file_name}[/white]")
                        print("📂 Popping up File Explorer location for human review...")
                        try:
                            os.startfile(DESKTOP_PATH)
                        except Exception:
                            subprocess.run(['explorer', DESKTOP_PATH])
                            
                        print("\n❓ Questionnaire Action Gate:")
                        print("  [1] Offload this file directly to your D: drive Projects Vault.")
                        print("  [2] Standard Ingest (Append text to RAG stream and zip archive).")
                        print("  [3] Skip and leave on Desktop.")
                        
                        choice = input("\nSelect routing target choice (1/2/3): ").strip()
                        
                        if choice == "1":
                            try:
                                dest_path = os.path.join(D_PROJECTS_VAULT, file_name)
                                shutil.move(full_path, dest_path)
                                console.print(f"[bold green]🚀 OFFLOAD SUCCESSFUL:[/bold green] Shifted to {dest_path}")
                                self.offloaded_count += 1
                                continue # Skip the standard delete loop since shutil.move clears the source
                            except Exception as e:
                                console.print(f"[red]❌ Migration fail: {str(e)}[/red]")
                        elif choice == "3":
                            console.print("[gray]File protected. Skipping asset lines...[/gray]")
                            continue

                    # Standard execution pathway for normal notes
                    try:
                        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                            raw_content = f.read().strip()
                        
                        if raw_content:
                            structured_entry = (
                                f"\n\n=== [DESKTOP_RAG][{timestamp}][SRC: {file_name.upper()}] ===\n"
                                f"{raw_content}"
                            )
                            rag_out.write(structured_entry)
                            self.ingested_count += 1
                        
                        archive.write(full_path, os.path.basename(full_path))
                        os.remove(full_path)
                        console.print(f"[green]✔ Digested, Archived, and Cleared:[/green] {file_name}")
                        
                    except Exception as e:
                        console.print(f"[bold red]❌ Transmission error on {file_name}: {str(e)}[/bold red]")

        console.print(Panel(
            f"[bold green]💥 DYNAMIC SWEEP SYSTEM TERMINATED CLEANLY[/bold green]\n\n"
            f"• Files Shifted off C: Drive to Vault: {self.offloaded_count}\n"
            f"• Standard Notes Consolidated to RAG: {self.ingested_count}\n"
            f"• Master Local RAG DB Target: {MISC_RAG_FILE}",
            title="SWEEP_SUMMARY", border_style="green"
        ))

if __name__ == "__main__":
    router = DynamicDesktopRouter()
    router.execution_sweep_and_archive()