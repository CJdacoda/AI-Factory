import os
import datetime

print("==================================================")
print("     AI FACTORY: SPLUNK SIEM SIMULATOR ENGINE     ")
print("==================================================")

# This simulates raw machine data ingested into a SIEM index
MOCK_LOG_EVENTS = [
    {"timestamp": "2026-05-17 23:14:02", "src_ip": "192.168.1.50", "dest_ip": "10.0.0.1", "action": "ALLOW", "reason": "Established connection"},
    {"timestamp": "2026-05-17 23:14:15", "src_ip": "45.227.254.12", "dest_ip": "10.0.0.1", "action": "DENY", "reason": "Brute force threshold exceeded"},
    {"timestamp": "2026-05-17 23:15:00", "src_ip": "192.168.1.99", "dest_ip": "10.0.0.5", "action": "ALLOW", "reason": "SSH successful login"},
    {"timestamp": "2026-05-17 23:16:22", "src_ip": "185.190.140.3", "dest_ip": "10.0.0.1", "action": "DENY", "reason": "Malicious IP Threat Intelligence Match"}
]

def display_siem_dashboard():
    print("\n[+] SIEM Database Online. Total indexed events found: 4")
    print("\nAvailable Indexed Fields: [_time, src_ip, dest_ip, action, reason]")
    print("------------------------------------------------------------------")
    
    # Simulating a basic Splunk search command pipeline using pipes (|)
    print("Simulated Splunk SPL Command Search: search action=DENY | table src_ip, reason")
    print("Results:")
    
    for log in MOCK_LOG_EVENTS:
        if log["action"] == "DENY":
            print(f" -> SRC_IP: {log['src_ip']} | REASON: {log['reason']}")
            
    print("\n[*] Next Step: Hook up the API to generate 100+ random hacker log variants for analysis.")

if __name__ == "__main__":
    display_siem_dashboard()