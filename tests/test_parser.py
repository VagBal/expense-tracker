import pytest
from unittest.mock import Mock, patch
import argparse
from src.parser.parser_core import Parser

class TestParser:
    @pytest.fixture
    def parser(self):
        """
        Creates a fresh Parser instance for each test.
        This ensures test isolation and prevents state bleeding between tests.
        """
        return Parser()

    def test_parser_initialization(self, parser):
        """
        Tests that the Parser class initializes correctly with all required argument groups
        and arguments. This verifies the basic structure of our command-line interface.
        """
        # Verify the main parser was created
        assert isinstance(parser.parser, argparse.ArgumentParser)
        
        # Get all argument groups and their arguments
        groups = {group.title: group for group in parser.parser._action_groups}
        
        # Verify required argument groups exist
        assert "Action arguments" in groups
        assert "List arguments" in groups
        assert "Summary arguments" in groups
        
        # Verify action arguments
        action_args = {action.dest: action for action in groups["Action arguments"]._group_actions}
        assert "add" in action_args
        assert "delete" in action_args
        assert "update_description" in action_args
        assert "update_amount" in action_args
        assert "update_category" in action_args
        assert "find" in action_args
        
        # Verify list arguments
        list_args = {action.dest: action for action in groups["List arguments"]._group_actions}
        assert "list_all" in list_args
        assert "list_by_category" in list_args
        assert "list_by_month" in list_args
        
        # Verify summary arguments
        summary_args = {action.dest: action for action in groups["Summary arguments"]._group_actions}
        assert "summary_all" in summary_args
        assert "summary_by_category" in summary_args
        assert "summary_by_month" in summary_args

    def test_parse_add_argument_valid(self, parser):
        """
        Tests parsing valid add expense arguments.
        Verifies that the amount is correctly converted to float.
        """
        test_args = ["--add", "Lunch", "15.50", "Food"]
        
        with patch('sys.argv', ['script.py'] + test_args):
            args = parser.parse_args()
            
            assert args.add == ["Lunch", 15.50, "Food"]
            assert isinstance(args.add[1], float)

    def test_parse_add_argument_invalid_amount(self, parser):
        """
        Tests that invalid amount values are properly caught and raise an error.
        The parser should detect non-numeric values and handle them appropriately.
        """
        test_args = ["--add", "Lunch", "invalid", "Food"]
        
        with patch('sys.argv', ['script.py'] + test_args):
            with pytest.raises(SystemExit):
                # ArgumentParser calls sys.exit() on error
                parser.parse_args()

    def test_parse_delete_argument(self, parser):
        """
        Tests parsing delete argument with a valid ID.
        Verifies that the ID is correctly converted to integer.
        """
        test_args = ["--delete", "1"]
        
        with patch('sys.argv', ['script.py'] + test_args):
            args = parser.parse_args()
            assert args.delete == 1
            assert isinstance(args.delete, int)

    def test_parse_update_description(self, parser):
        """
        Tests parsing update description arguments.
        Verifies that both ID and new description are captured correctly.
        """
        test_args = ["--update-description", "1", "New lunch"]
        
        with patch('sys.argv', ['script.py'] + test_args):
            args = parser.parse_args()
            assert args.update_description == ["1", "New lunch"]

    def test_parse_update_amount(self, parser):
        """
        Tests parsing update amount arguments.
        Verifies that both ID and new amount are captured correctly.
        """
        test_args = ["--update-amount", "1", "20.50"]
        
        with patch('sys.argv', ['script.py'] + test_args):
            args = parser.parse_args()
            assert args.update_amount == ["1", "20.50"]

    def test_parse_update_category(self, parser):
        """
        Tests parsing update category arguments.
        Verifies that both ID and new category are captured correctly.
        """
        test_args = ["--update-category", "1", "Groceries"]
        
        with patch('sys.argv', ['script.py'] + test_args):
            args = parser.parse_args()
            assert args.update_category == ["1", "Groceries"]

    def test_parse_find_argument(self, parser):
        """
        Tests parsing find argument with a valid ID.
        Verifies that the ID is correctly converted to integer.
        """
        test_args = ["--find", "1"]
        
        with patch('sys.argv', ['script.py'] + test_args):
            args = parser.parse_args()
            assert args.find == 1
            assert isinstance(args.find, int)

    def test_parse_list_arguments(self, parser):
        """
        Tests parsing various list arguments.
        Verifies that list flags and values are captured correctly.
        """
        # Test --list-all
        with patch('sys.argv', ['script.py', '--list-all']):
            args = parser.parse_args()
            assert args.list_all is True

        # Test --list-by-category
        with patch('sys.argv', ['script.py', '--list-by-category', 'Food']):
            args = parser.parse_args()
            assert args.list_by_category == 'Food'

        # Test --list-by-month
        with patch('sys.argv', ['script.py', '--list-by-month', 'January']):
            args = parser.parse_args()
            assert args.list_by_month == 'January'

    def test_parse_summary_arguments(self, parser):
        """
        Tests parsing various summary arguments.
        Verifies that summary flags and values are captured correctly.
        """
        # Test --summary-all
        with patch('sys.argv', ['script.py', '--summary-all']):
            args = parser.parse_args()
            assert args.summary_all is True

        # Test --summary-by-category
        with patch('sys.argv', ['script.py', '--summary-by-category', 'Food']):
            args = parser.parse_args()
            assert args.summary_by_category == 'Food'

        # Test --summary-by-month
        with patch('sys.argv', ['script.py', '--summary-by-month', 'January']):
            args = parser.parse_args()
            assert args.summary_by_month == 'January'

    def test_parse_export_argument(self, parser):
        """
        Tests parsing the export CSV argument.
        Verifies that the export flag is captured correctly.
        """
        with patch('sys.argv', ['script.py', '--export-csv']):
            args = parser.parse_args()
            assert args.export_csv is True

    def test_parse_invalid_argument_combination(self, parser):
        """
        Tests parser behavior with invalid argument combinations.
        The parser should handle these gracefully.
        """
        # Test mutually exclusive arguments if any
        with patch('sys.argv', ['script.py', '--add', 'Lunch', '15.50', 'Food', '--delete', '1']):
            # This should still work as ArgumentParser allows multiple arguments by default
            args = parser.parse_args()
            assert args.add == ['Lunch', 15.50, 'Food']
            assert args.delete == 1

    def test_parse_general_error_handling(self, parser):
        """
        Tests general error handling in parse_args method.
        Verifies that various types of errors are caught and handled appropriately.
        """
        # Test with invalid argument type
        with patch('sys.argv', ['script.py', '--delete', 'not_a_number']):
            with pytest.raises(SystemExit):
                parser.parse_args()

        # Test with missing required argument values
        with patch('sys.argv', ['script.py', '--add', 'Lunch']):  # Missing amount and category
            with pytest.raises(SystemExit):
                parser.parse_args()