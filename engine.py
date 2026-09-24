import json
import os
import requests
import socket

# BharatDef-AI: Autonomous Recon & Surface Intelligence Engine
# Architect: Sahil Ahmad
# Dedicated with love to: ZOYA

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY")

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

    return metadata

def run_ai_surface_audit(domain, data, api_key):
    print("[*] [Step 2] AI Reasoning Engine Analysis Shuru Kar Raha Hai...")
    
    analysis_prompt = f"""
    You are BharatDef-AI, an enterprise autonomous defensive security reasoning engine.
    Analyze the technical reconnaissance data of the following target domain:
    Target: {domain}
    Resolved IP: {data.get('ip_address')}
    HTTP Status: {data.get('http_status')}
    Response Headers: {json.dumps(data.get('server_headers'), indent=2)}

    Generate a formal executive defensive audit containing:
    1. Attack Surface Assessment.
    2. Missing Defensive Safeguards.
    3. Severity Score.
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
            print("\n=======================================================")
            print("   BHARATDEF-AI : ENTERPRISE SURFACE AUDIT REPORT     ")
            print("=======================================================\n")
            print(result['candidates'][0]['content']['parts'][0]['text'])
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

    target_input = input("\nEnter Target Domain (e.g. example.com): ").strip()
    if target_input:
        target_data = get_target_metadata(target_input)
        run_ai_surface_audit(target_input, target_data, active_key)
