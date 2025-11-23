import re
import json
import os

def load_ipc_data():
    json_path = os.path.join(os.path.dirname(__file__), "ipc_data.json")
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

def extract_ipc_sections(text):
    ipc_data = load_ipc_data()
    found = re.findall(r'(?:IPC|Section)?\s*(\d+[A-Z]?)', text, re.IGNORECASE)
    results = []
    seen = set()
    for sec in found:
        sec = sec.upper()
        if sec in seen or sec not in ipc_data:
            continue
        seen.add(sec)
        results.append({
            "section": f"IPC {sec}",
            "description": ipc_data[sec].get("description", "No description available"),
            "punishment": ipc_data[sec].get("punishment", "No punishment available")
        })
    return results