import random
from rich.console import Console
from rich.panel import Panel

console = Console()

def run_tactical_pathway_simulation():
    console.print(Panel("[bold cyan]🔮 SHADOW BIOME SIMULATION PROTOCOL[/bold cyan]\nRunning 1,000 multi-agent tactical round models over pure vector calculations..."))
    
    # Mathematical Representation of a map choke point
    # Vector coordinate bounds (X, Y)
    choke_point_x = 55.0
    sightline_obstruction = True 
    
    attacker_wins = 0
    defender_wins = 0
    
    for round_id in range(1, 1001):
        # Simulate an agent's entry speed and angle variables using randomized vectors
        attacker_angle = random.uniform(10.0, 90.0)
        defender_reaction_ms = random.randint(150, 300) # Reaction telemetry simulation
        
        # Pure logical evaluation gate: Why graphics aren't needed to test balance
        if sightline_obstruction and defender_reaction_ms < 220:
            if attacker_angle > 45.0:
                defender_wins += 1
            else:
                attacker_wins += 1
        else:
            attacker_wins += 1

    win_rate = (attacker_wins / 1000) * 100
    console.print(f"[🛡️ Sim Complete] Attacker Matrix Win Rate: [bold green]{win_rate:.2f}%[/bold green]")
    console.print(f"[📊 Data Output] Total Aggregated Telemetry Points Calculated: {1000 * 3}")

if __name__ == "__main__":
    run_tactical_pathway_simulation()