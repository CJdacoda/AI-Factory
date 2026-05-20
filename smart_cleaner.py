import os
from litellm import completion

def scan_factory_directory():
    """Scans the active directory to catalog files for RAG parsing."""
    valid_extensions = ('.py', '.txt', '.yml', '.json')
    catalog = []
    
    print("[Smart Cleaner] Inventorying current AI Factory workspace...")
    for file in os.listdir('.'):
        if file.endswith(valid_extensions) and os.path.isfile(file):
            catalog.append(file)
    return catalog

def run_intelligent_storage_optimizer():
    """
    Smart Cleaner Core - RAG Directory Alignment
    Analyzes active project files to optimize workspace structure.
    """
    print("\n[Smart Cleaner] Activating directory intelligence matrix...")
    
    files_to_optimize = scan_factory_directory()
    
    # Compile a structural manifest of all active files to use as RAG context
    workspace_manifest = ""
    for file_name in files_to_optimize:
        try:
            with open(file_name, "r", encoding="utf-8") as f:
                # Read the first few lines of each file to understand its purpose without wasting tokens
                snippet = "".join(f.readlines()[:5])
                workspace_manifest += f"\n--- FILE: {file_name} ---\n{snippet}\n"
        except Exception:
            workspace_manifest += f"\n--- FILE: {file_name} --- (Unable to parse raw data)\n"

    system_instruction = (
        "You are an elite System Administrator and Storage Optimization Intelligence. Your job is to analyze "
        "the active workspace file manifest, evaluate structural redundancies, and provide a perfectly organized "
        "directory layout recommendation to keep the development workspace running at peak performance."
    )
    
    user_prompt = (
        f"Analyze this active local file manifest and provide a structural optimization map:\n{workspace_manifest}"
    )

    try:
        response = completion(
            model="gemini/gemini-2.5-flash",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Optimizer Routing Error: {str(e)}"

if __name__ == "__main__":
    print("=== SMART CLEANER LOGISTICS ENGINE ONLINE ===")
    
    optimization_map = run_intelligent_storage_optimizer()
    print("\n[Icarus AI Factory - Recommended Storage Architecture Map]:")
    print(optimization_map)