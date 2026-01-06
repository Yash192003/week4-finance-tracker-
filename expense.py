from dataclasses import dataclass
from typing import Dict

@dataclass
class Expense:
    id: int
    date: str      # "YYYY-MM-DD"
    amount: float
    category: str
    description: str

    @classmethod
    def from_dict(cls, data: Dict) -> "Expense":
        return cls(
            id=data["id"],
            date=data["date"],
            amount=float(data["amount"]),
            category=data["category"],
            description=data.get("description", ""),
        )

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "date": self.date,
            "amount": float(self.amount),
            "category": self.category,
            "description": self.description,
        }
