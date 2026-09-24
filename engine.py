import json
import os
import requests
import socket
from datetime import datetime

# BharatDef-AI: Autonomous Recon & Surface Intelligence Engine
# Architect: Sahil Ahmad
# Dedicated with love to: ZOYA

COMMON_PORTS = [21, 22, 25, 53, 80, 110, 143, 443, 3306, 8080, 8443]

def scan_ports(host_ip):
    print(f"[*] [Step 2] Common Ports Scan Kar Raha Hai ({host_ip})...")
    open_ports = []
    for port in COMMON_PORTS:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.6)
        result = s.connect_ex((host_ip, port))
        if result == 0:
            open_ports.append(port)
        s.close()
    return open_ports

def get_target_metadata(domain):
    metadata = {}
    print(f"\n[*] [Step 1] Target Host Map Kar Raha Hai: {domain}")
    domain_clean = domain.replace("https://", "").replace("http://", "").split("/")[0]
    
    try:
        ip_address = socket.gethostbyname(domain_clean)
        metadata["ip_address"] = ip_address
    except Exception as e:
        metadata["ip_address"] = f"DNS Resolution Error: {e}"

    try:
        url = f"https://{domain_clean}"
        response = requests.get(url, timeout=7)
        metadata["http_status"] = response.status_code
        metadata["server_headers"] = dict(response.headers)
    except Exception as e:
        metadata["http_status"] = "Connection Failed"
        metadata["server_headers"] = str(e)

    if "DNS Resolution Error" not in metadata["ip_address"]:
        metadata["open_ports"] = scan_ports(metadata["ip_address"])
    else:
        metadata["open_ports"] = []

    return metadata

def run_ai_surface_audit(domain, data, api_key):
    print("[*] [Step 3] AI Reasoning Engine Analysis Shuru Kar Raha Hai...")
    
    analysis_prompt = f"""
    You are BharatDef-AI, an enterprise autonomous defensive security reasoning engine.
    Analyze the technical reconnaissance data of the following target domain:
    Target: {domain}
    Resolved IP: {data.get('ip_address')}
    Open Exposed Ports: {data.get('open_ports')}
    HTTP Status: {data.get('http_status')}
    Response Headers: {json.dumps(data.get('server_headers'), indent=2)}

    Generate a formal executive defensive audit containing:
    1. Attack Surface Assessment (including risks of exposed open ports).
    2. Missing Defensive Safeguards & Header Configurations.
    3. Exposure Severity Score (0-10).
    4. Actionable Remediation Roadmap.
    """

    endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": analysis_prompt}]}]
    }

    try:
        res = requests.post(endpoint, json=payload, headers={"Content-Type": "application/json"})
        if res.status_code == 200:
            result = res.json()
            report_body = result['candidates'][0]['content']['parts'][0]['text']
            
            banner = "\n=======================================================\n" \
                     "   BHARATDEF-AI : ENTERPRISE SURFACE AUDIT REPORT     \n" \
                     "   Architect: Sahil Ahmad | Dedicated to: ZOYA        \n" \
                     "=======================================================\n"
            
            print(banner)
            print(report_body)

            clean_name = domain.replace("https://", "").replace("http://", "").split("/")[0]
            filename = f"report_{clean_name}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(banner)
                f.write(f"\nGenerated At: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Target: {clean_name}\n")
                f.write(f"Resolved IP: {data.get('ip_address')}\n")
                f.write(f"Open Ports: {data.get('open_ports')}\n\n")
                f.write(report_body)

            print(f"\n[+] Audit Report Safaltapoorvak Save Ho Gayi: {filename}")
        else:
            print(f"[!] AI API Response Error: {res.status_code} - {res.text}")
    except Exception as e:
        print(f"[!] Pipeline Error: {e}")

if __name__ == "__main__":
    print("=======================================================")
    print("   BHARATDEF-AI ENGINE (Autonomous Intelligence)       ")
    print("   Architect: Sahil Ahmad | Dedicated to: ZOYA        ")
    print("=======================================================")
    
    active_key = os.environ.get("GEMINI_API_KEY")
    if not active_key:
        active_key = "YOUR_GEMINI_API_KEY"

    target_input = input("\nEnter Target Domain (e.g. scanme.nmap.org): ").strip()
    if target_input:
        target_data = get_target_metadata(target_input)
        run_ai_surface_audit(target_input, target_data, active_key)
