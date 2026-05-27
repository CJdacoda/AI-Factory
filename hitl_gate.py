import json
import os

TRACKER_FILE = "prompt_goal_tracker.json"
DEFAULT_KEY = "SEC-OPERATOR-99X"


def load_gate_config() -> dict:
    if not os.path.exists(TRACKER_FILE):
        return {"enabled": True, "authorization_validation_key": DEFAULT_KEY}
    with open(TRACKER_FILE, "r", encoding="utf-8") as f:
        tracker = json.load(f)
    return tracker.get(
        "Human_In_The_Loop_Safety_Gate",
        {"enabled": True, "authorization_validation_key": DEFAULT_KEY},
    )


def verify_operator_key(prompt: str | None = None) -> bool:
    gate = load_gate_config()
    if not gate.get("enabled", True):
        return True
    expected = str(gate.get("authorization_validation_key", DEFAULT_KEY))
    if prompt is None:
        prompt = "\n[SECURITY GATE] Enter authorization key for disk changes: "
    entered = input(prompt).strip()
    return entered == expected
