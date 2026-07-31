import tempfile
import unittest
from pathlib import Path

from guardian.memory.sqlite_storage import SQLiteStorage


class TestSQLiteStorage(unittest.TestCase):
    def test_append_and_get(self):
        with tempfile.TemporaryDirectory() as d:
            store = SQLiteStorage(str(Path(d) / "test.db"))
            store.append("agent-1", {"decision": "ALLOW", "risk_score": 5.0})
            store.append("agent-1", {"decision": "BLOCK", "risk_score": 95.0})
            records = store.get("agent-1")
            self.assertEqual(len(records), 2)
            self.assertEqual(records[0]["decision"], "ALLOW")
            self.assertEqual(records[1]["decision"], "BLOCK")

    def test_keys_are_isolated(self):
        with tempfile.TemporaryDirectory() as d:
            store = SQLiteStorage(str(Path(d) / "test.db"))
            store.append("agent-a", {"x": 1})
            store.append("agent-b", {"x": 2})
            self.assertEqual(len(store.get("agent-a")), 1)
            self.assertEqual(len(store.get("agent-b")), 1)

    def test_unknown_key_returns_empty_list(self):
        with tempfile.TemporaryDirectory() as d:
            store = SQLiteStorage(str(Path(d) / "test.db"))
            self.assertEqual(store.get("never-seen"), [])

    def test_persists_across_instances(self):
        """The whole point of this backend: data survives a process restart."""
        with tempfile.TemporaryDirectory() as d:
            db_path = str(Path(d) / "test.db")
            store1 = SQLiteStorage(db_path)
            store1.append("agent-1", {"decision": "WARN"})
            store1.close()

            store2 = SQLiteStorage(db_path)  # simulates a fresh process
            records = store2.get("agent-1")
            self.assertEqual(len(records), 1)
            self.assertEqual(records[0]["decision"], "WARN")

    def test_creates_parent_directory(self):
        with tempfile.TemporaryDirectory() as d:
            nested_path = str(Path(d) / "nested" / "dir" / "test.db")
            store = SQLiteStorage(nested_path)  # should not raise
            store.append("k", {"v": 1})
            self.assertEqual(len(store.get("k")), 1)


if __name__ == "__main__":
    unittest.main()
