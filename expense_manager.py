from typing import List, Dict
from datetime import datetime
from .expense import Expense
from .utils import CATEGORIES

class ExpenseManager:
    """Handles in-memory expense collection and validation."""

    def __init__(self) -> None:
        self.expenses: List[Expense] = []

    def load_from_dicts(self, items: List[Dict]) -> None:
        self.expenses = [Expense.from_dict(d) for d in items]

    def to_dicts(self) -> List[Dict]:
        return [e.to_dict() for e in self.expenses]

    def _validate_date(self, date_str: str) -> str:
        datetime.strptime(date_str, "%Y-%m-%d")  # raises if invalid
        return date_str

    def _normalize_category(self, category: str) -> str:
        cat = category.strip().title()
        return cat if cat in CATEGORIES else "Other"

    def add_expense(self, date: str, amount: float, category: str, desc: str) -> Expense:
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        date = self._validate_date(date)
        category = self._normalize_category(category)

        new_id = len(self.expenses) + 1
        expense = Expense(
            id=new_id,
            date=date,
            amount=float(amount),
            category=category,
            description=desc.strip(),
        )
        self.expenses.append(expense)
        return expense

    def get_all(self) -> List[Expense]:
        return list(self.expenses)

    def search(self, keyword: str) -> List[Expense]:
        kw = keyword.lower()
        results: List[Expense] = []
        for e in self.expenses:
            if (
                kw in e.category.lower()
                or kw in e.date
                or kw in e.description.lower()
            ):
                results.append(e)
        return results

    def filter_month(self, year_month: str) -> List[Expense]:
        """Filter by 'YYYY-MM' prefix."""
        return [e for e in self.expenses if e.date.startswith(year_month)]
