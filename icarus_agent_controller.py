import os
import json
import sys
import time
import subprocess
from rich.console import Console
from rich.panel import Panel

from terminal_io_consultant import TerminalIOConsultant, TERMINAL_LOG

console = Console()

PAUSE_FILE = "pause_state.json"
TRACKER_FILE = "prompt_goal_tracker.json"
PYTHON_EXE = os.path.join("venv", "Scripts", "python.exe")


class IcarusAgentController:
    def __init__(self):
        self.initialize_state_maps()
        self.terminal_consultant = TerminalIOConsultant()

    def initialize_state_maps(self):
        if not os.path.exists(PAUSE_FILE):
            with open(PAUSE_FILE, "w", encoding="utf-8") as f:
                json.dump({"agent_paused": False, "last_interrupt": 0}, f)

    def check_runtime_permission_gate(self):
        """Verifies if the operator has issued a hardware pause command via the web hypervisor interface."""
        if os.path.exists(PAUSE_FILE):
            with open(PAUSE_FILE, "r", encoding="utf-8") as f:
                state = json.load(f)
            if state.get("agent_paused", False):
                console.print(
                    "[bold blink red]⏸️ [INTERRUPT] AGENT PROCESSING PAUSED VIA DASHBOARD HUD[/bold blink red]"
                )
                return False
        return True

    def run_code_modification_pass(self) -> int:
        """
        Closed-loop triad pass:
        Agent controller executes verification → terminal consultant reads stream instantly.
        """
        console.print(
            "[System] Spinning up automated code modification pass through Cursor CLI engine..."
        )
        self.terminal_consultant.append_terminal_line(
            "Triad sync: agent controller linked to terminal I/O consultant.",
            source="TRIAD",
        )

        verification_targets = [
            "shadow_simulation.py",
            "chat_triage_bridge.py",
            "terminal_io_consultant.py",
        ]
        exit_code = 0
        for target in verification_targets:
            if not os.path.exists(target):
                self.terminal_consultant.append_terminal_line(
                    f"Skip missing target: {target}", source="MOD_PASS"
                )
                self.terminal_consultant.process_new_lines_instant()
                continue

            result = self.terminal_consultant.stream_command_to_log(
                [PYTHON_EXE, "-m", "py_compile", target],
                cwd=os.getcwd(),
                source="MOD_PASS",
            )
            if result != 0:
                exit_code = result

        return exit_code

    def execute_autonomous_sprint_cycle(self):
        console.print(
            "[bold bright_black]=======================================================[/bold bright_black]"
        )
        console.print(
            Panel(
                "[bold purple]🤖 ICARUS AUTONOMOUS REAL-TIME ORCHESTRATOR POLLING[/bold purple]\n"
                "Analyzing active task metrics and evaluation bounds...",
                title="AGENT_CORE",
                border_style="purple",
            )
        )

        if not self.check_runtime_permission_gate():
            console.print(
                "[yellow][Agent Status] Core loop suspended. Awaiting operator resumption code...[/yellow]"
            )
            return

        if os.path.exists(TRACKER_FILE):
            with open(TRACKER_FILE, "r", encoding="utf-8") as f:
                tracker = json.load(f)

            sprints = tracker.get("Active_Sprints", [])
            if not sprints:
                console.print(
                    "[green]✔ No active task parameters assigned. Standing by...[/green]"
                )
                return

            sprints.sort(
                key=lambda x: 0
                if x.get("priority") == "CRITICAL"
                else (1 if x.get("priority") == "HIGH" else 2)
            )
            active_target = sprints[0]

            console.print(
                f"[bold cyan][Executing Target Task][/bold cyan] ID {active_target['id']}: "
                f"[white]{active_target['task']}[/white] [{active_target['priority']}]"
            )

            triad = tracker.get("Closed_Loop_Triad_Orchestration", {})
            if triad.get("completion_percent") == 100:
                console.print(
                    "[bold green]✔ Closed-Loop Triad Orchestration: OPERATIONAL (100%)[/bold green]"
                )

            exit_code = self.run_code_modification_pass()

            if exit_code == 0:
                console.print(
                    "[bold green]✔ Code verification check complete. "
                    f"Terminal stream synchronized via {TERMINAL_LOG}.[/bold green]"
                )
            else:
                console.print(
                    "[bold red]❌ Modification pass reported errors. "
                    "Terminal consultant captured diagnostics in stream log.[/bold red]"
                )


if __name__ == "__main__":
    controller = IcarusAgentController()
    while True:
        controller.execute_autonomous_sprint_cycle()
        time.sleep(5)
