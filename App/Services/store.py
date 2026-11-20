from __future__ import annotations
import json
import os
import tempfile
from pathlib import Path
from threading import RLock
from typing import Callable, List, TypeVar
from App.Core.Models import Incident
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
INC_FILE = DATA_DIR / "incidents.json"
_STORE_LOCK = RLock()
T = TypeVar("T")
DATA_DIR.mkdir(parents=True, exist_ok=True)
if not INC_FILE.exists():
    INC_FILE.write_text("[]", encoding="utf-8")
def read_incidents() -> List[Incident]:
    with _STORE_LOCK:
        raw = json.loads(INC_FILE.read_text(encoding="utf-8"))
        if not isinstance(raw, list):
            raise ValueError("incident store must contain a JSON array")
        return [Incident(**item) for item in raw]
def write_incidents(items: List[Incident]) -> None:
    payload = json.dumps([item.model_dump(mode="json") for item in items], indent=2)
    with _STORE_LOCK:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        fd, temp_path = tempfile.mkstemp(prefix="incidents-", suffix=".tmp", dir=DATA_DIR)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temp_path, INC_FILE)
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
def mutate_incidents(mutator: Callable[[List[Incident]], T]) -> T:
    with _STORE_LOCK:
        items = read_incidents()
        result = mutator(items)
        write_incidents(items)
        return result
