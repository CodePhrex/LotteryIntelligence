from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4
from backup_integrity import snapshot

def create_backup(data_dir):
    data_dir = Path(data_dir)
    source = data_dir / "draws.sqlite"
    if not source.is_file():
        raise FileNotFoundError(source)
    folder = data_dir / "backups"
    folder.mkdir(exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return snapshot(source, folder / f"draws-{stamp}-{uuid4().hex}.sqlite")
