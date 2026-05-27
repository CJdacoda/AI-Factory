import os
import json
import time
import subprocess
from typing import List, Optional

from rich.console import Console
from rich.panel import Panel

console = Console()

TERMINAL_LOG = "active_terminal_stream.log"
PAUSE_FILE = "pause_state.json"


class TerminalIOConsultant:
    def __init__(self):
        self.last_processed_line = 0
        if not os.path.exists(TERMINAL_LOG):
            with open(TERMINAL_LOG, "w", encoding="utf-8") as f:
                f.write("[SYSTEM] Terminal Stream Logger Initialized.\n")

    def append_terminal_line(self, line: str, source: str = "AGENT") -> None:
        """Append a single line to the shared terminal buffer (closed-loop ingest)."""
        with open(TERMINAL_LOG, "a", encoding="utf-8") as f:
            f.write(f"[{source}] {line.rstrip()}\n")

    def process_new_lines_instant(self, emit_panel: bool = False) -> int:
        """
        Read and parse any newly appended log lines immediately.
        Returns the number of lines processed this pass.
        """
        if emit_panel:
            console.print(
                "[bold bright_black]=======================================================[/bold bright_black]"
            )
            console.print(
                Panel(
                    "[bold purple]📺 ICARUS // TERMINAL I/O ACTIVE RUNTIME CONSULTANT[/bold purple]\n"
                    f"Monitoring stream buffer: {TERMINAL_LOG} for rapid execution parsing...",
                    title="TERMINAL_AUDITOR",
                    border_style="purple",
                )
            )

        processed = 0
        try:
            with open(TERMINAL_LOG, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()

            if len(lines) <= self.last_processed_line:
                return 0

            new_content = lines[self.last_processed_line :]
            self.last_processed_line = len(lines)

            for line in new_content:
                line_str = line.strip()
                if not line_str:
                    continue

                processed += 1
                console.print(f"[gray][Terminal Output][/gray] {line_str}")

                if "Traceback" in line_str or "ModuleNotFoundError" in line_str:
                    console.print(
                        "\n[bold blink red]🚨 CRITICAL RUNTIME CRASH DETECTED IN TERMINAL FEED 🚨[/bold blink red]"
                    )
                    self.auto_inject_healing_command("pip install -r requirements.txt")
                    break

                if "InfiniteLoopWarning" in line_str or "OutOfMemory" in line_str:
                    console.print(
                        "\n[bold red]⏸️ EMERGENCY SUSPENSION: LOOP ANOMALY FLAGGED[/bold red]"
                    )
                    self.trigger_dashboard_emergency_halt()
                    break
        except Exception as e:
            console.print(
                f"[bold red]❌ Terminal link reading interruption: {str(e)}[/bold red]"
            )

        return processed

    def watch_and_inject_terminal_loop(self) -> None:
        """Polling entry point used when consultant runs as a standalone daemon."""
        self.process_new_lines_instant(emit_panel=True)

    def stream_command_to_log(
        self,
        command: List[str],
        cwd: Optional[str] = None,
        source: str = "MOD_PASS",
    ) -> int:
        """
        Execute a command-line modification pass; stream stdout/stderr to the
        terminal log and invoke instant consultant parsing after each line.
        """
        self.append_terminal_line(
            f"Starting modification pass: {' '.join(command)}", source=source
        )
        self.process_new_lines_instant()

        proc = subprocess.Popen(
            command,
            cwd=cwd or os.getcwd(),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )

        lines_streamed = 0
        if proc.stdout:
            for line in proc.stdout:
                self.append_terminal_line(line, source=source)
                lines_streamed += 1
                self.process_new_lines_instant()

        exit_code = proc.wait()
        self.append_terminal_line(
            f"Modification pass complete (exit={exit_code})", source=source
        )
        self.process_new_lines_instant()
        return exit_code

    def auto_inject_healing_command(self, recovery_command: str) -> None:
        """Programmatically inject corrective inputs into the terminal buffer."""
        console.print(
            Panel(
                f"[bold yellow]🔧 SELF-HEALING REFLEX INITIATED[/bold yellow]\n"
                f"Automatically injecting correction input string: [green]{recovery_command}[/green]",
                border_style="yellow",
            )
        )

        with open(TERMINAL_LOG, "a", encoding="utf-8") as f:
            f.write(f"\n[AUTO_INPUT] Executing Recovery Macro: {recovery_command}\n")

        console.print(
            "[bold green]✔ Recovery injection logged to workspace terminal stream.[/bold green]"
        )

    def trigger_dashboard_emergency_halt(self) -> None:
        """Force pause file state to freeze background agents."""
        with open(PAUSE_FILE, "w", encoding="utf-8") as f:
            json.dump({"agent_paused": True, "last_interrupt": time.time()}, f)
        console.print(
            "[bold red]✔ System state globally toggled to PAUSED. Background asset modifications frozen.[/bold red]"
        )


if __name__ == "__main__":
    consultant = TerminalIOConsultant()

    while True:
        consultant.watch_and_inject_terminal_loop()
        time.sleep(1)
