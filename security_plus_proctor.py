import os

print("==================================================")
print("     AI FACTORY: SECURITY+ SY0-701 PROCTOR ENGINE ")
print("==================================================")

# This structure holds the exact weights of the official exam objectives
EXAM_DOMAINS = {
    "1.0": {"name": "General Security Concepts", "weight": "12%"},
    "2.0": {"name": "Threats, Vulnerabilities, and Mitigations", "weight": "22%"},
    "3.0": {"name": "Security Architecture", "weight": "18%"},
    "4.0": {"name": "Security Operations", "weight": "28%"},
    "5.0": {"name": "Security Program Management and Oversight", "weight": "20%"}
}

def display_dashboard():
    print("\n[+] System Active. Ready to pull study metrics...")
    print("Official CompTIA SY0-701 Domain Targets:")
    for domain, info in EXAM_DOMAINS.items():
        print(f" -> Domain {domain}: {info['name']} ({info['weight']})")
    print("\n[*] Next Step: Initialize Anthropic API call to generate dynamic scenarios.")

if __name__ == "__main__":
    display_dashboard()