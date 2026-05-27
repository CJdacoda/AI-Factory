import os
import subprocess
import json
import webbrowser
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from hitl_gate import verify_operator_key

console = Console()
ROOT = Path(__file__).resolve().parent
VENV_PYTHON = ROOT / "venv" / "Scripts" / "python.exe"


def display_dashboard_menu():
    console.print("[bold bright_black]=======================================================[/bold bright_black]")
    console.print(
        Panel(
            "[bold cyan]🛰️ ICARUS AI FACTORY OPERATIONS DASHBOARD[/bold cyan]\n"
            "Dual-stack control: [white]Terminal matrix[/white] + [white]Local web HUD[/white] (no domain).\n"
            "Select a module key to execute.",
            title="SYSTEM_CONTROL",
            border_style="cyan",
        )
    )

    table = Table(title="Active Workspace Modules", title_style="bold magenta")
    table.add_column("Key", justify="center", style="green", no_wrap=True)
    table.add_column("Module", style="white")
    table.add_column("Objective", style="bright_black")

    table.add_row("1", "icarus_core.py", "Dual-pane RAG stream + Gemini comparison")
    table.add_row("2", "smart_cleaner.py", "Workspace radar + temp file review")
    table.add_row("3", "icarus_agent_loop.py", "Autonomous agent ledger loop")
    table.add_row("4", "icarus_scraper.py", "Harvest public meta → knowledge_base")
    table.add_row("5", "aws_cloud_shield.py", "Zero-trust IAM prototyper")
    table.add_row("6", "desktop_rag_cleaner.py", "Desktop .txt/.log → RAG + archive")
    table.add_row("7", "storage_offload_engine.py", "C: duplicate scan → offload to D:")
    table.add_row("10", "launch_icarus_stack.py", "Start bridge API + open Revenant HUD")
    table.add_row("11", "chat_triage_bridge.py", "Two-provider Flask API (:5000)")
    table.add_row("12", "rag_thread_researcher.py", "Visual thread reasoning load bar")
    table.add_row("14", "icarus_agent_controller.py", "Real-time sprint polling controller")
    table.add_row("15", "terminal_io_consultant.py", "Terminal I/O closed-loop monitor")
    table.add_row("16", "icarus_omni_speed.py", "Hyper-speed sprint orchestration")
    table.add_row("17", "icarus_orchestrator.py", "Goal tracker init + obsolete purge")
    table.add_row("M", "factory_manual.py", "Operations manual (reference)")
    table.add_row("Q", "Exit", "Power down dashboard")

    console.print(table)
    console.print(
        "[dim]Web HUD: double-click revenant_gui.html or use key [10]. "
        "Requires [11] or launch_icarus_stack running on 127.0.0.1:5000.[/dim]"
    )


def open_gui_only():
    gui = ROOT / "revenant_gui.html"
    if gui.exists():
        webbrowser.open(gui.as_uri())
        console.print(f"[green]✔ Opened {gui.name} in browser.[/green]")
    else:
        console.print("[red]❌ revenant_gui.html not found.[/red]")


def run_selected_module():
    gate_verified = False
    disk_touching = {
        "2", "3", "4", "6", "7", "11", "14", "16", "17",
    }
    modules = {
        "1": "icarus_core.py",
        "2": "smart_cleaner.py",
        "3": "icarus_agent_loop.py",
        "4": "icarus_scraper.py",
        "5": "aws_cloud_shield.py",
        "6": "desktop_rag_cleaner.py",
        "7": "storage_offload_engine.py",
        "10": "launch_icarus_stack.py",
        "11": "chat_triage_bridge.py",
        "12": "rag_thread_researcher.py",
        "14": "icarus_agent_controller.py",
        "15": "terminal_io_consultant.py",
        "16": "icarus_omni_speed.py",
        "17": "icarus_orchestrator.py",
        "m": "factory_manual.py",
    }

    while True:
        display_dashboard_menu()
        choice = input("\n[⚡ System Input] Enter Module Key to Execute: ").strip().lower()

        if choice == "q":
            console.print("[bold red]Shutting down operator dashboard...[/bold red]")
            break

        if choice == "h":
            open_gui_only()
            continue

        if choice not in modules:
            console.print("[bold red]Invalid operational key.[/bold red]\n")
            continue

        if choice in disk_touching and not gate_verified:
            if not verify_operator_key():
                console.print("[bold red]⛔ Launch blocked.[/bold red]\n")
                continue
            gate_verified = True

        target = modules[choice]
        console.print(
            Panel(
                f"[bold yellow][LAUNCHING][/bold yellow] {target}",
                border_style="yellow",
            )
        )

        try:
            subprocess.run([str(VENV_PYTHON), str(ROOT / target)], cwd=str(ROOT), check=True)
            console.print("[bold green]✔ Execution complete.[/bold green]\n")
            if choice not in ("10", "11", "14"):
                input("Press Enter to continue...")
        except subprocess.CalledProcessError as e:
            console.print(f"[bold red]❌ Error: {e}[/bold red]\n")
            input("Press Enter to continue...")
        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted.[/yellow]\n")


if __name__ == "__main__":
    run_selected_module()
