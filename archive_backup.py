"""Create a consistent, non-overwriting SQLite archive snapshot."""
import argparse
import pathlib
import sqlite3
import tempfile
import os


def backup(source, destination):
    source = pathlib.Path(source).resolve(strict=True)
    destination = pathlib.Path(destination).resolve()
    if destination.exists():
        raise FileExistsError(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(dir=destination.parent, suffix=".sqlite")
    os.close(fd)
    temporary = pathlib.Path(name)
    try:
        with sqlite3.connect(source.as_uri() + "?mode=ro", uri=True) as src:
            with sqlite3.connect(temporary) as dst:
                src.backup(dst)
                if dst.execute("PRAGMA integrity_check").fetchall() != [("ok",)]:
                    raise ValueError("Backup integrity check failed")
                dst.execute("SELECT game, draw_date, session, numbers, bonus, multiplier, source FROM draws LIMIT 0")
            dst.close()
        src.close()
        # Hard link publishes atomically without replacing an existing backup.
        os.link(temporary, destination)
        return destination
    finally:
        temporary.unlink(missing_ok=True)


if __name__ == "__main__":
    from lottery import DATA
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=pathlib.Path)
    args = parser.parse_args()
    print(backup(DATA / "draws.sqlite", args.destination))
