import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest.mock import patch
from App.Core.Models import Incident
from App.Services import store
class AtomicStoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.patches = [patch.object(store, "DATA_DIR", self.root),
                        patch.object(store, "INC_FILE", self.root / "incidents.json")]
        for item in self.patches: item.start()
        store.write_incidents([])
    def tearDown(self):
        for item in reversed(self.patches): item.stop()
        self.temp.cleanup()
    def make_incident(self, index):
        return Incident(id=f"I{index}", ward="A", type="pothole",
            description=f"Demo report {index}", lat=22.56, lng=88.39,
            createdAt=1700000000000 + index)
    def test_round_trip(self):
        store.write_incidents([self.make_incident(1)])
        self.assertEqual(store.read_incidents()[0].id, "I1")
    def test_concurrent_mutations_do_not_lose_updates(self):
        def add(index):
            store.mutate_incidents(lambda rows: rows.append(self.make_incident(index)))
        with ThreadPoolExecutor(max_workers=8) as pool: list(pool.map(add, range(30)))
        self.assertEqual(len(store.read_incidents()), 30)
if __name__ == "__main__": unittest.main()
