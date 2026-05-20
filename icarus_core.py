import os
from litellm import completion

def read_context_file(file_name):
    """Safely reads content from a specified workspace text file."""
    if not os.path.exists(file_name):
        return f"[System Matrix] Log file '{file_name}' empty or initializing baseline."
    with open(file_name, "r", encoding="utf-8") as f:
        return f.read()

def run_icarus_multi_rag(user_prompt):
    """
    Advanced Icarus Matrix - Dual-Thread RAG Router
    Cross-references User Concepts with Live Ingested Scraping Data.
    """
    print("\n[Icarus Engine] Activating dual-thread RAG routing...")
    
    # Extract both local knowledge bases
    creations_context = read_context_file("valorant_creations.txt")
    scraped_philosophy = read_context_file("knowledge_base.txt")
    
    system_instruction = (
        "You are Icarus, an elite private intelligence engine specializing in tactical game development philosophy, "
        "asset generation, and competitive data telemetry. You combine raw user prompt logic with ingested developer "
        "guidelines to instantly output complex, highly technical asset mockups, map layout briefs, and system code scripts."
    )
    
    # Merging the layers together cleanly for Gemini's massive context window
    combined_prompt = (
        "=== THREAD 1: USER ASSET CONCEPTS ===\n"
        f"{creations_context}\n"
        "=====================================\n\n"
        "=== THREAD 2: INGESTED DEV PHILOSOPHY & TELEMETRY ===\n"
        f"{scraped_philosophy}\n"
        "=====================================================\n\n"
        f"DEVELOPER PORTFOLIO REQUEST: {user_prompt}"
    )

    try:
        response = completion(
            model="gemini/gemini-2.5-flash",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": combined_prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Engine Routing Error: {str(e)}"

if __name__ == "__main__":
    print("--- ICARUS ENTERPRISE CORE ONLINE ---")
    
    # Complex multi-layered prompt to run a rapid prototyping mockup simulation
    portfolio_task = (
        "Based on my framework and the ingested meta trends, draft a highly complex, technical proposal "
        "for a new competitive map concept or weapon asset. Explain exactly how it forces a 50/50 round win probability "
        "shift based on utility economy, and lay down a conceptual rapid prototyping script blueprint for Blender."
    )
    
    output = run_icarus_multi_rag(portfolio_task)
    print("\n[Icarus Intelligence Output]:")
    print(output)