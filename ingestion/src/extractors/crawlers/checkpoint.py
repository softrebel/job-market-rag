"""
Minimal per-source checkpoint so a crawler doesn't restart from zero
every run. Good enough to start with; swap for a DB table
(e.g. `crawl_state(source, last_url, last_run_at)`) once this needs
to run from multiple machines or survive container restarts cleanly.
"""

import json
from pathlib import Path
from config.settings import settings

# STATE_DIR = Path(__file__).resolve().parents[2] / ".state"
STATE_DIR = Path(settings.DATA_PATH)
STATE_DIR.mkdir(exist_ok=True)


def load_checkpoint(source_name: str) -> dict:
    path = STATE_DIR / f"{source_name}.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def save_checkpoint(source_name: str, data: dict) -> None:
    path = STATE_DIR / f"{source_name}.json"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2))
