import os
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def render_operations_manual():
    console.print("[bold bright_black]=======================================================[/bold bright_black]")
    console.print(
        Panel(
            "[bold cyan]🛰️ ICARUS AI FACTORY OPERATIONS MANUAL v2.0[/bold cyan]\n"
            "Dual-branch stack: Terminal dashboard + Local web HUD (Revenant).",
            title="SYSTEM_MANUAL",
            border_style="cyan",
        )
    )

    env_table = Table(title="🔌 Boot Sequence", title_style="bold magenta")
    env_table.add_column("Step", style="green")
    env_table.add_column("Command", style="white")
    env_table.add_row("1", "d:")
    env_table.add_row("2", "cd D:\\AI_Factory")
    env_table.add_row("3", "venv\\Scripts\\activate")
    env_table.add_row("4", "python launch_icarus_stack.py   # API + browser HUD")
    env_table.add_row("5", "python factory_dashboard.py     # terminal menu")
    console.print(env_table)

    file_table = Table(title="🗄️ Core Modules", title_style="bold magenta")
    file_table.add_column("Key", style="cyan", justify="center")
    file_table.add_column("File", style="yellow")
    file_table.add_column("Role", style="white")
    rows = [
        ("10", "launch_icarus_stack.py", "Start bridge + open revenant_gui.html"),
        ("11", "chat_triage_bridge.py", "Gemini→Mistral triage API :5000"),
        ("—", "revenant_gui.html", "Local browser HUD (file:///)"),
        ("7", "storage_offload_engine.py", "Move duplicate game/cache files C→D"),
        ("6", "desktop_rag_cleaner.py", "Ingest desktop notes → RAG, clear clutter"),
        ("2", "smart_cleaner.py", "Workspace temp/radar scan"),
        ("14", "icarus_agent_controller.py", "Sprint polling + pause_state.json"),
        ("15", "terminal_io_consultant.py", "Closed-loop terminal log triad"),
    ]
    for r in rows:
        file_table.add_row(*r)
    console.print(file_table)

    console.print(
        Panel(
            "[bold green]🧠 RAG + Safety[/bold green]\n"
            "• knowledge_base.txt — structural memory\n"
            "• active_chat_stream.txt — live ingest (Tampermonkey / HUD)\n"
            "• Human gate: SEC-OPERATOR-99X for disk-changing ops\n"
            "• Providers: Gemini Flash + Mistral Large only (no Grok)",
            title="DATA_MANAGEMENT",
            border_style="green",
        )
    )


if __name__ == "__main__":
    render_operations_manual()
