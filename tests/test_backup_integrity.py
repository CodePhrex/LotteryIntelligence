import pathlib
import sqlite3
from contextlib import closing
import tempfile
import unittest
from backup_integrity import snapshot

class BackupTests(unittest.TestCase):
    def test_snapshot_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as folder:
            src = pathlib.Path(folder)/"source.sqlite"
            dst = pathlib.Path(folder)/"backup.sqlite"
            with closing(sqlite3.connect(src)) as db, db:
                db.execute("CREATE TABLE draws(numbers TEXT)")
                db.execute("INSERT INTO draws VALUES ('007')")
            snapshot(src,dst)
            with closing(sqlite3.connect(dst)) as db:
                self.assertEqual(db.execute("SELECT numbers FROM draws").fetchone(),("007",))
            with self.assertRaises(FileExistsError):
                snapshot(src,dst)
    def test_missing_source(self):
        with tempfile.TemporaryDirectory() as folder:
            src = pathlib.Path(folder)/"missing.sqlite"
            dst = pathlib.Path(folder)/"backup.sqlite"
            with self.assertRaises(FileNotFoundError):
                snapshot(src,dst)
            self.assertFalse(src.exists())
            self.assertFalse(dst.exists())
