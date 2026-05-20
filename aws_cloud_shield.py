import os
import json
from litellm import completion

def generate_hardened_iam_policy(role_scope):
    """
    Cloud Shield Engine - Powered by LiteLLM & Gemini Free Tier
    Generates strict, zero-trust AWS IAM JSON policies based on least privilege.
    """
    print(f"\n[Cloud Shield] Analyzing scope and drafting security policy for: {role_scope}")
    
    system_instruction = (
        "You are an elite Cloud Security Architect specializing in public sector zero-trust frameworks. "
        "Your task is to output a valid, production-ready AWS IAM JSON policy that enforces strict least privilege. "
        "Do not include any introductory markdown commentary—only output the raw, valid JSON string."
    )
    
    user_prompt = f"Generate a hardened, zero-trust IAM policy for this specific role/scope: {role_scope}"

    try:
        response = completion(
            model="gemini/gemini-2.5-flash",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Policy Generation Error: {str(e)}"

def local_security_scan(policy_json_str):
    """Simulates a local SIEM/Linter security scan on the generated policy"""
    print("[Cloud Shield] Running local threat linting scan...")
    
    # Simple Python rule check for unsafe wildcard permissions
    if '"*"' in policy_json_str or '"Action": "*"' in policy_json_str:
        print("[⚠️ SECURITY ALERT] Unsafe wildcard '*' detected! Reviewing policy access rings.")
        return "CRITICAL: Policy violates Zero-Trust protocols due to excessive scope."
    
    print("[🛡️ PASS] No global administrative wildcards detected in policy syntax.")
    return "SUCCESS: Secure configuration baseline verified."

if __name__ == "__main__":
    print("=== AWS CLOUD SHIELD ARCHITECT ONLINE ===")
    
    # Let's mock a high-risk data scenario: an automation bot that needs access to a secure S3 ledger bucket
    target_scope = "A background data pipeline that needs to read and write logs strictly to an S3 bucket named 'government-esports-telemetry-2026'. No deletion allowed."
    
    generated_policy = generate_hardened_iam_policy(target_scope)
    print("\n[Generated AWS IAM Security Policy]:")
    print(generated_policy)
    
    print("\n-------------------------------------------")
    scan_results = local_security_scan(generated_policy)
    print(f"[Scan Results Summary]: {scan_results}")