import sqlite3
import tempfile
import unittest
from pathlib import Path
from contextlib import closing
from dashboard_backup import create_backup

class DashboardBackupTests(unittest.TestCase):
    def test_unique_backups(self):
        with tempfile.TemporaryDirectory() as root:
            root = Path(root)
            with closing(sqlite3.connect(root / "draws.sqlite")) as db, db:
                db.execute("CREATE TABLE draws(numbers TEXT)")
                db.execute("INSERT INTO draws VALUES ('007')")
            first, second = create_backup(root), create_backup(root)
            self.assertNotEqual(first, second)
            self.assertEqual(first.parent, root / "backups")
            for path in (first, second):
                with closing(sqlite3.connect(path)) as db:
                    self.assertEqual(db.execute("SELECT numbers FROM draws").fetchone(), ("007",))
    def test_missing_database(self):
        with tempfile.TemporaryDirectory() as root:
            with self.assertRaises(FileNotFoundError):
                create_backup(root)
            self.assertFalse((Path(root) / "backups").exists())
