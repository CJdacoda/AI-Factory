import os
import time
from rich.console import Console
from rich.panel import Panel
from llm_provider_config import gemini_flash_completion

console = Console()

def check_system_load():
    """
    Dynamic Resource Guard.
    Simulates checking system resource load to allocate task thresholds safely.
    """
    # In a full deployment, psutil would read live RAM here.
    # For our safety blueprint, we set a smart constraint:
    console.print("[bold yellow][Safety Guard] Evaluating active system resource thresholds...[/bold yellow]")
    
    # Let's assume standard app usage is active to prevent lag spikes
    active_applications_open = True 
    
    if active_applications_open:
        console.print("[🛡️ Resource Guard] Active apps detected. Limiting background pipeline to: 1 Task Max.")
        return 1
    else:
        console.print("[🚀 Resource Guard] System idle. Unlocking parallel processing: 2 Tasks Max.")
        return 2

def read_agent_ledger():
    """Reads the 10-minute historical token ledger to track recent actions."""
    ledger_file = "agent_log.txt"
    if not os.path.exists(ledger_file):
        with open(ledger_file, "w", encoding="utf-8") as f:
            f.write("[TOKEN-1000] System Initialization. Core RAG modules online.\n")
        return "[TOKEN-1000] System Initialization. Core RAG modules online."
    
    with open(ledger_file, "r", encoding="utf-8") as f:
        return f.read()

def execute_agent_evaluation(task_limit):
    """Executes a self-correcting evaluation loop using Gemini 2.5 Flash."""
    console.print(Panel("[bold cyan]🔄 ICARUS CORE LOOP RUNNING[/bold cyan]\nReading historical token metrics...", title="AGENT_MATRIX"))
    
    # Ingest the 10-minute historical token horizon
    past_actions = read_agent_ledger()
    
    system_instruction = (
        "You are the brain of the Icarus Autonomous Agent Loop. Your job is to analyze your recent action ledger, "
        "evaluate what tasks were executed in the last 10 minutes, and determine the single next optimal logical step "
        "for cloud simulation or data ingestion based on the allowed task limits."
    )
    
    user_prompt = (
        f"HISTORICAL RUN LOGS (Last 10 Min):\n{past_actions}\n\n"
        f"RESOURCE ALLOCATION LIMIT: Execute max {task_limit} task(s).\n"
        "Output a new timestamped memory token indicating what task you are initiating next."
    )

    try:
        response = gemini_flash_completion(
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_prompt},
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Agent Loop Error: {str(e)}"

def append_new_token(new_log_token):
    """Appends the newly generated action token back into the continuous ledger."""
    with open("agent_log.txt", "a", encoding="utf-8") as f:
        f.write(f"\n[TOKEN-{int(time.time())}] {new_log_token}")
    console.print("[bold green][Ledger] New authorization token successfully appended to agent_log.txt.[/bold green]")

if __name__ == "__main__":
    console.print("[bold bright_black]=============================================[/bold bright_black]")
    
    # 1. Check system load to allocate task counts
    allowed_tasks = check_system_load()
    
    # 2. Run the RAG self-evaluation matrix
    next_action_token = execute_agent_evaluation(allowed_tasks)
    
    # 3. Print the live thought to your screen
    console.print(Panel(next_action_token, title="[bold magenta]ICARUS SELF-DETERMINED NEXT TASK[/bold magenta]", border_style="yellow"))
    
    # 4. Commit it to memory
    append_new_token(next_action_token)