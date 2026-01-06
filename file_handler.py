import json
import csv
import os
import shutil
from typing import List, Dict, Any
from .utils import DATA_FILE, BACKUP_FILE, BUDGET_FILE, EXPORT_DIR

class FileHandler:
    """Handles all file I/O: JSON, CSV, backup/restore."""

    @staticmethod
    def load_json_list(path: str) -> List[Dict[str, Any]]:
        if not os.path.exists(path):
            return []
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data if isinstance(data, list) else []
        except (json.JSONDecodeError, OSError):
            return []

    @staticmethod
    def load_json_dict(path: str) -> Dict[str, Any]:
        if not os.path.exists(path):
            return {}
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data if isinstance(data, dict) else {}
        except (json.JSONDecodeError, OSError):
            return {}

    @staticmethod
    def save_json(data: Any, path: str) -> None:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def export_to_csv(expenses: List[Dict[str, Any]]) -> str:
        os.makedirs(EXPORT_DIR, exist_ok=True)
        csv_path = os.path.join(EXPORT_DIR, "expenses.csv")
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["id", "date", "amount", "category", "description"],
            )
            writer.writeheader()
            writer.writerows(expenses)
        return csv_path

    @staticmethod
    def backup() -> None:
        os.makedirs(os.path.dirname(BACKUP_FILE) or ".", exist_ok=True)
        if os.path.exists(DATA_FILE):
            shutil.copy(DATA_FILE, BACKUP_FILE)

    @staticmethod
    def restore() -> None:
        if os.path.exists(BACKUP_FILE):
            os.makedirs(os.path.dirname(DATA_FILE) or ".", exist_ok=True)
            shutil.copy(BACKUP_FILE, DATA_FILE)

    # Convenience wrappers using default paths
    @classmethod
    def load_expenses(cls) -> List[Dict[str, Any]]:
        return cls.load_json_list(DATA_FILE)

    @classmethod
    def save_expenses(cls, items: List[Dict[str, Any]]) -> None:
        cls.save_json(items, DATA_FILE)

    @classmethod
    def load_budget(cls) -> Dict[str, float]:
        raw = cls.load_json_dict(BUDGET_FILE)
        return {k: float(v) for k, v in raw.items()}

    @classmethod
    def save_budget(cls, budget: Dict[str, float]) -> None:
        cls.save_json(budget, BUDGET_FILE)
