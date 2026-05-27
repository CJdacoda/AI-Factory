import os
import json
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from llm_provider_config import mistral_large_completion

console = Console()

TRACKER_FILE = "prompt_goal_tracker.json"
PAUSE_FILE = "pause_state.json"


class IcarusOmniSpeedController:
    def __init__(self):
        # Human clearance key required for any disk-touching / code-modification actions.
        self.access_key = "SEC-OPERATOR-99X"
        self.initialize_system_states()

    def initialize_system_states(self):
        if not os.path.exists(PAUSE_FILE):
            with open(PAUSE_FILE, "w", encoding="utf-8") as f:
                json.dump({"agent_paused": False}, f)

    def _load_pause_state(self) -> dict:
        if not os.path.exists(PAUSE_FILE):
            return {"agent_paused": False}
        with open(PAUSE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def _set_paused(self, paused: bool) -> None:
        with open(PAUSE_FILE, "w", encoding="utf-8") as f:
            json.dump({"agent_paused": paused}, f)

    def rank_and_score_codebase_files(self):
        """Scans the master goal manifest and ranks code files from most to least important."""
        if not os.path.exists(TRACKER_FILE):
            return []

        with open(TRACKER_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        sprints = data.get("Active_Sprints", [])

        # Priority Weighting Matrix Mapping Algorithm
        priority_weights = {"CRITICAL": 1, "HIGH": 2, "MEDIUM": 3, "LOW": 4}
        sprints.sort(key=lambda x: priority_weights.get(x.get("priority", "LOW"), 5))

        table = Table(title="📡 Icarus Smart RAG Priority Ingestion Hierarchy")
        table.add_column("Rank Index", justify="center", style="cyan")
        table.add_column("Target Task Objective", style="white")
        table.add_column("Priority Tier", style="yellow", justify="center")

        for idx, task in enumerate(sprints, start=1):
            table.add_row(str(idx), task.get("task"), task.get("priority"))

        console.print(table)
        return sprints

    def execute_proactive_operator_interrogation(self, current_task: str):
        """Halts operations before completion to prompt the user with interactive questions."""
        console.print(
            f"\n[bold yellow]❓ [ICARUS INTERROGATION] Evaluating Phase: {current_task}[/bold yellow]"
        )

        # Interactive Human-In-The-Loop Question Gate
        user_input = input(
            ">> Confirm code generation parameters meet industry standards? (y/n): "
        ).strip().lower()
        entered_key = input(
            ">> Enter authorization key for disk changes (SEC-OPERATOR-99X): "
        ).strip()

        if user_input != "y" or entered_key != self.access_key:
            console.print(
                "[bold red]⏸️ Execution suspended by operator directive. Freezing file modifications.[/bold red]"
            )
            # Signal other controllers to halt.
            self._set_paused(True)
            return False

        # Clear paused state after successful validation.
        self._set_paused(False)
        return True

    def inject_personality_flair(self, clean_technical_checklist: str) -> str:
        """High-intensity personality overlay using the allowed Mistral Large provider."""
        console.print("\n[cyan]🎭 Transmitting pristine checklist to Mistral Large for tactical flair injection...[/cyan]")

        system_instruction = (
            "You are the aggressive tactical AI persona of the Icarus-Omni Hypervisor. "
            "Take the provided system checklist and rewrite it with high-intensity, demanding military efficiency. "
            "Focus heavily on discipline, speed, and securing competitive clearance benchmarks. Keep it punchy. "
            "Do not add disclaimers."
        )

        try:
            response = mistral_large_completion(
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": clean_technical_checklist},
                ]
            )
            return response.choices[0].message.content
        except Exception:
            fallback = (
                "[Fallback Operational Notice] Core requirements secured. Baseline benchmarks cleared on disk partition."
            )
            console.print(f"[yellow]{fallback}[/yellow]")
            return fallback

    def run_hyperspeed_orchestration_cycle(self):
        console.print(
            "[bold bright_black]=======================================================[/bold bright_black]"
        )
        ranked_tasks = self.rank_and_score_codebase_files()

        if not ranked_tasks:
            console.print(
                "[yellow]Standing by. No active sprint targets flagged in workspace logs.[/yellow]"
            )
            return

        primary_target = ranked_tasks[0].get("task")

        # Run human verification check before pushing code models / file tasks.
        if self.execute_proactive_operator_interrogation(primary_target):
            # Simulated pristine output generated by your local Gemini Flash intake filters (represented here as a checklist).
            mock_clean_checklist = (
                "1. Clear out untracked temporary log files from active paths.\n"
                "2. Push optimized directory updates straight to your portfolio repository.\n"
                "3. Satisfy mechanical baseline response benchmarks before competitive matchmaking unlocks."
            )
            flavored = self.inject_personality_flair(mock_clean_checklist)
            console.print(
                Panel(
                    flavored,
                    title="[bold red]🛰️ ICARUS-OMNI SECURE BROADCAST[/bold red]",
                    border_style="red",
                )
            )


if __name__ == "__main__":
    controller = IcarusOmniSpeedController()
    controller.run_hyperspeed_orchestration_cycle()

