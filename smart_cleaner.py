import os
import time
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.table import Table

console = Console()

def run_realtime_radar_matrix():
    console.print("[bold bright_black]=============================================[/bold bright_black]")
    console.print(Panel("[bold green]📡 ICARUS DYNAMIC SYSTEM RADAR v3[/bold green]\nStreaming active workspace tracking arrays straight to console...", title="RADAR_LIVE"))
    
    all_files = [f for f in os.listdir('.') if os.path.isfile(f)]
    marked_for_review = []
    skipped_files = []

    # Dynamic Visual Stream Panel
    with Live(Panel("Initializing active sweep...", title="[cyan]LIVE REGISTRY SCAN[/cyan]"), refresh_per_second=10) as live:
        for index, file in enumerate(all_files):
            # This line forces the terminal to update dynamically so you see exactly what the bot is looking at
            live.update(Panel(f"Parsing node path: [bold yellow]{file}[/bold yellow]\nProgress tracking: {index+1}/{len(all_files)} files processed.", title="[cyan]LIVE REGISTRY SCAN[/cyan]", border_style="yellow"))
            time.sleep(0.15) # Smooth visible cadence for terminal views and streams
            
            if file.endswith(('.tmp', '.bak', '.old')) or file in ("test_log.txt", "desktop_cleaned_archive.zip"):
                marked_for_review.append(file)
            else:
                skipped_files.append(file)

    # Output Container Presentation
    summary_table = Table(title="🗄️ Automated Workspace Container Allocation")
    summary_table.add_column("Status Matrix", justify="left", style="cyan")
    summary_table.add_column("Tracked File Assets", style="white")
    summary_table.add_column("Reasoning Layer", style="bright_black")
    
    for f in marked_for_review:
        summary_table.add_row("🚩 REVIEW FOR PURGE", f, "Matches temporary workspace clutter signature.")
    for f in skipped_files:
        summary_table.add_row("🔒 SAFE / SKIPPED", f, "Core system script or protected data structure.")
        
    console.print(summary_table)

    # Human-In-The-Loop Training Interface
    if skipped_files:
        console.print(f"\n[bold magenta]Icarus Learning Loop:[/bold magenta] Evaluate the safe containers above.")
        console.print("👉 Did I skip an uncategorized file that you want marked for deletion? (y/n)")
        choice = input("> ").strip().lower()
        
        if choice == 'y':
            flagged_file = input("Enter the EXACT file name to inject into the training array: ").strip()
            if flagged_file in skipped_files:
                # Appends the rule directly back into your live RAG memory file
                with open("active_chat_stream.txt", "a", encoding="utf-8") as f:
                    f.write(f"\n[TRAINING_REINFORCEMENT] User manually flagged protected file '{flagged_file}' for future deletion cycles.")
                console.print(f"[bold green]✔ Optimization rule successfully promoted to active_chat_stream.txt for next RAG pass.[/bold green]")
            else:
                console.print("[bold red]File not found in active directory pool.[/bold red]")

if __name__ == "__main__":
    run_realtime_radar_matrix()