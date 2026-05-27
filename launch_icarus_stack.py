import os
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

from rich.console import Console
from rich.panel import Panel

console = Console()

ROOT = Path(__file__).resolve().parent
VENV_PYTHON = ROOT / "venv" / "Scripts" / "python.exe"
BRIDGE_SCRIPT = ROOT / "chat_triage_bridge.py"
GUI_FILE = ROOT / "revenant_gui.html"
BRIDGE_URL = "http://127.0.0.1:5000"


def launch_icarus_stack(open_browser: bool = True) -> None:
    console.print(
        Panel(
            "[bold cyan]🛰️ ICARUS LOCAL STACK LAUNCHER[/bold cyan]\n"
            "Starts the triage bridge API and opens the Revenant HUD in your browser.\n"
            "No domain required — everything runs on 127.0.0.1.",
            title="LAUNCH",
            border_style="cyan",
        )
    )

    if not VENV_PYTHON.exists():
        console.print("[red]❌ venv not found. Run: python -m venv venv && pip install -r requirements.txt[/red]")
        sys.exit(1)

    if not GUI_FILE.exists():
        console.print("[red]❌ revenant_gui.html missing in project root.[/red]")
        sys.exit(1)

    console.print("[yellow]Starting chat_triage_bridge.py on port 5000...[/yellow]")
    proc = subprocess.Popen(
        [str(VENV_PYTHON), str(BRIDGE_SCRIPT)],
        cwd=str(ROOT),
        creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == "nt" else 0,
    )

    time.sleep(2)
    gui_uri = GUI_FILE.as_uri()
    console.print(f"[green]✔ Bridge PID {proc.pid}[/green]")
    console.print(f"[green]✔ API:[/green] {BRIDGE_URL}")
    console.print(f"[green]✔ HUD:[/green] {gui_uri}")

    if open_browser:
        webbrowser.open(gui_uri)
        console.print("[cyan]Opened Revenant GUI in default browser.[/cyan]")

    console.print(
        "\n[dim]Leave the bridge window running. Press Ctrl+C in that window to stop the API.[/dim]"
    )


if __name__ == "__main__":
    launch_icarus_stack()
