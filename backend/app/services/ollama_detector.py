import shutil
import subprocess
import httpx
from typing import List, Dict

def is_ollama_installed() -> bool:
    """Check if the Ollama binary exists in the system PATH."""
    return shutil.which("ollama") is not None

def is_ollama_running() -> bool:
    """Check if the Ollama service is reachable on the default port."""
    try:
        resp = httpx.get("http://localhost:11434/api/tags", timeout=1.0)
        return resp.status_code == 200
    except Exception:
        return False

def get_ollama_models() -> List[Dict]:
    """Return a list of model info dictionaries from Ollama if reachable."""
    try:
        resp = httpx.get("http://localhost:11434/api/tags", timeout=2.0)
        if resp.status_code == 200:
            data = resp.json()
            return data.get("models", [])
    except Exception:
        pass
    return []

def get_status() -> Dict:
    """Return a unified status dict for Ollama detection."""
    installed = is_ollama_installed()
    running = is_ollama_running() if installed else False
    models = get_ollama_models() if running else []
    return {"installed": installed, "running": running, "models": models}
