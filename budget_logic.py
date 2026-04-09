def calculate_budget(income):
    """
    Apply 50-30-20 budgeting rule.
    """

    needs = income * 0.5
    wants = income * 0.3
    savings = income * 0.2

    return {
        "Needs": round(needs, 2),
        "Wants": round(wants, 2),
        "Savings": round(savings, 2)
    }


def analyze_expenses(expenses):
    """
    Analyze total expenses.
    """

    total = sum([exp[1] for exp in expenses])

    if total == 0:
        return "No expenses recorded yet."

    if total > 20000:
        return "Your spending is high. Try reducing non-essential expenses."

    elif total > 10000:
        return "Your spending is moderate. Keep tracking regularly."

    else:
        return "Good job managing expenses!"


def suggest_savings(income, total_expense):
    """
    Suggest saving strategy.
    """

    remaining = income - total_expense

    if remaining <= 0:
        return "You are overspending. Reduce unnecessary purchases."

    if remaining < income * 0.2:
        return "Try increasing savings to at least 20% of income."

    return "Your savings look good. Keep it up!"