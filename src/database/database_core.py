from src.expense.expense_core import Expense
from src.database.database_maker import DatabaseMaker, DB_FILE_PATH, CSV_FILE_PATH
from enum import Enum
import datetime
import json
import csv
from prettytable import PrettyTable

class States(Enum):
    INVACTIVE = 0
    ACTIVE = 1

class Database:
    _state = None
    _database = None
    _id = int()
    _database_maker = None
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.init_database()
        return cls._instance
    
    def init_database(self):
        self._state = States.ACTIVE
        self._database_maker = DatabaseMaker()
        if self._database_maker.is_db_file_exists() is False:
            self._database_maker.make_a_new_db()

        self.load_db_from_file(DB_FILE_PATH)
        self._id = self.get_last_id()
    
    def get_last_id(self):
        """Get the last used ID from the database."""
        if self._database["expenses"]:
            return max(expense["id"] for expense in self._database["expenses"])
        return 0

    def get_state(self):
        return self._state
    
    def load_db_from_file(self, file_path):
        with open(file_path, mode='r', encoding="utf-8") as read_file:
            self._database = json.load(read_file)

    def add_an_expense(self, description: str, amount: int, category: str):
        self._id += 1
        month = int(datetime.datetime.now().month)
        expense = Expense(int(self._id), description, int(amount), category, str(datetime.datetime.now()), month)
        expense_dict = expense.as_dict()
        self._database["expenses"].append(expense_dict)
        self._database_maker.update_an_existing_db(self._database)
        print(f"A new expense has been added with ID:{self._id}")

        monthly_budget = 0
        for months in self._database["monthly_budgets"]:
            if months["id"] == month:
                monthly_budget = months["budget"]

        current_budget = 0
        for expense in self._database["expenses"]:
            if expense["month"] == month:
                current_budget += expense["amount"]
        
        if current_budget > monthly_budget:
            print(f"The current budget: {current_budget} is exceeded the monthly budget: {monthly_budget} for this month: {self.get_month_name_by_id(month)}")
        
    def get_month_name_by_id(self, month_id):
        for month in  self._database["monthly_budgets"]:
            if month["id"] == month_id:
                return month["name"]

    def delete_an_expense(self, id: int):
        try:
            self._database["expenses"] = [expense for expense in self._database["expenses"] if expense["id"] != id]
            self._database_maker.update_an_existing_db(self._database)
            print(f"The expense with ID:{id} has been deleted")
        except Exception as e:
            print(f"An error occurred: {e} with the expense with id: {id} deletion")

    def update_an_expense_amount(self, id: int, amount: int):
        try: 
            expense = self.find_task_by_id(id)
            expense["amount"] = amount
            print(f"The expense's amount with ID:{id} has been updated")
        except ValueError as e: 
            print(e)

        self._database_maker.update_an_existing_db(self._database)
    
    def update_an_expense_description(self, id: int, description: str):
        try: 
            expense = self.find_task_by_id(id)
            expense["description"] = description
            print(f"The expense's description with ID:{id} has been updated")
        except ValueError as e: 
            print(e)

        self._database_maker.update_an_existing_db(self._database)

    def update_an_expense_category(self, id: int, category: str):
        try: 
            expense = self.find_task_by_id(id)
            expense["category"] = category
            print(f"The expense's category with ID:{id} has been updated")
        except ValueError as e: 
            print(e)

        self._database_maker.update_an_existing_db(self._database)

    def find_expense_by_id(self, id: int):
        for expense in self._database["expenses"]:
            if expense["id"] == id:
                self.tablify(expense)
        raise ValueError(f"Expense with ID:{id} not found")

    def set_budget_for_a_month(self, month: str, budget: int):
        try: 
            for month in self._database["monthly_budgets"]:
                if month["name"] == month:
                    if month["budget"] != budget:
                        month["budget"] = budget
                        print(f"The monthly budget of {month} has been updated to {budget}$")
        except ValueError as e: 
            print(e)

        self._database_maker.update_an_existing_db(self._database)
        

    def is_budget_exceeded(self, budget: int) -> bool:
        pass

    def summary_expenses(self, data, filter="all"):
        expenses = self._database.get("expenses", [])

        if not expenses:
            print("No expenses available.")
            return

        if filter == "all":
            filtered_expenses = expenses 
        else: 
            filtered_expenses = [expense for expense in expenses if expense.get(filter) == data]
        
        if not filtered_expenses:
            print(f"The expenses cannot be summarized by {filter}" if filter else "No expenses available.")
            return

        sum_of_expenses = 0
        for expense in filtered_expenses:
            sum_of_expenses += expense["amount"]
        
        print(f"The sum of expenses for the given filter: {filter} is {sum_of_expenses}$")

    def export_expenses(self, type: str):
        if type == "csv":
            with open(DB_FILE_PATH) as json_file:
                json_data = json.load(json_file)
            data_file = open(CSV_FILE_PATH, 'w', newline='')
            csv_writer = csv.writer(data_file)
            count = 0
            for data in json_data:
                if count == 0:
                    header = data.keys()
                    csv_writer.writerow(header)
                    count += 1
                csv_writer.writerow(data.values())

            data_file.close()
            print(f"The expense database has been exported to a CSV to {CSV_FILE_PATH}")
        else:
            print("Invalid file type. Only CSV is supported for now.")

    def list_expenses(self, filter=None):
        expenses = self._database.get("expenses", [])
        if not expenses:
            print("No expenses available.")
            return

        if filter is None: 
            filtered_expenses = expenses 
        else: 
            filtered_expenses = [expense for expense in expenses if expense.get(filter)]
        
        if not filtered_expenses:
            print(f"The expenses cannot be filtered by {filter}" if filter else "No expenses available.")
            return

        self.tablify(filtered_expenses)
    
    def tablify(self, data):
        table = PrettyTable()
        table.field_names = ["id", "description", "amount", "category", "createdAt"]

        if len(data) > 1:
            for expense in data:
                table.add_row([int(expense["id"]), str(expense["description"]), int(expense["amount"]), str(expense["category"]),  str(expense["createdAt"])])
        else:
            table.add_row([int(expense["id"]), str(expense["description"]), int(expense["amount"]), str(expense["category"]),  str(expense["createdAt"])])

        print(table)