import unittest
from draw_analytics import frequencies

class FrequencyTests(unittest.TestCase):
    def test_digits(self):
        game = "michigan_daily_3"
        result = frequencies(game, [{"game": game, "numbers": "007"}])
        self.assertEqual(result["main"], {"0": 2, "7": 1})
        self.assertEqual(result["positions"][1], {"0": 1})
        self.assertEqual(result["draws"], 1)

    def test_bonus(self):
        game = "powerball"
        result = frequencies(game, [{"game": game, "numbers": "1 2 3 4 5", "bonus": "1"}])
        self.assertEqual(result["main"]["1"], 1)
        self.assertEqual(result["bonus"], {"1": 1})

    def test_mixed_games(self):
        with self.assertRaises(ValueError):
            frequencies("powerball", [{"game": "mega_millions"}])

    def test_empty(self):
        self.assertEqual(frequencies("powerball", [])["draws"], 0)
