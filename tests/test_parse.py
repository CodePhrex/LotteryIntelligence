import unittest
from lottery import parse
class Tests(unittest.TestCase):
    def test_optional_multiplier(self):
        row=next(parse('mega_millions','Mega Millions,4,8,2025,1,2,3,4,5,6','fixture'))
        self.assertEqual(row[1:6],('2025-04-08','evening','1 2 3 4 5','6',''))
    def test_multiplier(self):
        row=next(parse('powerball','Powerball,1,1,2020,5,4,3,2,1,6,2','fixture'))
        self.assertEqual(row[3:6],('1 2 3 4 5','6','2'))
