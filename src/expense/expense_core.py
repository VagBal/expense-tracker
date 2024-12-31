from dataclasses import dataclass

@dataclass
class Expense:
    _id: int
    _description: str
    _amount: float
    _category: str
    _created_at: str
    _month: int
    
    def as_dict(self) -> dict:
        return {
            "id": self._id,
            "description": self._description,
            "amount": self._amount,
            "category": self._category,
            "created_at": self._created_at,
            "month": self._month
        }