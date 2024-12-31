import pytest
from datetime import datetime, timedelta
from freezegun import freeze_time
from src.expense.expense_core import Expense

class TestExpense:
    # Default test data that will be used across multiple tests
    @pytest.fixture
    def valid_expense_data(self):
        return {
            "id": 1,
            "description": "Test Expense",
            "amount": 100.0,
            "category": "Food",
            "created_at": "2024-01-01T10:00:00"
        }
    
    @pytest.fixture
    def expense(self, valid_expense_data):
        return Expense(**valid_expense_data)

    def test_expense_initialization(self, valid_expense_data, expense):
        """Test that an expense is properly initialized with all fields"""
        assert expense.id == valid_expense_data["id"]
        assert expense.description == valid_expense_data["description"]
        assert expense.amount == valid_expense_data["amount"]
        assert expense.category == valid_expense_data["category"]
        assert expense.created_at == valid_expense_data["created_at"]
        assert expense.month == 1  # January

    def test_negative_amount_raises_error(self, valid_expense_data):
        """Test that initializing with negative amount raises ValueError"""
        valid_expense_data["amount"] = -100.0
        with pytest.raises(ValueError, match="Amount must be non-negative"):
            Expense(**valid_expense_data)

    @freeze_time("2024-03-15T14:30:00")
    def test_default_created_at(self):
        """Test that created_at defaults to current time when not provided"""
        expense = Expense(
            id=1,
            description="Test",
            amount=100.0,
            category="Food"
        )
        expected_datetime = datetime(2024, 3, 15, 14, 30, 0)
        assert expense.created_at == expected_datetime.isoformat()
        assert expense.month == 3  # March

    def test_as_dict_method(self, expense, valid_expense_data):
        """Test that as_dict returns correct dictionary representation"""
        expense_dict = expense.as_dict()
        assert expense_dict["id"] == valid_expense_data["id"]
        assert expense_dict["description"] == valid_expense_data["description"]
        assert expense_dict["amount"] == valid_expense_data["amount"]
        assert expense_dict["category"] == valid_expense_data["category"]
        assert expense_dict["created_at"] == valid_expense_data["created_at"]
        assert expense_dict["month"] == 1

    def test_str_representation(self, expense):
        """Test that __str__ returns correct string representation"""
        expected_str = (
            "Expense(id=1, description=Test Expense, amount=100.0, "
            "category=Food, created_at=2024-01-01T10:00:00, month=1)"
        )
        assert str(expense) == expected_str

    def test_repr_representation(self, expense):
        """Test that __repr__ returns same as __str__"""
        assert repr(expense) == str(expense)

    def test_month_calculation_across_different_months(self):
        """Test month calculation for different dates throughout the year"""
        test_dates = [
            ("2024-01-15T10:00:00", 1),
            ("2024-06-30T23:59:59", 6),
            ("2024-12-01T00:00:00", 12)
        ]
        
        for date_str, expected_month in test_dates:
            expense = Expense(
                id=1,
                description="Test",
                amount=100.0,
                category="Food",
                created_at=date_str
            )
            assert expense.month == expected_month

    def test_zero_amount_is_valid(self):
        """Test that zero amount is accepted"""
        expense = Expense(
            id=1,
            description="Zero cost item",
            amount=0.0,
            category="Free"
        )
        assert expense.amount == 0.0