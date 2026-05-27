import os
import json
import time
from rich.console import Console
from rich.panel import Panel
from hitl_gate import verify_operator_key

console = Console()

TRACKER_FILE = "prompt_goal_tracker.json"
KB_FILE = "knowledge_base.txt"

class IcarusOrchestrator:
    def __init__(self):
        self.default_goals = {
            "Active_Sprints": [
                {
                    "id": 1,
                    "task": "Two-Provider Core Architecture Synchronization",
                    "priority": "CRITICAL",
                    "status": "ACTIVE",
                },
                {
                    "id": 2,
                    "task": "Visual thread researcher routing integration",
                    "priority": "HIGH",
                    "status": "QUEUED",
                },
            ],
            "Human_In_The_Loop_Safety_Gate": {
                "enabled": True,
                "authorization_validation_key": "SEC-OPERATOR-99X",
                "enforcement_scope": "disk_changes",
            },
            "Obsolete_Assets": ["old_test_script.py", "junk_log.txt"]
        }

    def initialize_tracker_cache(self):
        """Ensures your master goal tracker manifest is physically written to disk."""
        if not os.path.exists(TRACKER_FILE):
            with open(TRACKER_FILE, "w", encoding="utf-8") as f:
                json.dump(self.default_goals, f, indent=4)
            console.print("[green]✔ Initialized a pristine prompt_goal_tracker.json manifest file.[/green]")

    def auto_purge_obsolete_assets(self):
        """Scans the manifest definitions and auto-deletes specified junk scripts to optimize RAG safety."""
        if os.path.exists(TRACKER_FILE):
            with open(TRACKER_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            if not verify_operator_key():
                console.print(
                    "[bold red]⛔ Authorization failed. Disk change operations aborted.[/bold red]"
                )
                return
            
            purged = []
            for file_name in data.get("Obsolete_Assets", []):
                if os.path.exists(file_name):
                    os.remove(file_name)
                    purged.append(file_name)
            
            if purged:
                console.print(f"[bold red]🗑️ Auto-Purged Obsolete Junk Files from Drive Grid:[/bold red] {purged}")
            else:
                console.print("[gray][Orchestrator] No untracked junk scripts flagged for active deletion loops.[/gray]")

if __name__ == "__main__":
    orchestrator = IcarusOrchestrator()
    orchestrator.initialize_tracker_cache()
    orchestrator.auto_purge_obsolete_assets()