# models.py

# Makes a single expense entry with all the necessary things based on the inputs of the user in the interface

class Expense:
       
    def __init__(self, expense_id, date, amount, category, description):
        self.id = expense_id
        self.date = date
        self.amount = amount
        self.category = category
        self.description = description

    def to_dict(self):
           #Convert the expense to dictionary for CSV storage
        return {
            'id': self.id,
            'date': self.date,
            'amount': self.amount,
            'category': self.category,
            'description': self.description
        }

    @classmethod
    def fr_dict(cls, data):
           #Create the Expense object from dictionary
        return cls(
            expense_id=int(data['id']),
            date=data['date'],
            amount=float(data['amount']),
            category=data['category'],
            description=data['description']
        )

    def __repr__(self):
        return f"Expense(ID: {self.id}, Date: {self.date}, Category: {self.category}, Amount: ${self.amount:.2f}, Desc: {self.description})"