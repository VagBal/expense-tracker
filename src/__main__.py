from enum import Enum
from src.database.database_core import Database
from src.parser.parser_core import Parser

class ListMode(Enum):
    CATEGORY = "category"
    MONTH = "month"

class SummaryMode(Enum):
    ALL = "all"
    CATEGORY = "category"
    MONTH = "month"

def main():
    try:
        db = Database()
        parser = Parser()
        args = parser.parse_args()

        if args.add:
            description, amount, category = args.add
            try:
                amount = float(amount)
            except ValueError:
                raise ValueError(f"Invalid amount: {amount}. Must be a number.")
            db.add_an_expense(str(description), amount, str(category))
            
        elif args.delete:
            db.delete_an_expense(args.delete)  # Type conversion handled by argparse
            
        elif args.update_description:
            expense_id, new_description = args.update_description
            db.update_an_expense_description(expense_id, str(new_description))
            
        elif args.update_amount:
            expense_id, new_amount = args.update_amount
            db.update_an_expense_amount(expense_id, new_amount)  # Type conversion handled by argparse
            
        elif args.update_category:
            expense_id, new_category = args.update_category
            db.update_an_expense_category(expense_id, str(new_category))
            
        elif args.find:
            db.find_expense_by_id(args.find)  # Type conversion handled by argparse
            
        elif args.list_all:
            db.list_expenses()
            
        elif args.list_by_category:
            category = args.list_by_category
            db.list_expenses(category)
            
        elif args.list_by_month:
            month = args.list_by_month
            db.list_expenses(month)
            
        elif args.summary_all:
            db.summary_expenses()
            
        elif args.summary_by_category:
            category = args.summary_by_category
            db.summary_expenses(category, "category")
            
        elif args.summary_by_month:
            month = args.summary_by_month
            db.summary_expenses(month)
            
        elif args.export_csv:
            db.export_expenses("csv")
            
        else:
            parser.parser.print_help()
            
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise

if __name__ == "__main__":
    main()