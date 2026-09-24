# BharatDef-AI 🛡️
> Enterprise Autonomous Cyber Defense & Attack Surface Intelligence Engine

**Architect & Lead Researcher:** Sahil Ahmad  
**Dedicated with love to:** ZOYA ❤️

BharatDef-AI is an autonomous defensive reconnaissance and security analysis engine built for Termux & Linux environments. It performs intelligent surface mapping, identifies exposed perimeter services, and leverages Google DeepMind's Gemini reasoning models to generate enterprise-grade vulnerability audits and developer remediation roadmaps.

---

### 🚀 Core Capabilities
- **Automated Host Mapping:** Real-time DNS resolution and HTTP/HTTPS security header hygiene inspection.
- **Port Reconnaissance:** Socket-based scanner covering enterprise attack-surface ports (HTTP, SSH, MySQL, FTP, etc.).
- **Subdomain Intelligence:** Discovers active perimeter assets and shadow infrastructure.
- **AI-Powered Defensive Audits:** Generates severity-ranked vulnerability assessments, architectural gap analyses, and step-by-step remediation plans.
- **Audit Archival:** Automatically saves formatted client-ready audit reports (report_<domain>.txt).
- **Interactive CLI Dashboard:** Clean terminal navigation for modular and deep scanning workflows.

---

### ⚙️ Quick Installation & Setup

```bash
# Clone the repository
git clone [https://github.com/skraj748487-blip/BharatDef-AI-.git](https://github.com/skraj748487-blip/BharatDef-AI-.git)
cd BharatDef-AI-

# Install required dependencies
pkg install python git -y
pip install requests

# Set your Gemini API Key
export GEMINI_API_KEY="YOUR_API_KEY"

# Launch the Engine
python engine.py

