import pandas as pd
import matplotlib.pyplot as plt


def create_pie_chart(expenses):
    """
    Create pie chart based on category spending.
    """

    if not expenses:
        return None

    df = pd.DataFrame(
        expenses,
        columns=[
            "id",
            "amount",
            "category",
            "description",
            "date"
        ]
    )

    # Group by category
    category_totals = df.groupby("category")["amount"].sum()

    fig, ax = plt.subplots()

    ax.pie(
        category_totals,
        labels=category_totals.index,
        autopct="%1.1f%%"
    )

    ax.set_title("Expense Distribution by Category")

    return fig


def create_bar_chart(expenses):
    """
    Create monthly expense bar chart.
    """

    if not expenses:
        return None

    df = pd.DataFrame(
        expenses,
        columns=[
            "id",
            "amount",
            "category",
            "description",
            "date"
        ]
    )

    # Convert date column
    df["date"] = pd.to_datetime(df["date"])

    # Extract month
    df["month"] = df["date"].dt.strftime("%Y-%m")

    monthly_totals = df.groupby("month")["amount"].sum()

    fig, ax = plt.subplots()

    monthly_totals.plot(
        kind="bar",
        ax=ax
    )

    ax.set_title("Monthly Expenses")

    return fig