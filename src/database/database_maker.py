import json
import os
from pathlib import Path

BASE_PATH = Path(__file__).parent
DB_FILE_NAME = "db.json"
CSV_FILE_NAME = "expenses.csv"
DB_FILE_PATH = (BASE_PATH / f"../database/{DB_FILE_NAME}").resolve()
CSV_FILE_PATH = (BASE_PATH / f"../export/{DB_FILE_NAME}").resolve()

DATABASE_STRUCTURE = {
    "name": "Expense Tracker Database",
    "monthly_budgets": [
        {"id": 1, "name": "January", "budget": 100},
        {"id": 2, "name": "February", "budget": 100},
        {"id": 3, "name": "March", "budget": 100},
        {"id": 4, "name": "April", "budget": 100},
        {"id": 5, "name": "May", "budget": 100},
        {"id": 6, "name": "June", "budget": 100},
        {"id": 7, "name": "July", "budget": 100},
        {"id": 8, "name": "August", "budget": 100},
        {"id": 9, "name": "September", "budget": 100},
        {"id": 10, "name": "October", "budget": 100},
        {"id": 11, "name": "November", "budget": 100},
        {"id": 12, "name": "December", "budget": 100}
    ],
    "expenses": [
    ]
}

class DatabaseMaker:
    _database_dict = None
    _db_file_path = None

    def __init__(self):
        self._db_file_path = DB_FILE_PATH
        self._database_dict = DATABASE_STRUCTURE

    def make_a_new_db(self):
        with open(self._db_file_path, mode='w', encoding="utf-8") as db_file:
            json.dump(self._database_dict, db_file, indent=4)
    
    def update_an_existing_db(self, new_dict):
        with open(self._db_file_path, mode='w', encoding="utf-8") as db_file:
            json.dump(new_dict, db_file, indent=4)
    
    def is_db_file_exists(self):
        return os.path.isfile(DB_FILE_PATH)
    


