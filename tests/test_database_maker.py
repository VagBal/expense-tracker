import pytest
import json
from unittest.mock import mock_open, patch, MagicMock
from pathlib import Path
from src.database.database_maker import DatabaseMaker, DATABASE_STRUCTURE, DB_FILE_PATH

class TestDatabaseMaker:
    @pytest.fixture
    def sample_db_content(self):
        """Provides sample content for the new database"""
        return {
            "name": "Expense Tracker Database",
            "monthly_budgets": [],
            "expenses": []
        }

    @pytest.fixture
    def database_maker(self):
        """
        Creates a fresh DatabaseMaker instance for each test.
        This fixture helps maintain test isolation.
        """
        return DatabaseMaker()

    @pytest.fixture
    def mock_db_path(self):
        """
        Creates a mock Path object for testing file operations.
        This helps us avoid actual filesystem operations during testing.
        """
        with patch('pathlib.Path') as mock_path:
            # Configure the mock path to match our expected DB_FILE_PATH
            mock_path.return_value = MagicMock(spec=Path)
            mock_path.return_value.resolve.return_value = DB_FILE_PATH
            yield mock_path

    def test_initialization(self, database_maker):
        """
        Tests that DatabaseMaker initializes with correct attributes.
        Verifies both the file path and database structure are properly set.
        """
        assert database_maker.db_file_path == DB_FILE_PATH
        assert database_maker.database_dict == DATABASE_STRUCTURE
        
        # Verify the structure of DATABASE_STRUCTURE
        assert "name" in database_maker.database_dict
        assert "monthly_budgets" in database_maker.database_dict
        assert "expenses" in database_maker.database_dict
        assert len(database_maker.database_dict["monthly_budgets"]) == 12

    def test_make_a_new_db_handles_error(self, database_maker, capfd):
        """
        Tests error handling when creating a new database fails.
        Verifies that the error message is properly printed.
        """
        with patch('builtins.open', side_effect=Exception("Test error")):
            database_maker.make_a_new_db()
        
        # Capture and verify the error message
        captured = capfd.readouterr()
        assert "An error occurred while creating the database: Test error" in captured.out

    def test_update_an_existing_db_handles_error(self, database_maker, capfd):
        """
        Tests error handling when updating an existing database fails.
        Verifies that the error message is properly printed.
        """
        new_dict = {"test": "data"}
        with patch('builtins.open', side_effect=Exception("Test error")):
            database_maker.update_an_existing_db(new_dict)
        
        # Capture and verify the error message
        captured = capfd.readouterr()
        assert "An error occurred while updating the database: Test error" in captured.out

    def test_is_db_file_exists_true(self, database_maker):
        """
        Tests the is_db_file_exists method when the file exists.
        Uses a mock to simulate the presence of the database file.
        """
        with patch.object(Path, 'is_file', return_value=True):
            assert database_maker.is_db_file_exists() is True

    def test_is_db_file_exists_false(self, database_maker):
        """
        Tests the is_db_file_exists method when the file doesn't exist.
        Uses a mock to simulate the absence of the database file.
        """
        with patch.object(Path, 'is_file', return_value=False):
            assert database_maker.is_db_file_exists() is False

    def test_database_structure_content(self):
        """
        Tests the content and structure of the DATABASE_STRUCTURE constant.
        Verifies all required fields and their formats.
        """
        # Verify basic structure
        assert isinstance(DATABASE_STRUCTURE, dict)
        assert all(key in DATABASE_STRUCTURE for key in ['name', 'monthly_budgets', 'expenses'])
        
        # Verify monthly budgets
        budgets = DATABASE_STRUCTURE['monthly_budgets']
        assert len(budgets) == 12
        
        # Verify each month's structure
        months = ['January', 'February', 'March', 'April', 'May', 'June',
                 'July', 'August', 'September', 'October', 'November', 'December']
        for i, budget in enumerate(budgets, 1):
            assert budget['id'] == i
            assert budget['name'] == months[i-1]
            assert budget['budget'] == 100

        # Verify expenses list exists and is empty
        assert isinstance(DATABASE_STRUCTURE['expenses'], list)
        assert len(DATABASE_STRUCTURE['expenses']) == 0