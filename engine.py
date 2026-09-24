import json
import os
import requests
import socket
import ssl
import glob
from datetime import datetime

# BharatDef-AI: Autonomous Recon & Surface Intelligence Engine
# Architect: Sahil Ahmad
# Dedicated with love to: ZOYA

# ANSI Colors
C_RESET = "\033[0m"
C_BOLD = "\033[1m"
C_RED = "\033[91m"
C_GREEN = "\033[92m"
C_YELLOW = "\033[93m"
C_BLUE = "\033[94m"
C_CYAN = "\033[96m"

COMMON_PORTS = [21, 22, 25, 53, 80, 110, 143, 443, 3306, 8080, 8443]
COMMON_SUBDOMAINS = ["api", "admin", "dev", "staging", "mail", "vpn", "portal", "test", "auth", "secure"]

def get_api_key():
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        print(f"\n{C_RED}[!] Error: GEMINI_API_KEY environment variable set nahi hai.{C_RESET}")
        print(f"{C_YELLOW}[!] Command run karein: export GEMINI_API_KEY='aapki_key'{C_RESET}")
        return None
    return key

def clean_target(domain):
    return domain.replace("https://", "").replace("http://", "").split("/")[0].strip()

def check_ssl(domain_clean):
    print(f"{C_BLUE}[*] Checking SSL/TLS Certificate for {domain_clean}...{C_RESET}")
    ssl_info = {}
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((domain_clean, 443), timeout=5) as sock:
            with ctx.wrap_socket(sock, server_hostname=domain_clean) as ssock:
                cert = ssock.getpeercert()
                ssl_info["issuer"] = dict(x[0] for x in cert.get("issuer", []))
                ssl_info["expiry"] = cert.get("notAfter")
                ssl_info["version"] = ssock.version()
                print(f"  {C_GREEN}[+] SSL Active | Expires: {ssl_info.get('expiry')}{C_RESET}")
    except Exception as e:
        ssl_info["error"] = f"SSL Check Failed / No HTTPS: {e}"
        print(f"  {C_YELLOW}[!] SSL Check Failed / No HTTPS{C_RESET}")
    return ssl_info

def scan_ports(host_ip):
    print(f"\n{C_BLUE}[*] Scanning common ports on {host_ip}...{C_RESET}")
    open_ports = []
    for port in COMMON_PORTS:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        if s.connect_ex((host_ip, port)) == 0:
            open_ports.append(port)
            print(f"  {C_GREEN}[+] Open Port Detected: {port}{C_RESET}")
        s.close()
    return open_ports

def discover_subdomains(target_domain):
    print(f"\n{C_BLUE}[*] Subdomain Discovery shuru ho rahi hai ({target_domain})...{C_RESET}")
    discovered = []
    for sub in COMMON_SUBDOMAINS:
        sub_host = f"{sub}.{target_domain}"
        try:
            sub_ip = socket.gethostbyname(sub_host)
            discovered.append({"subdomain": sub_host, "ip": sub_ip})
            print(f"  {C_GREEN}[+] Active mila: {sub_host} -> {sub_ip}{C_RESET}")
        except socket.error:
            pass
    return discovered

def get_headers_and_ip(domain_clean):
    data = {}
    try:
        ip = socket.gethostbyname(domain_clean)
        data["ip_address"] = ip
        print(f"{C_GREEN}[+] Resolved IP: {ip}{C_RESET}")
    except Exception as e:
        data["ip_address"] = f"DNS Error: {e}"
        print(f"{C_RED}[!] DNS Error: {e}{C_RESET}")

    try:
        res = requests.get(f"https://{domain_clean}", timeout=7)
        data["http_status"] = res.status_code
        data["server_headers"] = dict(res.headers)
    except Exception as e:
        data["http_status"] = "Connection Failed"
        data["server_headers"] = str(e)
    return data

def run_ai_audit(domain, data, open_ports, subdomains, ssl_data, api_key):
    print(f"\n{C_CYAN}[*] AI Reasoning Engine Enterprise Audit taiyar kar raha hai...{C_RESET}")
    
    prompt = f"""
    You are BharatDef-AI, an enterprise defensive security reasoning engine.
    Target: {domain}
    Resolved Root IP: {data.get('ip_address')}
    Open Exposed Ports: {open_ports}
    Discovered Active Subdomains: {json.dumps(subdomains, indent=2)}
    SSL/TLS Certificate Details: {json.dumps(ssl_data, indent=2)}
    HTTP Status: {data.get('http_status')}
    Response Headers: {json.dumps(data.get('server_headers'), indent=2)}

    Generate a formal executive defensive audit containing:
    1. Attack Surface Assessment (ports, tech stack, subdomains, SSL health).
    2. Missing Defensive Headers & Security Architecture Gaps.
    3. Exposure Severity Score (0-10) with technical rationale.
    4. Actionable Remediation Roadmap for engineering teams.
    """

    endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent?key={api_key}"
    try:
        res = requests.post(endpoint, json={"contents": [{"parts": [{"text": prompt}]}]}, headers={"Content-Type": "application/json"})
        if res.status_code == 200:
            report = res.json()['candidates'][0]['content']['parts'][0]['text']
            
            banner = f"{C_CYAN}\n=======================================================\n" \
                     f"   BHARATDEF-AI : ENTERPRISE SURFACE AUDIT REPORT     \n" \
                     f"   Architect: Sahil Ahmad | Dedicated to: ZOYA        \n" \
                     f"======================================================={C_RESET}\n"
            print(banner)
            print(report)

            clean_banner = "\n=======================================================\n" \
                           "   BHARATDEF-AI : ENTERPRISE SURFACE AUDIT REPORT     \n" \
                           "   Architect: Sahil Ahmad | Dedicated to: ZOYA        \n" \
                           "=======================================================\n"

            filename = f"report_{domain}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(clean_banner)
                f.write(f"\nGenerated At: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Target: {domain}\n")
                f.write(f"Resolved IP: {data.get('ip_address')}\n")
                f.write(f"Open Ports: {open_ports}\n")
                f.write(f"Discovered Subdomains: {json.dumps(subdomains, indent=2)}\n")
                f.write(f"SSL Status: {json.dumps(ssl_data, indent=2)}\n\n")
                f.write(report)
            print(f"\n{C_GREEN}[+] Audit Report Safaltapoorvak Save Ho Gayi: {filename}{C_RESET}")
        else:
            print(f"{C_RED}[!] AI API Error: {res.status_code} - {res.text}{C_RESET}")
    except Exception as e:
        print(f"{C_RED}[!] Request Failed: {e}{C_RESET}")

def list_reports():
    reports = glob.glob("report_*.txt")
    if not reports:
        print(f"\n{C_YELLOW}[!] Abhi tak koi saved report nahi mili.{C_RESET}")
        return
    print(f"\n{C_CYAN}--- Saved Audit Reports ---{C_RESET}")
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
        print(f"{C_CYAN}\n=======================================================")
        print(f"   {C_BOLD}BHARATDEF-AI ENGINE (Autonomous Intelligence){C_RESET}{C_CYAN}       ")
        print(f"   Architect: Sahil Ahmad | Dedicated to: {C_RED}ZOYA ❤️{C_RESET}{C_CYAN}        ")
        print(f"======================================================={C_RESET}")
        print(f"{C_GREEN}[1]{C_RESET} Quick Web Audit (DNS + Headers + AI)")
        print(f"{C_GREEN}[2]{C_RESET} Perimeter Scan (DNS + Ports + SSL + Headers + AI)")
        print(f"{C_GREEN}[3]{C_RESET} Full Attack-Surface Audit (Ports + Subdomains + SSL + AI)")
        print(f"{C_GREEN}[4]{C_RESET} View Saved Audit Reports")
        print(f"{C_RED}[5] Exit{C_RESET}")
        
        choice = input(f"\n{C_YELLOW}Option chunein (1-5): {C_RESET}").strip()

        if choice == "1":
            target = input("\nEnter Target Domain (e.g. example.com): ").strip()
            if target:
                clean = clean_target(target)
                data = get_headers_and_ip(clean)
                run_ai_audit(clean, data, "Not Scanned", [], {}, api_key)
        elif choice == "2":
            target = input("\nEnter Target Domain (e.g. scanme.nmap.org): ").strip()
            if target:
                clean = clean_target(target)
                data = get_headers_and_ip(clean)
                open_ports = []
                if "DNS Error" not in data["ip_address"]:
                    open_ports = scan_ports(data["ip_address"])
                ssl_data = check_ssl(clean)
                run_ai_audit(clean, data, open_ports, [], ssl_data, api_key)
        elif choice == "3":
            target = input("\nEnter Target Domain (e.g. github.com): ").strip()
            if target:
                clean = clean_target(target)
                data = get_headers_and_ip(clean)
                open_ports = []
                if "DNS Error" not in data["ip_address"]:
                    open_ports = scan_ports(data["ip_address"])
                subs = discover_subdomains(clean)
                ssl_data = check_ssl(clean)
                run_ai_audit(clean, data, open_ports, subs, ssl_data, api_key)
        elif choice == "4":
            list_reports()
        elif choice == "5":
            print(f"\n{C_GREEN}Exiting BharatDef-AI. Jai Hind!{C_RESET}\n")
            break
        else:
            print(f"\n{C_RED}[!] Galat option, kripya 1 se 5 ke beech chunein.{C_RESET}")

if __name__ == "__main__":
    main_menu()
