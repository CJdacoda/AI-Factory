print("==================================================")
print("     AI FACTORY: AZURE IAM ARCHITECT ENGINE       ")
print("==================================================")

# Simulating an Azure Active Directory Tenant Permission Matrix
AZURE_RBAC_POLICY = {
    "Role_Definition": "Cloud Security Auditor",
    "Assignable_Scopes": ["/subscriptions/sub-101"],
    "Permissions": {
        "Actions": [
            "Microsoft.Authorization/*/read",
            "Microsoft.Insights/Logs/read",
            "Microsoft.Security/securityStatuses/read"
        ],
        "NotActions": [
            "Microsoft.Authorization/*/write",
            "Microsoft.Security/policies/write"
        ]
    }
}

def audit_cloud_identity():
    print("\n[+] Azure Resource Manager (ARM) Identity Simulator Active.")
    print(f"Current Role Evaluated: {AZURE_RBAC_POLICY['Role_Definition']}")
    print("------------------------------------------------------------------")
    print("Enforcing Zero Trust Architecture Compliance...")
    
    print("\nAllowed Actions (Read-Only Audit Track):")
    for action in AZURE_RBAC_POLICY["Permissions"]["Actions"]:
        print(f" -> ALLOW: {action}")
        
    print("\nBlocked Actions (Explicit Deny to Prevent Privilege Escalation):")
    for not_action in AZURE_RBAC_POLICY["Permissions"]["NotActions"]:
        print(f" -> DENY: {not_action}")

    print("\n[*] Next Step: Connect API to simulate an IAM cloud breach evaluation script.")

if __name__ == "__main__":
    audit_cloud_identity()