# expense-tracker
A simple expense tracker application to manage your finances.

# Requirements
Build a simple expense tracker application to manage your finances. The application should allow users to add, delete, and view their expenses. The application should also provide a summary of the expenses.

Application should run from the command line and should have the following features:

Users can add an expense with a description and amount.
Users can update an expense.
Users can delete an expense.
Users can view all expenses.
Users can view a summary of all expenses.
Users can view a summary of expenses for a specific month (of current year).
Here are some additional features that you can add to the application:

Add expense categories and allow users to filter expenses by category.
Allow users to set a budget for each month and show a warning when the user exceeds the budget.
Allow users to export expenses to a CSV file.
The list of commands and their expected output is shown below:

```python
$ expense-tracker --add Lunch 20 Food

$ expense-tracker --add "Dinner" 10 Food

$ expense-tracker --list-all
```

Implementation
You can implement the application using any programming language of your choice. Here are some suggestions:

Use any programming language for any available module for parsing command arguments (e.g. python with the argparse, node.js with commander etc).
Use a simple text file to store the expenses data. You can use JSON, CSV, or any other format to store the data.
Add error handling to handle invalid inputs and edge cases (e.g. negative amounts, non-existent expense IDs, etc).
Use functions to modularize the code and make it easier to test and maintain.
This project idea is a great way to practice your logic building skills and learn how to interact with the filesystem using a CLI application. It will also help you understand how to manage data and provide useful information to users in a structured way.