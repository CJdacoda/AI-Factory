import os
import time
from rich.console import Console, Group
from rich.panel import Panel
from rich.columns import Columns
from rich.live import Live
from llm_provider_config import gemini_flash_completion

console = Console()

KNOWLEDGE_BASE_FILE = "knowledge_base.txt"
ACTIVE_CHAT_FILE = "active_chat_stream.txt"
PANE_PREVIEW_CHARS = 1400
POLL_INTERVAL_SEC = 2.0

ACTIVE_CHAT_BASELINE = """=== LIVE CHAT STREAM — Structural Notes ===
[Paste or append live Cursor, ChatGPT, and Gemini thread fragments here for side-by-side comparison with knowledge_base.txt]
"""


def read_context_file(file_name):
    """Safely reads content from a specified workspace text file."""
    if not os.path.exists(file_name):
        return f"[System Matrix] Log file '{file_name}' empty or initializing baseline."
    with open(file_name, "r", encoding="utf-8") as f:
        return f.read()


def ensure_active_chat_stream():
    """Creates the live chat stream file if it does not exist yet."""
    if not os.path.exists(ACTIVE_CHAT_FILE):
        with open(ACTIVE_CHAT_FILE, "w", encoding="utf-8") as f:
            f.write(ACTIVE_CHAT_BASELINE)


def _truncate_for_pane(text, max_chars=PANE_PREVIEW_CHARS):
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n\n[dim]… truncated for pane preview[/dim]"


def build_dual_pane_renderable(kb_text, chat_text):
    """Side-by-side panes: structural KB vs live chat stream."""
    left = Panel(
        _truncate_for_pane(kb_text),
        title=f"[bold cyan]STRUCTURAL KB[/bold cyan] — {KNOWLEDGE_BASE_FILE}",
        border_style="cyan",
    )
    right = Panel(
        _truncate_for_pane(chat_text),
        title=f"[bold magenta]LIVE STREAM[/bold magenta] — {ACTIVE_CHAT_FILE}",
        border_style="magenta",
    )
    return Columns([left, right], equal=True, expand=True)


def run_dual_pane_stream(poll_interval=POLL_INTERVAL_SEC):
    """
    Real-time dual-pane comparison loop.
    Left: knowledge_base.txt | Right: active_chat_stream.txt (polls for file changes).
    """
    ensure_active_chat_stream()
    last_chat_mtime = None

    console.print("[bold cyan][Icarus Engine][/bold cyan] Dual-pane RAG stream online. Ctrl+C to exit watch mode.\n")

    with Live(console=console, refresh_per_second=4, screen=True) as live:
        while True:
            kb_text = read_context_file(KNOWLEDGE_BASE_FILE)
            chat_text = read_context_file(ACTIVE_CHAT_FILE)

            mtime = os.path.getmtime(ACTIVE_CHAT_FILE) if os.path.exists(ACTIVE_CHAT_FILE) else 0
            if last_chat_mtime is None:
                stream_status = "[yellow]○ initializing[/yellow]"
            elif mtime != last_chat_mtime:
                stream_status = "[bold green]● LIVE UPDATE[/bold green]"
            else:
                stream_status = "[dim]○ synced[/dim]"
            last_chat_mtime = mtime

            header = Panel(
                "[bold]Dual-Pane RAG Stream[/bold]  |  "
                f"{stream_status}  |  poll {poll_interval}s  |  Ctrl+C to exit",
                border_style="bright_black",
            )
            live.update(Group(header, build_dual_pane_renderable(kb_text, chat_text)))
            time.sleep(poll_interval)


def run_icarus_multi_rag(user_prompt):
    """
    Advanced Icarus Matrix — Dual-Thread RAG Router
    Cross-references structural knowledge_base notes with the live active_chat_stream.
    """
    ensure_active_chat_stream()
    console.print("\n[bold cyan][Icarus Engine][/bold cyan] Activating dual-thread RAG routing...")

    structural_kb = read_context_file(KNOWLEDGE_BASE_FILE)
    live_chat = read_context_file(ACTIVE_CHAT_FILE)

    system_instruction = (
        "You are Icarus, an elite private intelligence engine. You compare structural reference "
        "notes from a master knowledge base against a live chat stream. Highlight alignments, "
        "contradictions, and gaps between the two threads. Output concise, technical structural "
        "analysis the developer can act on immediately."
    )

    combined_prompt = (
        "=== THREAD 1: STRUCTURAL KNOWLEDGE BASE (knowledge_base.txt) ===\n"
        f"{structural_kb}\n"
        "================================================================\n\n"
        "=== THREAD 2: LIVE CHAT STREAM (active_chat_stream.txt) ===\n"
        f"{live_chat}\n"
        "===========================================================\n\n"
        f"COMPARISON REQUEST: {user_prompt}"
    )

    try:
        response = gemini_flash_completion(
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": combined_prompt},
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Engine Routing Error: {str(e)}"


if __name__ == "__main__":
    console.print("[bold bright_black]--- ICARUS ENTERPRISE CORE ONLINE ---[/bold bright_black]")

    try:
        run_dual_pane_stream()
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Stream halted.[/bold yellow]")

    console.print(
        Panel(
            "[bold]Dual-pane watch ended.[/bold]\n"
            "Append notes to active_chat_stream.txt while the stream runs, "
            "then run a comparison query below.",
            title="RAG_ROUTER",
            border_style="cyan",
        )
    )

    user_prompt = input("\n[⚡] Enter comparison query (Enter = default structural diff): ").strip()
    if not user_prompt:
        user_prompt = (
            "Compare structural themes in the knowledge base against the live chat stream. "
            "List what is aligned, what is missing from the KB, and what should be promoted "
            "into the master layer."
        )

    output = run_icarus_multi_rag(user_prompt)
    console.print(Panel(output, title="[bold green]Icarus Intelligence Output[/bold green]", border_style="green"))
