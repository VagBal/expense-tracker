import pytest
import json
import csv
from unittest.mock import Mock, patch, mock_open, call, MagicMock
from datetime import datetime
from src.database.database_core import Database, States
from src.expense.expense_core import Expense
import threading
import time

class TestDatabase:
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """
        Setup and teardown for each test.
        Ensures Database singleton is reset between tests.
        """
        # Reset the singleton instance before each test
        Database.instance = None
        Database.state = None
        Database.database = None
        Database.id = 0
        Database.database_maker = None
        
        yield
        
        # Cleanup after each test
        Database.instance = None

    @pytest.fixture
    def mock_database_maker(self):
        """Creates a mock DatabaseMaker with necessary methods"""
        mock = Mock()
        mock.is_db_file_exists.return_value = True
        return mock

    @pytest.fixture
    def sample_database_content(self):
        """Provides sample database content for testing"""
        return {
            "name": "Expense Tracker Database",
            "monthly_budgets": [
                {"id": 1, "name": "January", "budget": 100},
                {"id": 2, "name": "February", "budget": 100}
            ],
            "expenses": [
                {
                    "id": 1,
                    "description": "Test Expense",
                    "amount": 50.0,
                    "category": "Food",
                    "created_at": "2024-01-01T10:00:00",
                    "month": 1
                }
            ]
        }

    def test_singleton_pattern(self):
        """Tests that Database implements singleton pattern correctly"""
        db1 = Database()
        db2 = Database()
        assert db1 is db2
        
        # Test thread safety of singleton
        def create_db():
            return Database()
            
        threads = [threading.Thread(target=create_db) for _ in range(10)]
        [t.start() for t in threads]
        [t.join() for t in threads]
        
        db3 = Database()
        assert db1 is db3

    @patch('src.database.database_core.DatabaseMaker')
    def test_init_database(self, mock_file, mock_database_maker):
        """Tests database initialization"""
        with patch('src.database.database_core.DatabaseMaker') as MockDatabaseMaker:
            MockDatabaseMaker.return_value = mock_database_maker
            mock_file.return_value.__enter__.return_value.read.return_value = '{}'
            
            db = Database()
            assert db.state == States.ACTIVE
            assert db.database_maker is not None
            assert db.id == db.get_last_id()


    def test_get_last_id_empty_database(self):
        """Tests getting last ID from empty database"""
        db = Database()
        db.database = {"expenses": []}
        assert db.get_last_id() == 0

    def test_get_last_id_with_expenses(self, sample_database_content):
        """Tests getting last ID with existing expenses"""
        db = Database()
        db.database = sample_database_content
        assert db.get_last_id() == 1

    def test_get_state(self):
        """Tests getting database state"""
        db = Database()
        assert db.get_state() == States.ACTIVE

    @patch('builtins.open', new_callable=mock_open)
    def test_load_db_from_file(self, mock_file, sample_database_content):
        """Tests loading database from file"""
        mock_file.return_value.__enter__.return_value.read.return_value = json.dumps(sample_database_content)
        
        db = Database()
        db.load_db_from_file("test_path")
        assert db.database == sample_database_content

    @patch('builtins.print')
    def test_load_db_from_file_error(self, mock_print):
        """Tests error handling when loading database"""
        db = Database()
        with patch('builtins.open', side_effect=Exception("Test error")):
            db.load_db_from_file("test_path")
            mock_print.assert_called_with("An error occurred while loading the database: Test error")

    @patch('datetime.datetime')
    def test_add_an_expense(self, mock_datetime, sample_database_content):
        """Tests adding a new expense"""
        mock_datetime.now.return_value.isoformat.return_value = "2024-01-01T10:00:00"
        mock_datetime.now.return_value.month = 1
        
        db = Database()
        db.database = sample_database_content
        db.database_maker = Mock()

        # Update monthly budget to allow adding the new expense
        db.database["monthly_budgets"][0]["budget"] = 200
        
        with patch('builtins.print') as mock_print:
            db.add_an_expense("Test", 75.0, "Food")
            assert len(db.database["expenses"]) == 2
            assert db.database["expenses"][-1]["description"] == "Test"

    def test_delete_an_expense(self, sample_database_content):
        """Tests deleting an expense"""
        db = Database()
        db.database = sample_database_content
        db.database_maker = Mock()
        
        initial_count = len(db.database["expenses"])
        db.delete_an_expense(1)
        assert len(db.database["expenses"]) == initial_count - 1

    def test_update_expense_amount(self, sample_database_content):
        """Tests updating expense amount"""
        db = Database()
        db.database = sample_database_content
        db.database_maker = Mock()
        
        db.update_an_expense_amount(1, 75.0)
        assert db.database["expenses"][0]["amount"] == 75.0

    def test_update_expense_description(self, sample_database_content):
        """Tests updating expense description"""
        db = Database()
        db.database = sample_database_content
        db.database_maker = Mock()
        
        db.update_an_expense_description(1, "Updated Test")
        assert db.database["expenses"][0]["description"] == "Updated Test"

    def test_update_expense_category(self, sample_database_content):
        """Tests updating expense category"""
        db = Database()
        db.database = sample_database_content
        db.database_maker = Mock()
        
        db.update_an_expense_category(1, "Updated Category")
        assert db.database["expenses"][0]["category"] == "Updated Category"

    def test_find_expense_by_id(self, sample_database_content):
        """Tests finding expense by ID"""
        db = Database()
        db.database = sample_database_content
        
        expense = db.find_expense_by_id(1)
        assert expense["id"] == 1
        assert expense["description"] == "Test Expense"

    def test_find_expense_by_id_not_found(self, sample_database_content):
        """Tests error handling when expense not found"""
        db = Database()
        db.database = sample_database_content
        
        with pytest.raises(ValueError, match="Expense with ID:999 not found"):
            db.find_expense_by_id(999)

    def test_set_budget_for_a_month(self, sample_database_content):
        """Tests setting budget for a specific month"""
        db = Database()
        db.database = sample_database_content
        db.database_maker = Mock()
        
        db.set_budget_for_a_month("January", 200)
        assert db.database["monthly_budgets"][0]["budget"] == 200

    @patch('builtins.print')
    def test_summary_expenses(self, mock_print, sample_database_content):
        """Tests expense summary functionality"""
        db = Database()
        db.database = sample_database_content
        
        db.summary_expenses(None)
        mock_print.assert_called_with("The sum of expenses for the given filter: all is 50.0$")

    @patch('builtins.open', new_callable=mock_open)
    def test_export_expenses_csv(self, mock_file, sample_database_content):
        """Tests exporting expenses to CSV"""
        mock_file.return_value.__enter__.return_value.read.return_value = json.dumps(sample_database_content)
        
        db = Database()
        db.load_db_from_file("test_path")
        db.database = sample_database_content  # Ensure the database is initialized with sample content
        
        with patch('json.load', return_value=sample_database_content):
            db.export_expenses("csv")
            mock_file.assert_called()

    from unittest.mock import patch, Mock

    def test_list_expenses_with_filter(self, sample_database_content):
        """Tests listing expenses with filters"""
        db = Database()
        db.database = sample_database_content
        
        with patch('src.database.database_core.PrettyTable') as MockPrettyTable:  # Ensure this path is correct
            mock_table = MockPrettyTable.return_value
            db.list_expenses(filter="category", filter_value="Food")
            assert mock_table.add_row.called

    def test_tablify(self, sample_database_content):
        """Tests table creation functionality"""
        db = Database()
        db.database = sample_database_content
        
        with patch('src.database.database_core.PrettyTable') as MockPrettyTable:  # Correct the path
            mock_table = MockPrettyTable.return_value
            db.tablify(sample_database_content["expenses"])
            assert mock_table.field_names == ["id", "description", "amount", "category", "created_at"]
            mock_table.add_row.assert_called()
