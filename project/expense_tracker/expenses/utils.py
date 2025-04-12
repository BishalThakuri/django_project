
def validate_expense(expense):
    if expense.amount <= 0:
        return "Amount must be greater than zero."
    if not expense.title:
        return "Title is required."
    if not expense.date:
        return "Date is required."
    return None
