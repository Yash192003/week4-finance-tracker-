from datetime import datetime
from .expense_manager import ExpenseManager
from .file_handler import FileHandler
from .reports import Reports
from .utils import CATEGORIES

class FinanceTracker:
    def __init__(self) -> None:
        self.manager = ExpenseManager()
        self.budget: dict[str, float] = {}
        self._load_on_startup()

    def _load_on_startup(self) -> None:
        # Load expenses
        expenses_data = FileHandler.load_expenses()
        self.manager.load_from_dicts(expenses_data)
        # Load budget
        self.budget = FileHandler.load_budget()

    def _save_all(self) -> None:
        FileHandler.save_expenses(self.manager.to_dicts())
        FileHandler.save_budget(self.budget)

    def run(self) -> None:
        print("=" * 60)
        print("          PERSONAL FINANCE TRACKER")
        print("=" * 60)

        while True:
            print("\n" + "=" * 40)
            print("              MAIN MENU")
            print("=" * 40)
            print("1. Add New Expense")
            print("2. View All Expenses")
            print("3. Search Expenses")
            print("4. Generate Monthly Report")
            print("5. View Category Breakdown")
            print("6. Set/Update Budget")
            print("7. Export Data to CSV")
            print("8. View Statistics")
            print("9. Backup/Restore Data")
            print("0. Exit")
            print("=" * 40)

            choice = input("\nEnter your choice (0-9): ").strip()

            if choice == "1":
                self.add_expense()
            elif choice == "2":
                self.view_expenses()
            elif choice == "3":
                self.search_expenses()
            elif choice == "4":
                self.generate_monthly_report()
            elif choice == "5":
                self.view_category_breakdown()
            elif choice == "6":
                self.set_budget()
            elif choice == "7":
                self.export_data()
            elif choice == "8":
                self.view_statistics()
            elif choice == "9":
                self.backup_restore()
            elif choice == "0":
                self._save_all()
                print("\n" + "=" * 60)
                print("Thank you for using Personal Finance Tracker!")
                print("=" * 60)
                break
            else:
                print("Invalid choice! Please enter 0-9.")
            input("\nPress Enter to continue...")

    # -------- menu actions --------

    def add_expense(self) -> None:
        print("\n--- ADD NEW EXPENSE ---")
        try:
            date_str = input("Date (YYYY-MM-DD) [today]: ").strip()
            if not date_str:
                date_str = datetime.now().strftime("%Y-%m-%d")

            amount_str = input("Amount: ").strip()
            amount = float(amount_str)

            print("Categories:", ", ".join(CATEGORIES))
            category = input("Category: ").strip()

            description = input("Description: ").strip()

            expense = self.manager.add_expense(date_str, amount, category, description)
            self._save_all()
            print(f"Expense #{expense.id} added successfully!")
        except ValueError as e:
            print(f"Error: {e}")

    def view_expenses(self) -> None:
        print("\n--- ALL EXPENSES ---")
        expenses = self.manager.get_all()
        if not expenses:
            print("No expenses recorded yet.")
            return
        for e in expenses[-20:]:
            print(
                f"ID: {e.id} | {e.date} | ₹{e.amount:.2f} | "
                f"{e.category} | {e.description}"
            )

    def search_expenses(self) -> None:
        print("\n--- SEARCH EXPENSES ---")
        keyword = input("Enter keyword (date/category/description): ").strip()
        results = self.manager.search(keyword)
        if not results:
            print("No matching expenses found.")
            return
        for e in results:
            print(
                f"ID: {e.id} | {e.date} | ₹{e.amount:.2f} | "
                f"{e.category} | {e.description}"
            )

    def generate_monthly_report(self) -> None:
        print("\n--- MONTHLY REPORT ---")
        ym = input("Year-Month (YYYY-MM) [current]: ").strip()
        if not ym:
            ym = datetime.now().strftime("%Y-%m")

        data = Reports.monthly_summary(self.manager.to_dicts(), ym)
        print(f"\nReport for {data['year_month']}")
        print(f"Total expenses: ₹{data['total']:.2f}")
        print(f"Number of expenses: {data['count']}")
        if data["count"] == 0:
            return
        print("\nCategory-wise breakdown:")
        for cat, amt in data["by_category"].items():
            print(f"  {cat}: ₹{amt:.2f}")

    def view_category_breakdown(self) -> None:
        print("\n--- CATEGORY BREAKDOWN (ALL TIME) ---")
        data = Reports.category_breakdown(self.manager.to_dicts(), self.budget)
        if not data:
            print("No expenses recorded yet.")
            return
        total = sum(v["amount"] for v in data.values())
        print(f"Total spent: ₹{total:.2f}\n")
        for cat, info in data.items():
            status = "✅" if info["over_budget"] <= 0 else "❌"
            print(
                f"{cat}: ₹{info['amount']:.2f} "
                f"({info['percentage']:.1f}%) | Over budget: ₹{info['over_budget']:.2f} {status}"
            )

    def set_budget(self) -> None:
        print("\n--- SET/UPDATE BUDGET ---")
        for cat in CATEGORIES:
            current = self.budget.get(cat, 0.0)
            raw = input(f"{cat} monthly budget [current: ₹{current:.2f}]: ").strip()
            if raw:
                try:
                    self.budget[cat] = float(raw)
                except ValueError:
                    print(f"Invalid amount for {cat}, keeping existing.")
        self._save_all()
        print("Budget updated successfully!")

    def export_data(self) -> None:
        print("\n--- EXPORT DATA TO CSV ---")
        path = FileHandler.export_to_csv(self.manager.to_dicts())
        print(f"Data exported to: {path}")

    def view_statistics(self) -> None:
        print("\n--- STATISTICS ---")
        stats = Reports.statistics(self.manager.to_dicts())
        if stats["count"] == 0:
            print("No expenses recorded yet.")
            return
        print(f"Total spent: ₹{stats['total']:.2f}")
        print(f"Average expense: ₹{stats['average']:.2f}")
        print(f"Number of expenses: {stats['count']}")

    def backup_restore(self) -> None:
        print("\n--- BACKUP/RESTORE ---")
        print("1. Create Backup")
        print("2. Restore From Backup")
        choice = input("Enter your choice (1-2): ").strip()
        if choice == "1":
            FileHandler.backup()
            print("Backup created successfully.")
        elif choice == "2":
            FileHandler.restore()
            self._load_on_startup()
            print("Data restored from backup.")
        else:
            print("Invalid choice.")
