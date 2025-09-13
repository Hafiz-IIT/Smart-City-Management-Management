# app/services/store.py
from __future__ import annotations
import json
from pathlib import Path
from typing import List
from app.core.models import Incident

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
INC_FILE = DATA_DIR / "incidents.json"

DATA_DIR.mkdir(parents=True, exist_ok=True)
if not INC_FILE.exists():
    INC_FILE.write_text("[]", encoding="utf-8")

def read_incidents() -> List[Incident]:
    raw = json.loads(INC_FILE.read_text(encoding="utf-8"))
    return [Incident(**x) for x in raw]

def write_incidents(items: List[Incident]) -> None:
    INC_FILE.write_text(json.dumps([x.model_dump() for x in items], indent=2), encoding="utf-8")
