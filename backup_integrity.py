"""Non-destructive SQLite snapshots using the online backup API."""
import pathlib
import sqlite3
import tempfile
import os

def snapshot(source, destination):
    source, destination = pathlib.Path(source).resolve(), pathlib.Path(destination).resolve()
    if not source.is_file():
        raise FileNotFoundError(source)
    if destination.exists():
        raise FileExistsError(destination)
    fd, name = tempfile.mkstemp(prefix=".snapshot-", dir=destination.parent)
    os.close(fd)
    try:
        with sqlite3.connect(source.as_uri()+"?mode=ro", uri=True) as src:
            with sqlite3.connect(name) as dst:
                src.backup(dst)
                if dst.execute("PRAGMA integrity_check").fetchone() != ("ok",):
                    raise ValueError("Snapshot integrity check failed")
        # Hard-link publication is atomic and refuses an existing destination.
        os.link(name, destination)
    finally:
        os.unlink(name)
    return destination
