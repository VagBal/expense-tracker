import pytest
from unittest.mock import Mock, patch, call
from src.__main__ import main, ListMode, SummaryMode
from src.database.database_core import Database
from src.parser.parser_core import Parser

class TestmainModule:
    @pytest.fixture
    def mock_database(self):
        """
        Creates a mock Database instance with all necessary methods.
        This fixture helps isolate our tests from the actual database operations.
        """
        mock_db = Mock(spec=Database)
        return mock_db

    @pytest.fixture
    def mock_parser(self):
        """
        Creates a mock Parser instance that returns predefined arguments.
        This allows us to simulate different command-line inputs.
        """
        mock_parser = Mock(spec=Parser)
        # Create a mock for the internal ArgumentParser as well
        mock_parser.parser = Mock()
        return mock_parser

    def test_add_expense_successful(self, mock_database, mock_parser):
        """
        Tests the successful addition of an expense through the __main__ function.
        Verifies that the database add_an_expense method is called with correct parameters.
        """
        # Setup mock parser to return add argument
        args = Mock()
        args.add = ["Lunch", "15.50", "Food"]
        args.delete = args.update_description = args.update_amount = None
        args.update_category = args.find = args.list_all = None
        args.list_by_category = args.list_by_month = args.summary_all = None
        args.summary_by_category = args.summary_by_month = args.export_csv = None
        mock_parser.parse_args.return_value = args

        with patch('src.__main__.Database', return_value=mock_database), \
             patch('src.__main__.Parser', return_value=mock_parser):
            main()

        # Verify the database method was called with correct parameters
        mock_database.add_an_expense.assert_called_once_with("Lunch", 15.50, "Food")

    def test_add_expense_invalid_amount(self, mock_database, mock_parser):
        """
        Tests handling of invalid amount when adding an expense.
        Verifies that appropriate error handling occurs.
        """
        args = Mock()
        args.add = ["Lunch", "invalid", "Food"]
        args.delete = args.update_description = args.update_amount = None
        args.update_category = args.find = args.list_all = None
        args.list_by_category = args.list_by_month = args.summary_all = None
        args.summary_by_category = args.summary_by_month = args.export_csv = None
        mock_parser.parse_args.return_value = args

        with patch('src.__main__.Database', return_value=mock_database), \
             patch('src.__main__.Parser', return_value=mock_parser), \
             patch('builtins.print') as mock_print:
            main()

        mock_print.assert_called_with("Error: Invalid amount: invalid. Must be a number.")
        mock_database.add_an_expense.assert_not_called()

    def test_delete_expense(self, mock_database, mock_parser):
        """
        Tests the deletion of an expense through the main function.
        Verifies that the database delete_an_expense method is called correctly.
        """
        args = Mock()
        args.add = None
        args.delete = 1
        args.update_description = args.update_amount = None
        args.update_category = args.find = args.list_all = None
        args.list_by_category = args.list_by_month = args.summary_all = None
        args.summary_by_category = args.summary_by_month = args.export_csv = None
        mock_parser.parse_args.return_value = args

        with patch('src.__main__.Database', return_value=mock_database), \
             patch('src.__main__.Parser', return_value=mock_parser):
            main()

        mock_database.delete_an_expense.assert_called_once_with(1)

    def test_update_description(self, mock_database, mock_parser):
        """
        Tests updating an expense description through the main function.
        Verifies proper handling of ID conversion and database method call.
        """
        args = Mock()
        args.add = args.delete = None
        args.update_description = ["1", "New lunch description"]
        args.update_amount = args.update_category = args.find = None
        args.list_all = args.list_by_category = args.list_by_month = None
        args.summary_all = args.summary_by_category = args.summary_by_month = None
        args.export_csv = None
        mock_parser.parse_args.return_value = args

        with patch('src.__main__.Database', return_value=mock_database), \
             patch('src.__main__.Parser', return_value=mock_parser):
            main()

        mock_database.update_an_expense_description.assert_called_once_with(1, "New lunch description")

    def test_update_amount(self, mock_database, mock_parser):
        """
        Tests updating an expense amount through the main function.
        Verifies proper conversion of string amount to float.
        """
        args = Mock()
        args.add = args.delete = args.update_description = None
        args.update_amount = ["1", "25.50"]
        args.update_category = args.find = args.list_all = None
        args.list_by_category = args.list_by_month = args.summary_all = None
        args.summary_by_category = args.summary_by_month = args.export_csv = None
        mock_parser.parse_args.return_value = args

        with patch('src.__main__.Database', return_value=mock_database), \
             patch('src.__main__.Parser', return_value=mock_parser):
            main()

        mock_database.update_an_expense_amount.assert_called_once_with(1, 25.50)

    def test_list_expenses(self, mock_database, mock_parser):
        """
        Tests various list expense operations through the main function.
        Covers list all, list by category, and list by month scenarios.
        """
        # Test list all
        args = Mock()
        args.add = args.delete = args.update_description = None
        args.update_amount = args.update_category = args.find = None
        args.list_all = True
        args.list_by_category = args.list_by_month = args.summary_all = None
        args.summary_by_category = args.summary_by_month = args.export_csv = None
        mock_parser.parse_args.return_value = args

        with patch('src.__main__.Database', return_value=mock_database), \
             patch('src.__main__.Parser', return_value=mock_parser):
            main()

        mock_database.list_expenses.assert_called_once_with()

        # Test list by category
        mock_database.reset_mock()
        args.list_all = False
        args.list_by_category = "Food"
        with patch('src.__main__.Database', return_value=mock_database), \
             patch('src.__main__.Parser', return_value=mock_parser):
            main()

        mock_database.list_expenses.assert_called_once_with("category", "Food")

    def test_summary_operations(self, mock_database, mock_parser):
        """
        Tests various summary operations through the main function.
        Covers summary all, summary by category, and summary by month scenarios.
        """
        # Test summary all
        args = Mock()
        args.add = args.delete = args.update_description = None
        args.update_amount = args.update_category = args.find = None
        args.list_all = args.list_by_category = args.list_by_month = None
        args.summary_all = True
        args.summary_by_category = args.summary_by_month = args.export_csv = None
        mock_parser.parse_args.return_value = args

        with patch('src.__main__.Database', return_value=mock_database), \
             patch('src.__main__.Parser', return_value=mock_parser):
            main()

        mock_database.summary_expenses.assert_called_once_with()

        # Test summary by category
        mock_database.reset_mock()
        args.summary_all = False
        args.summary_by_category = "Food"
        with patch('src.__main__.Database', return_value=mock_database), \
             patch('src.__main__.Parser', return_value=mock_parser):
            main()

        mock_database.summary_expenses.assert_called_once_with("Food", "category")

    def test_export_csv(self, mock_database, mock_parser):
        """
        Tests the CSV export functionality through the main function.
        Verifies that the export_expenses method is called with correct parameters.
        """
        args = Mock()
        args.add = args.delete = args.update_description = None
        args.update_amount = args.update_category = args.find = None
        args.list_all = args.list_by_category = args.list_by_month = None
        args.summary_all = args.summary_by_category = args.summary_by_month = None
        args.export_csv = True
        mock_parser.parse_args.return_value = args

        with patch('src.__main__.Database', return_value=mock_database), \
             patch('src.__main__.Parser', return_value=mock_parser):
            main()

        mock_database.export_expenses.assert_called_once_with("csv")

    def test_no_arguments_prints_help(self, mock_database, mock_parser):
        """
        Tests that the help message is printed when no arguments are provided.
        Verifies proper handling of the default case.
        """
        args = Mock()
        args.add = args.delete = args.update_description = None
        args.update_amount = args.update_category = args.find = None
        args.list_all = args.list_by_category = args.list_by_month = None
        args.summary_all = args.summary_by_category = args.summary_by_month = None
        args.export_csv = None
        mock_parser.parse_args.return_value = args

        with patch('src.__main__.Database', return_value=mock_database), \
             patch('src.__main__.Parser', return_value=mock_parser):
            main()

        mock_parser.parser.print_help.assert_called_once()

    def test_unexpected_error_handling(self, mock_database, mock_parser):
        """
        Tests handling of unexpected errors in the main function.
        Verifies that errors are properly caught and reported.
        """
        args = Mock()
        args.add = ["Lunch", "15.50", "Food"]
        mock_parser.parse_args.return_value = args
        mock_database.add_an_expense.side_effect = Exception("Unexpected error")

        with patch('src.__main__.Database', return_value=mock_database), \
             patch('src.__main__.Parser', return_value=mock_parser), \
             patch('builtins.print') as mock_print, \
             pytest.raises(Exception):
            main()

        mock_print.assert_called_with("An unexpected error occurred: Unexpected error")