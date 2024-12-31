import argparse

class Parser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Command line Expense Tracker App")
        
        # Create a main parser group
        action_group = self.parser.add_argument_group("Action arguments")
        list_group = self.parser.add_argument_group("List arguments")
        summary_group = self.parser.add_argument_group("Summary arguments")
        
        # Action arguments
        action_group.add_argument(
            "--add",
            nargs=3,
            metavar=("DESCRIPTION", "AMOUNT", "CATEGORY"),
            help="Add a new expense record"
        )
        action_group.add_argument(
            "--delete",
            type=int,
            metavar="ID",
            help="Delete an expense record by id"
        )
        action_group.add_argument(
            "--update-description",
            nargs=2,
            metavar=("ID", "NEW_DESCRIPTION"),
            help="Update an expense record's description"
        )
        action_group.add_argument(
            "--update-amount",
            nargs=2,
            metavar=("ID", "NEW_AMOUNT"),
            type=float,
            help="Update an expense record's amount"
        )
        action_group.add_argument(
            "--update-category",
            nargs=2,
            metavar=("ID", "NEW_CATEGORY"),
            help="Update an expense record's category"
        )
        action_group.add_argument(
            "--find",
            type=int,
            metavar="ID",
            help="Find an expense record by id"
        )
        
        # List arguments
        list_group.add_argument(
            "--list-all",
            action="store_true",
            help="List all expenses"
        )
        list_group.add_argument(
            "--list-by-category",
            metavar="CATEGORY",
            help="List all expenses by category"
        )
        list_group.add_argument(
            "--list-by-month",
            metavar="MONTH",
            help="List all expenses by month of the current year"
        )
        
        # Summary arguments
        summary_group.add_argument(
            "--summary-all",
            action="store_true",
            help="Summary of all expenses"
        )
        summary_group.add_argument(
            "--summary-by-category",
            metavar="CATEGORY",
            help="Summary of expenses by category"
        )
        summary_group.add_argument(
            "--summary-by-month",
            metavar="MONTH",
            help="Summary of expenses by month of the current year"
        )
        
        # Export argument
        self.parser.add_argument(
            "--export-csv",
            action="store_true",
            help="Export the expenses to a CSV file"
        )
    
    def parse_args(self):
        try:
            args = self.parser.parse_args()
            if args.add:
                # Convert amount to float
                args.add[1] = float(args.add[1])
            return args
        except ValueError as e:
            self.parser.error(f"Invalid argument value: {e}")
        except SystemExit as e:
            raise  # Re-raise SystemExit to maintain original behavior
        except Exception as e:
            self.parser.error(f"Error parsing arguments: {e}")
