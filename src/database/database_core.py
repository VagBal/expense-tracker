from src.expense.expense_core import Expense
from src.database.database_maker import DatabaseMaker, DB_FILE_PATH, CSV_FILE_PATH
from enum import Enum
import datetime
import json
import csv
from prettytable import PrettyTable
import threading

class States(Enum):
    INACTIVE = 0
    ACTIVE = 1

class Database:
    _lock = threading.Lock()
    state = None
    database = None
    id = 0
    database_maker = None
    instance = None

    def __new__(cls):
        if cls.instance is None:
            with cls._lock:
                if cls.instance is None:  # Double-checked locking
                    cls.instance = super(Database, cls).__new__(cls)
                    cls.instance.init_database()
        return cls.instance
    
    def init_database(self):
        self.state = States.ACTIVE
        self.database_maker = DatabaseMaker()
        if not self.database_maker.is_db_file_exists():
            self.database_maker.make_a_new_db()
        self.load_db_from_file(DB_FILE_PATH)
        self.id = self.get_last_id()
    
    def get_last_id(self):
        """Get the last used ID from the database."""
        if self.database["expenses"]:
            return max(expense["id"] for expense in self.database["expenses"])
        return 0

    def get_state(self):
        return self.state
    
    def load_db_from_file(self, file_path):
        try:
            with open(file_path, mode='r', encoding="utf-8") as read_file:
                self.database = json.load(read_file)
        except Exception as e:
            print(f"An error occurred while loading the database: {e}")

    def add_an_expense(self, description: str, amount: float, category: str):
        with self._lock:
            self.id += 1
            expense = Expense(
                id=self.id, 
                description=description, 
                amount=amount, 
                category=category, 
                created_at=datetime.datetime.now().isoformat()
            )
            expense_dict = expense.as_dict()
            self.database["expenses"].append(expense_dict)
            self.database_maker.update_an_existing_db(self.database)
            print(f"A new expense has been added with ID:{self.id}")

        current_month = datetime.datetime.now().month
        monthly_budget = next((budget["budget"] for budget in self.database["monthly_budgets"] if budget["id"] == current_month), 0)
        current_budget = sum(expense["amount"] for expense in self.database["expenses"] if expense["month"] == current_month)

        if current_budget > monthly_budget:
            print(f"The current budget: {current_budget} exceeds the monthly budget: {monthly_budget} for this month: {self.get_month_name_by_id(current_month)}")

    def get_month_name_by_id(self, month_id):
        return next((month["name"] for month in self.database["monthly_budgets"] if month["id"] == month_id), "Unknown")

    def delete_an_expense(self, id: int):
        try:
            with self._lock:
                self.database["expenses"] = [expense for expense in self.database["expenses"] if expense["id"] != id]
                self.database_maker.update_an_existing_db(self.database)
                print(f"The expense with ID:{id} has been deleted")
        except Exception as e:
            print(f"An error occurred: {e} while deleting the expense with id: {id}")

    def update_an_expense_amount(self, id: int, amount: float):
        try: 
            with self._lock:
                expense = self.find_expense_by_id(id)
                expense["amount"] = amount
                print(f"The expense's amount with ID:{id} has been updated to {amount}")
                self.database_maker.update_an_existing_db(self.database)
        except ValueError as e: 
            print(e)

    def update_an_expense_description(self, id: int, description: str):
        try: 
            with self._lock:
                expense = self.find_expense_by_id(id)
                expense["description"] = description
                print(f"The expense's description with ID:{id} has been updated to {description}")
                self.database_maker.update_an_existing_db(self.database)
        except ValueError as e: 
            print(e)

    def update_an_expense_category(self, id: int, category: str):
        try: 
            with self._lock:
                expense = self.find_expense_by_id(id)
                expense["category"] = category
                print(f"The expense's category with ID:{id} has been updated to {category}")
                self.database_maker.update_an_existing_db(self.database)
        except ValueError as e: 
            print(e)

    def find_expense_by_id(self, id: int, type="no_print"):
        expense = next((expense for expense in self.database["expenses"] if expense["id"] == id), None)
        if expense:
            if type == "print":
                self.tablify([expense])
            return expense
        raise ValueError(f"Expense with ID:{id} not found")

    def set_budget_for_a_month(self, month: str, budget: int):
        try:
            with self._lock:
                month_data = next((m for m in self.database["monthly_budgets"] if m["name"] == month), None)
                if month_data and month_data["budget"] != budget:
                    month_data["budget"] = budget
                    print(f"The monthly budget of {month} has been updated to {budget}$")
                    self.database_maker.update_an_existing_db(self.database)
        except ValueError as e: 
            print(e)
        
    def summary_expenses(self, data, filter="all"):
        expenses = self.database.get("expenses", [])

        if not expenses:
            print("No expenses available.")
            return

        filtered_expenses = expenses if filter == "all" else [expense for expense in expenses if expense.get(filter) == data]
        
        if not filtered_expenses:
            print(f"The expenses cannot be summarized by {filter}" if filter else "No expenses available.")
            return

        sum_of_expenses = sum(expense["amount"] for expense in filtered_expenses)
        
        print(f"The sum of expenses for the given filter: {filter} is {sum_of_expenses}$")

    def export_expenses(self, type: str):
        if type == "csv":
            try:
                with open(DB_FILE_PATH) as json_file:
                    json_data = json.load(json_file)
                with open(CSV_FILE_PATH, 'w', newline='') as data_file:
                    csv_writer = csv.writer(data_file)
                    count = 0
                    for data in json_data["expenses"]:
                        if count == 0:
                            header = data.keys()
                            csv_writer.writerow(header)
                            count += 1
                        csv_writer.writerow(data.values())

                print(f"The expense database has been exported to a CSV to {CSV_FILE_PATH}")
            except Exception as e:
                print(f"An error occurred while exporting to CSV: {e}")
        else:
            print("Invalid file type. Only CSV is supported for now.")

    def list_expenses(self, filter=None, filter_value=None):
        expenses = self.database.get("expenses", [])
        if not expenses:
            print("No expenses available.")
            return

        # Filtering logic
        if filter is None:
            filtered_expenses = expenses
        elif filter == "category":
            filtered_expenses = [expense for expense in expenses if expense["category"].lower() == filter_value.lower()]
        elif filter == "month":
            month_id = [budget["id"] for budget in self.database.get("monthly_budgets", []) if budget["name"] == filter_value]
            filtered_expenses = [expense for expense in expenses if expense["month"] == month_id[0]]
        else:
            filtered_expenses = []

        if not filtered_expenses:
            print(f"No expenses found for the given filter: {filter} with value: {filter_value}")
            return

        self.tablify(filtered_expenses)

    
    def tablify(self, data):
        table = PrettyTable()
        table.field_names = ["id", "description", "amount", "category", "created_at"]

        for expense in data:
            table.add_row([expense["id"], expense["description"], expense["amount"], expense["category"], expense["created_at"]])

        print(table)
