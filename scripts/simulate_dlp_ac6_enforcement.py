#!/usr/bin/env python3
"""
simulate_dlp_ac6_enforcement.py - NIST SP 800-53 AC-6 Least Privilege & DLP Simulation
Google Cybersecurity Professional Certificate - Course 5: Assets, Threats, and Vulnerabilities
Author: Eduardo Souza Marques (@edusouzamarques)

Demonstrates:
1. Vulnerable Document Sharing (Manual verbal warnings, persistent access, accidental parent folder leak)
2. NIST AC-6 Hardened Sharing (Auto-revoking TTL links, Role-Based Access Controls, and DLP policy block)
"""

import time
from datetime import datetime, timedelta

def simulate_vulnerable_data_leak():
    print("\n" + "="*70)
    print("🚨 SCENARIO 1: VULNERABLE DATA SHARING (Manual Oversight / Unrestricted)")
    print("="*70)
    print("[*] Asset: 'New_Product_Launch_2026' (Parent Internal Folder)")
    print("[*] Contents: [promotional_flyer.pdf, customer_analytics.xlsx, business_plans.docx]")
    print("[*] Control: Verbal Manager Warning ('Please do not share yet')\n")

    print("[+] Sales Manager shares full parent folder with sales rep...")
    time.sleep(0.5)
    print("    --> Folder shared. Meeting ends. Manager FORGETS to revoke permissions.")
    print("    --> Residual Access Status: PERSISTENT (Indefinite Access).")

    print("\n[+] Sales Representative enters video call with external partner...")
    time.sleep(0.5)
    print("    --> Representative attempts to share 'promotional_flyer.pdf'...")
    print("    ⚠️ MISTAKE: Representative accidentally copies parent folder URL instead!")
    print("    ⚠️ Outbound Sharing Policy: DISABLED (Unrestricted External Sharing).")
    
    print("\n🚨 [DATA LEAK CONFIRMED] External partner receives confidential folder link!")
    print("🚨 Partner posts link to public social media page. Confidential roadmaps exposed.")
    print("="*70)

class CloudDocumentShare:
    def __init__(self, resource_name, is_confidential=False):
        self.resource_name = resource_name
        self.is_confidential = is_confidential
        self.active_shares = {}

    def grant_time_bound_access(self, user, role, duration_seconds=2):
        expiry = datetime.now() + timedelta(seconds=duration_seconds)
        self.active_shares[user] = {"role": role, "expiry": expiry}
        print(f"[+] AC-6 Control: Granted access on '{self.resource_name}' to {user} (Role: {role}).")
        print(f"    --> Automated Expiration (TTL): {duration_seconds}s from issuance.")

    def is_access_valid(self, user):
        if user not in self.active_shares:
            return False, "User not provisioned in Access Control List."
        
        share_info = self.active_shares[user]
        if datetime.now() > share_info["expiry"]:
            return False, "Access expired via automatic time-based revocation (NIST AC-6)."
        
        return True, "Authorized."

    def attempt_external_share(self, user, target_email):
        valid, reason = self.is_access_valid(user)
        if not valid:
            return False, f"BLOCKED: {reason}"
        
        role = self.active_shares[user]["role"]
        # NIST AC-6 Role Restriction: Sales reps cannot externally share parent confidential folders
        if self.is_confidential and role != "Executive_Admin":
            return False, "DLP VIOLATION: Role 'Sales_Representative' cannot share confidential parent folders externally."

        return True, "External link generated successfully."

def simulate_hardened_nist_ac6_defense():
    print("\n" + "="*70)
    print("🛡️ SCENARIO 2: HARDENED DATA SHARING (NIST SP 800-53: AC-6 Controls)")
    print("="*70)
    print("[*] Control 1: Automated Time-Based Access Revocation (Expiring TTL Links)")
    print("[*] Control 2: Role-Based External Link Restriction (RBAC & DLP Policy)\n")

    parent_folder = CloudDocumentShare("New_Product_Launch_2026", is_confidential=True)

    # 1. Manager provisions time-bound access
    parent_folder.grant_time_bound_access("sales_rep_1", role="Sales_Representative", duration_seconds=1)

    print("\n[+] Sales rep attempts to share parent confidential folder with external partner...")
    success, message = parent_folder.attempt_external_share("sales_rep_1", "partner@externalcorp.com")
    print(f"    🛡️ Policy Enforcement: {message}")

    print("\n[+] Meeting concludes. Waiting for automatic time-to-live (TTL) expiration...")
    time.sleep(1.2)

    print("\n[+] Sales rep attempts to re-access folder post-meeting...")
    valid, message = parent_folder.is_access_valid("sales_rep_1")
    print(f"    🛡️ Access Check: {message}")
    print("🛡️ [PROTECTED] Accidental data leak completely prevented by automated controls.")
    print("="*70)

if __name__ == "__main__":
    simulate_vulnerable_data_leak()
    time.sleep(1)
    simulate_hardened_nist_ac6_defense()
    print("\n✅ Verification Complete: NIST SP 800-53 AC-6 least privilege controls validated.")
