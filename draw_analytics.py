"""Descriptive counts only; no prediction or probability adjustment."""
from collections import Counter

def frequencies(game, rows):
    main, bonus = Counter(), Counter()
    positions = {}
    count = 0
    for row in rows:
        if row["game"] != game:
            raise ValueError("Mixed games")
        numbers = row["numbers"]
        if game in ("michigan_daily_3", "michigan_daily_4"):
            if len(numbers) != int(game[-1]) or not numbers.isascii() or not numbers.isdigit():
                raise ValueError("Invalid Michigan digits")
            for i, digit in enumerate(numbers, 1):
                positions.setdefault(i, Counter())[digit] += 1
            main.update(numbers)
        elif game in ("powerball", "mega_millions"):
            balls = [str(int(n)) for n in numbers.split()]
            if len(balls) != 5 or len(set(balls)) != 5:
                raise ValueError("Invalid main balls")
            main.update(balls)
            bonus[str(int(row["bonus"]))] += 1
        else:
            raise ValueError("Unknown game")
        count += 1
    return {"draws": count, "main": dict(main), "bonus": dict(bonus),
            "positions": {i: dict(c) for i, c in positions.items()}}
