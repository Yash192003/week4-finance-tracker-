import unittest
from finance_tracker.expense import Expense

class TestExpense(unittest.TestCase):
    def test_to_from_dict(self):
        data = {
            "id": 1,
            "date": "2026-01-01",
            "amount": 100.5,
            "category": "Food",
            "description": "Lunch",
        }
        exp = Expense.from_dict(data)
        self.assertEqual(exp.id, 1)
        self.assertEqual(exp.category, "Food")
        back = exp.to_dict()
        self.assertEqual(back["amount"], 100.5)

if __name__ == "__main__":
    unittest.main()
