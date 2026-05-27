import hashlib
import json
import os
import shutil
from collections import defaultdict
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from hitl_gate import verify_operator_key

console = Console()
CONFIG_FILE = "icarus_workspace_config.json"


def _load_config() -> dict:
    if not os.path.exists(CONFIG_FILE):
        return {
            "storage_offload_root": r"D:\AI_Factory\storage_offload",
            "game_offload_root": r"D:\AI_Factory\game_offload",
            "scan_sources_on_c": [],
            "duplicate_extensions": [".tmp", ".bak", ".log", ".zip", ".pak"],
            "protected_paths": [],
        }
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _expand_user(path: str) -> str:
    return os.path.expandvars(os.path.expanduser(path))


def _file_hash(path: str, block_size: int = 65536) -> str:
    h = hashlib.md5()
    with open(path, "rb") as f:
        while chunk := f.read(block_size):
            h.update(chunk)
    return h.hexdigest()


def _is_protected(path: str, protected: list[str]) -> bool:
    norm = os.path.normcase(os.path.abspath(path))
    for p in protected:
        base = os.path.normcase(os.path.abspath(_expand_user(p)))
        if norm.startswith(base):
            return True
    return False


def scan_duplicate_candidates(cfg: dict, max_files_per_root: int = 5000) -> list[dict]:
    """Find duplicate files (same MD5) under configured C: scan roots."""
    exts = tuple(cfg.get("duplicate_extensions", []))
    protected = [_expand_user(p) for p in cfg.get("protected_paths", [])]
    sources = [_expand_user(p) for p in cfg.get("scan_sources_on_c", []) if p]

    by_hash: dict[str, list[str]] = defaultdict(list)
    scanned = 0

    for root in sources:
        if not os.path.isdir(root):
            continue
        for dirpath, _, filenames in os.walk(root):
            if scanned >= max_files_per_root:
                break
            for name in filenames:
                if exts and not name.lower().endswith(exts):
                    continue
                full = os.path.join(dirpath, name)
                if _is_protected(full, protected):
                    continue
                try:
                    if os.path.getsize(full) < 1024:
                        continue
                    digest = _file_hash(full)
                    by_hash[digest].append(full)
                    scanned += 1
                except OSError:
                    continue

    duplicates = []
    for digest, paths in by_hash.items():
        if len(paths) > 1:
            duplicates.append({"hash": digest, "paths": paths, "size_mb": round(os.path.getsize(paths[0]) / (1024 * 1024), 2)})
    duplicates.sort(key=lambda x: x["size_mb"], reverse=True)
    return duplicates


def offload_duplicates_to_d(duplicates: list[dict], cfg: dict, dry_run: bool = False) -> int:
    """Keep first path; move extras to D:\\AI_Factory\\game_offload\\<hash>\\"""
    offload_root = _expand_user(cfg.get("game_offload_root", r"D:\AI_Factory\game_offload"))
    os.makedirs(offload_root, exist_ok=True)
    moved = 0

    for group in duplicates:
        keep = group["paths"][0]
        for extra in group["paths"][1:]:
            dest_dir = os.path.join(offload_root, group["hash"][:12])
            os.makedirs(dest_dir, exist_ok=True)
            dest = os.path.join(dest_dir, os.path.basename(extra))
            if dry_run:
                console.print(f"[dim]DRY-RUN move:[/dim] {extra} -> {dest}")
                moved += 1
                continue
            try:
                shutil.move(extra, dest)
                console.print(f"[green]✔ Offloaded:[/green] {extra} -> {dest}")
                moved += 1
            except OSError as e:
                console.print(f"[red]❌ Failed {extra}: {e}[/red]")
    return moved


def run_storage_offload_pipeline():
    console.print(
        Panel(
            "[bold cyan]💾 ICARUS STORAGE OFFLOAD ENGINE[/bold cyan]\n"
            "Scans configured C: paths for duplicate game/cache files and moves extras to D:.",
            title="STORAGE_OFFLOAD",
            border_style="cyan",
        )
    )

    cfg = _load_config()
    console.print("[yellow]Scanning for duplicate file groups (this may take a minute)...[/yellow]")
    dupes = scan_duplicate_candidates(cfg)

    if not dupes:
        console.print("[green]✔ No duplicate groups found in configured scan paths.[/green]")
        return

    table = Table(title="Duplicate Groups (largest first)")
    table.add_column("#", style="cyan")
    table.add_column("Size (MB)", justify="right")
    table.add_column("Copies", justify="center")
    table.add_column("Sample path", style="white")

    for i, g in enumerate(dupes[:15], start=1):
        table.add_row(str(i), str(g["size_mb"]), str(len(g["paths"])), g["paths"][0][:70])

    console.print(table)
    console.print(f"[bold]Found {len(dupes)} duplicate group(s).[/bold]")

    if not verify_operator_key():
        console.print("[red]⛔ Offload aborted — authorization failed.[/red]")
        return

    dry = input("Dry-run first? (y/n, default y): ").strip().lower() != "n"
    if dry:
        offload_duplicates_to_d(dupes, cfg, dry_run=True)
        confirm = input("\nProceed with real offload to D: ? (y/n): ").strip().lower()
        if confirm != "y":
            console.print("[yellow]Offload cancelled.[/yellow]")
            return
        offload_duplicates_to_d(dupes, cfg, dry_run=False)
    else:
        offload_duplicates_to_d(dupes, cfg, dry_run=False)

    console.print(
        Panel(
            f"[green]Offload target:[/green] {_expand_user(cfg.get('game_offload_root', ''))}\n"
            "C: drive clutter reduced by moving duplicate copies to D:.",
            title="COMPLETE",
            border_style="green",
        )
    )


if __name__ == "__main__":
    run_storage_offload_pipeline()
