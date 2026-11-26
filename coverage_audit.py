"""Read-only coverage audit for explicitly supplied date windows."""
import datetime as dt
from collections import Counter

def audit(rows, game, start, end, weekdays, sessions):
    """Return missing and duplicate draw keys; caller supplies verified schedule.
    
    Dates are inclusive. No historical schedule or archive completeness is assumed.
    """
    start, end = dt.date.fromisoformat(start), dt.date.fromisoformat(end)
    weekdays, sessions = set(weekdays), set(sessions)
    if start > end or not weekdays or not weekdays <= set(range(7)):
        raise ValueError("Invalid date window or weekdays")
    if not sessions or not sessions <= {"midday", "evening"}:
        raise ValueError("Invalid sessions")
    expected = set()
    day = start
    while day <= end:
        if day.weekday() in weekdays:
            expected.update((day.isoformat(), s) for s in sessions)
        if day == end:
            break
        day += dt.timedelta(days=1)
    counts = Counter((r[1], r[2]) for r in rows if r[0] == game
                     and start <= dt.date.fromisoformat(r[1]) <= end)
    return {"expected": len(expected), "observed": len(expected & counts.keys()),
            "missing": sorted(expected - counts.keys()),
            "unexpected": sorted(counts.keys() - expected),
            "duplicates": sorted(k for k, n in counts.items() if n > 1)}
