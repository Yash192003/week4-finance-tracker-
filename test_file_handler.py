import os
import unittest
from finance_tracker.file_handler import FileHandler
from finance_tracker.utils import DATA_FILE

class TestFileHandler(unittest.TestCase):
    def test_save_and_load_expenses(self):
        test_items = [
            {"id": 1, "date": "2026-01-01", "amount": 10.0, "category": "Food", "description": "Test"}
        ]
        FileHandler.save_expenses(test_items)
        loaded = FileHandler.load_expenses()
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0]["category"], "Food")
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)

if __name__ == "__main__":
    unittest.main()
