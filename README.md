# Security Tools

A small collection of standalone Python utilities for threat intelligence, network defense, and file metadata inspection. Each script is self-contained and can be run independently.

## Contents

### `pulse2yara.py`
Pulls threat indicators from an AlienVault OTX (Open Threat Exchange) pulse via its API and converts them into two usable outputs:
- A CSV export of all indicators (type + value)
- A generated YARA rule file matching the indicator strings

Useful for quickly turning shared threat intel into detection rules.

**Requirements:** `requests`, `yara-python`
**Usage:**
```bash
python pulse2yara.py
# Enter the OTX pulse ID when prompted
```
> Set your own OTX API key in the `api_key` variable before running.

---

### `minifw_netsh.py`
A lightweight, interactive command-line firewall manager for Windows, built on top of `netsh advfirewall`. Lets you:
- Allow or block traffic by protocol/port
- Block or unblock specific IP addresses
- Export all current firewall rules to a CSV file for review

**Requirements:** Windows, run with administrator privileges
**Usage:**
```bash
python minifw_netsh.py
```

---

### `Right-Click Image EXIF Viewer.js`
A quick-access script for viewing EXIF metadata embedded in JPG/JPEG images directly via a right-click context menu action — useful for fast privacy/forensics checks without opening a full image editor.

---

## License
See [LICENSE](./LICENSE).
