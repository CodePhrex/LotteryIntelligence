import unittest
from coverage_audit import audit

class CoverageTests(unittest.TestCase):
    def test_sessions_and_duplicates(self):
        rows = [('michigan_daily_3','2026-01-01','midday','007'),
                ('michigan_daily_3','2026-01-01','midday','007'),
                ('michigan_daily_4','2026-01-01','evening','0007')]
        result = audit(rows,'michigan_daily_3','2026-01-01','2026-01-01',
                       range(7),['midday','evening'])
        self.assertEqual(result['expected'],2)
        self.assertEqual(result['observed'],1)
        self.assertEqual(result['missing'],[('2026-01-01','evening')])
        self.assertEqual(result['duplicates'],[('2026-01-01','midday')])
    def test_weekday_and_unexpected(self):
        result = audit([('powerball','2026-01-02','evening')], 'powerball',
                       '2026-01-01','2026-01-03',[5],['evening'])
        self.assertEqual(result['missing'],[('2026-01-03','evening')])
        self.assertEqual(result['unexpected'],[('2026-01-02','evening')])
    def test_invalid_window(self):
        with self.assertRaises(ValueError):
            audit([], 'powerball','2026-01-03','2026-01-01',[5],['evening'])
