import pathlib
import sqlite3
import tempfile
import unittest
from archive_backup import backup


class BackupTests(unittest.TestCase):
    def test_snapshot_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            source, target = root / "source.sqlite", root / "backup.sqlite"
            db = sqlite3.connect(source)
            try:
                db.execute("CREATE TABLE draws(game, draw_date, session, numbers, bonus, multiplier, source)")
                db.execute("INSERT INTO draws VALUES(?,?,?,?,?,?,?)", ("test", "2000-01-01", "midday", "001", "", "", "synthetic test"))
                db.commit()
                backup(source, target)
                db.execute("DELETE FROM draws")
                db.commit()
                copy = sqlite3.connect(target)
                try:
                    self.assertEqual(copy.execute("SELECT numbers FROM draws").fetchone(), ("001",))
                finally:
                    copy.close()
                with self.assertRaises(FileExistsError):
                    backup(source, target)
            finally:
                db.close()

    def test_missing_source(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            with self.assertRaises(FileNotFoundError):
                backup(root / "missing.sqlite", root / "backup.sqlite")
            self.assertFalse((root / "backup.sqlite").exists())
