import json
import os
import requests
import socket
import glob
from datetime import datetime

# BharatDef-AI: Autonomous Recon & Surface Intelligence Engine
# Architect: Sahil Ahmad
# Dedicated with love to: ZOYA

COMMON_PORTS = [21, 22, 25, 53, 80, 110, 143, 443, 3306, 8080, 8443]
COMMON_SUBDOMAINS = ["api", "admin", "dev", "staging", "mail", "vpn", "portal", "test", "auth", "secure"]

def get_api_key():
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        print("\n[!] Error: GEMINI_API_KEY environment variable set nahi hai.")
        print("[!] Command run karein: export GEMINI_API_KEY='aapki_key'")
        return None
    return key

def clean_target(domain):
    return domain.replace("https://", "").replace("http://", "").split("/")[0].strip()

def scan_ports(host_ip):
    print(f"\n[*] Scanning common ports on {host_ip}...")
    open_ports = []
    for port in COMMON_PORTS:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        if s.connect_ex((host_ip, port)) == 0:
            open_ports.append(port)
        s.close()
    return open_ports

def discover_subdomains(target_domain):
    print(f"\n[*] Subdomain Discovery shuru ho rahi hai ({target_domain})...")
    discovered = []
    for sub in COMMON_SUBDOMAINS:
        sub_host = f"{sub}.{target_domain}"
        try:
            sub_ip = socket.gethostbyname(sub_host)
            discovered.append({"subdomain": sub_host, "ip": sub_ip})
            print(f"  [+] Active mila: {sub_host} -> {sub_ip}")
        except socket.error:
            pass
    return discovered

def get_headers_and_ip(domain_clean):
    data = {}
    try:
        ip = socket.gethostbyname(domain_clean)
        data["ip_address"] = ip
    except Exception as e:
        data["ip_address"] = f"DNS Error: {e}"

    try:
        res = requests.get(f"https://{domain_clean}", timeout=7)
        data["http_status"] = res.status_code
        data["server_headers"] = dict(res.headers)
    except Exception as e:
        data["http_status"] = "Connection Failed"
        data["server_headers"] = str(e)
    return data

def run_ai_audit(domain, data, open_ports, subdomains, api_key):
    print("\n[*] AI Reasoning Engine Enterprise Audit taiyar kar raha hai...")
    
    prompt = f"""
    You are BharatDef-AI, an enterprise defensive security reasoning engine.
    Target: {domain}
    Resolved Root IP: {data.get('ip_address')}
    Open Exposed Ports: {open_ports}
    Discovered Active Subdomains: {json.dumps(subdomains, indent=2)}
    HTTP Status: {data.get('http_status')}
    Response Headers: {json.dumps(data.get('server_headers'), indent=2)}

    Generate a formal executive defensive audit containing:
    1. Attack Surface Assessment (analyze exposed ports, tech stack, and discovered subdomains).
    2. Missing Defensive Headers & Security Architecture Gaps.
    3. Exposure Severity Score (0-10) with technical rationale.
    4. Actionable Remediation Roadmap for engineering teams.
    """

    endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent?key={api_key}"
    try:
        res = requests.post(endpoint, json={"contents": [{"parts": [{"text": prompt}]}]}, headers={"Content-Type": "application/json"})
        if res.status_code == 200:
            report = res.json()['candidates'][0]['content']['parts'][0]['text']
            banner = "\n=======================================================\n" \
                     "   BHARATDEF-AI : ENTERPRISE SURFACE AUDIT REPORT     \n" \
                     "   Architect: Sahil Ahmad | Dedicated to: ZOYA        \n" \
                     "=======================================================\n"
            print(banner)
            print(report)

            filename = f"report_{domain}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(banner)
                f.write(f"\nGenerated At: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Target: {domain}\n")
                f.write(f"Resolved IP: {data.get('ip_address')}\n")
                f.write(f"Open Ports: {open_ports}\n")
                f.write(f"Discovered Subdomains: {json.dumps(subdomains, indent=2)}\n\n")
                f.write(report)
            print(f"\n[+] Audit Report Save Ho Gayi: {filename}")
        else:
            print(f"[!] AI API Error: {res.status_code} - {res.text}")
    except Exception as e:
        print(f"[!] Request Failed: {e}")

def list_reports():
    reports = glob.glob("report_*.txt")
    if not reports:
        print("\n[!] Abhi tak koi saved report nahi mili.")
        return
    print("\n--- Saved Audit Reports ---")
    for i, r in enumerate(reports, 1):
        print(f"[{i}] {r}")
    choice = input("\nReport number choose karein (ya Enter dabayein wapas jane ke liye): ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(reports):
        with open(reports[int(choice) - 1], "r", encoding="utf-8") as f:
            print("\n" + f.read())

def main_menu():
    api_key = get_api_key()
    if not api_key:
        return

    while True:
        print("\n=======================================================")
        print("   BHARATDEF-AI ENGINE (Autonomous Intelligence)       ")
        print("   Architect: Sahil Ahmad | Dedicated to: ZOYA        ")
        print("=======================================================")
        print("[1] Quick Web Audit (DNS + HTTP Headers + AI Report)")
        print("[2] Full Defense Scan (DNS + Port Recon + Headers + AI)")
        print("[3] Deep Perimeter Audit (Ports + Subdomains + AI Report)")
        print("[4] View Saved Audit Reports")
        print("[5] Exit")
        
        choice = input("\nOption chunein (1-5): ").strip()

        if choice == "1":
            target = input("\nEnter Target Domain (e.g. example.com): ").strip()
            if target:
                clean = clean_target(target)
                data = get_headers_and_ip(clean)
                run_ai_audit(clean, data, "Not Scanned (Quick Mode)", [], api_key)
        elif choice == "2":
            target = input("\nEnter Target Domain (e.g. scanme.nmap.org): ").strip()
            if target:
                clean = clean_target(target)
                data = get_headers_and_ip(clean)
                open_ports = []
                if "DNS Error" not in data["ip_address"]:
                    open_ports = scan_ports(data["ip_address"])
                run_ai_audit(clean, data, open_ports, [], api_key)
        elif choice == "3":
            target = input("\nEnter Target Domain (e.g. github.com): ").strip()
            if target:
                clean = clean_target(target)
                data = get_headers_and_ip(clean)
                open_ports = []
                if "DNS Error" not in data["ip_address"]:
                    open_ports = scan_ports(data["ip_address"])
                subs = discover_subdomains(clean)
                run_ai_audit(clean, data, open_ports, subs, api_key)
        elif choice == "4":
            list_reports()
        elif choice == "5":
            print("\nExiting BharatDef-AI. Jai Hind!\n")
            break
        else:
            print("\n[!] Galat option, kripya 1 se 5 ke beech chunein.")

if __name__ == "__main__":
    main_menu()
