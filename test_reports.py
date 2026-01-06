import unittest
from finance_tracker.reports import Reports

class TestReports(unittest.TestCase):
    def setUp(self):
        self.expenses = [
            {"id": 1, "date": "2026-01-01", "amount": 100.0, "category": "Food", "description": "A"},
            {"id": 2, "date": "2026-01-05", "amount": 200.0, "category": "Transport", "description": "B"},
        ]

    def test_statistics(self):
        stats = Reports.statistics(self.expenses)
        self.assertEqual(stats["count"], 2)
        self.assertAlmostEqual(stats["total"], 300.0)

if __name__ == "__main__":
    unittest.main()
