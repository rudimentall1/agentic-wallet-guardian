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
            assert len(records) == 2
            assert records[0]["decision"] == "ALLOW"
            assert records[1]["decision"] == "BLOCK"
            store.close()

    def test_keys_are_isolated(self):
        with tempfile.TemporaryDirectory() as d:
            store = SQLiteStorage(str(Path(d) / "test.db"))
            store.append("agent-a", {"x": 1})
            store.append("agent-b", {"x": 2})
            assert len(store.get("agent-a")) == 1
            assert len(store.get("agent-b")) == 1
            store.close()

    def test_unknown_key_returns_empty_list(self):
        with tempfile.TemporaryDirectory() as d:
            store = SQLiteStorage(str(Path(d) / "test.db"))
            assert store.get("never-seen") == []
            store.close()

    def test_persists_across_instances(self):
        with tempfile.TemporaryDirectory() as d:
            db_path = str(Path(d) / "test.db")
            store1 = SQLiteStorage(db_path)
            store1.append("agent-1", {"decision": "WARN"})
            store1.close()

            store2 = SQLiteStorage(db_path)
            records = store2.get("agent-1")
            assert len(records) == 1
            assert records[0]["decision"] == "WARN"
            store2.close()

    def test_creates_parent_directory(self):
        with tempfile.TemporaryDirectory() as d:
            nested_path = str(Path(d) / "nested" / "dir" / "test.db")
            store = SQLiteStorage(nested_path)
            store.append("k", {"v": 1})
            assert len(store.get("k")) == 1
            store.close()


if __name__ == "__main__":
    unittest.main()
