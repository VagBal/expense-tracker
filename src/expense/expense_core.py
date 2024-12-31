from dataclasses import dataclass, field
from typing import Dict
from datetime import datetime

@dataclass
class Expense:
    id: int
    description: str
    amount: float
    category: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    month: int = field(init=False)

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Amount must be non-negative")
        self.month = datetime.fromisoformat(self.created_at).month

    def as_dict(self) -> Dict[str, any]:
        return {
            "id": self.id,
            "description": self.description,
            "amount": self.amount,
            "category": self.category,
            "created_at": self.created_at,
            "month": self.month
        }

    def __str__(self) -> str:
        return f"Expense(id={self.id}, description={self.description}, amount={self.amount}, " \
               f"category={self.category}, created_at={self.created_at}, month={self.month})"

    def __repr__(self) -> str:
        return self.__str__()
