from collections import defaultdict
from typing import List, Dict, Any, Optional
from datetime import datetime

class Reports:
    """Generates summaries and statistics."""

    @staticmethod
    def monthly_summary(expenses: List[Dict[str, Any]], year_month: Optional[str] = None) -> Dict[str, Any]:
        if not year_month:
            year_month = datetime.now().strftime("%Y-%m")
        monthly = [e for e in expenses if e["date"].startswith(year_month)]
        total = sum(float(e["amount"]) for e in monthly)
        cat_breakdown = defaultdict(float)
        for e in monthly:
            cat_breakdown[e["category"]] += float(e["amount"])
        return {
            "year_month": year_month,
            "total": total,
            "count": len(monthly),
            "by_category": dict(cat_breakdown),
        }

    @staticmethod
    def category_breakdown(expenses: List[Dict[str, Any]], budget: Dict[str, float]) -> Dict[str, Any]:
        """All‑time category breakdown with budget comparison."""
        totals = defaultdict(float)
        for e in expenses:
            totals[e["category"]] += float(e["amount"])

        total_spent = sum(totals.values())
        result: Dict[str, Any] = {}

        for cat, amt in totals.items():
            pct = (amt / total_spent * 100) if total_spent > 0 else 0.0
            over = amt - budget.get(cat, 0.0)
            result[cat] = {
                "amount": amt,
                "percentage": pct,
                "over_budget": over,
            }
        return result

    @staticmethod
    def statistics(expenses: List[Dict[str, Any]]) -> Dict[str, float]:
        if not expenses:
            return {"total": 0.0, "average": 0.0, "count": 0}
        total = sum(float(e["amount"]) for e in expenses)
        count = len(expenses)
        avg = total / count
        return {"total": total, "average": avg, "count": count}
