import pandas as pd
import altair as alt

def create_pie_chart(expenses):
    """
    Generates an interactive pie chart (donut style) showing the distribution 
    of expenses across different categories using Altair.
    
    Args:
        expenses (list): A list of tuples containing expense data.
        
    Returns:
        altair.Chart: An Altair donut chart object.
    """
    if not expenses:
        return None

    # Load data into DataFrame
    df = pd.DataFrame(
        expenses,
        columns=["id", "amount", "category", "description", "date"]
    )

    # Group by category and sum the amounts
    category_totals = df.groupby("category", as_index=False)["amount"].sum()

    # Create the Altair donut chart
    chart = alt.Chart(category_totals).mark_arc(innerRadius=50).encode(
        theta=alt.Theta(field="amount", type="quantitative"),
        color=alt.Color(field="category", type="nominal", scale=alt.Scale(scheme='category20b')),
        tooltip=[alt.Tooltip(field="category", type="nominal"), alt.Tooltip(field="amount", type="quantitative", format=",.2f")]
    ).properties(
        title="Expense Distribution by Category",
        width=400,
        height=400
    ).interactive()

    return chart

def create_bar_chart(expenses):
    """
    Generates an interactive bar chart showing monthly expense totals using Altair.
    
    Args:
        expenses (list): A list of tuples containing expense data.
        
    Returns:
        altair.Chart: An Altair bar chart object.
    """
    if not expenses:
        return None

    # Load data into DataFrame
    df = pd.DataFrame(
        expenses,
        columns=["id", "amount", "category", "description", "date"]
    )

    # Convert date strings to datetime objects for time-based operations
    df["date"] = pd.to_datetime(df["date"])

    # Format the date to Year-Month (e.g., 2024-01)
    df["Month"] = df["date"].dt.strftime("%b %Y")

    # Group by month and sum the amounts
    monthly_totals = df.groupby("Month", as_index=False)["amount"].sum()

    # Create the Altair bar chart
    chart = alt.Chart(monthly_totals).mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3).encode(
        x=alt.X(field="Month", type="nominal", sort=None, title="Month"),
        y=alt.Y(field="amount", type="quantitative", title="Total Spent (₹)"),
        color=alt.value("#636EFA"),
        tooltip=[alt.Tooltip(field="Month", type="nominal"), alt.Tooltip(field="amount", type="quantitative", format=",.2f")]
    ).properties(
        title="Monthly Expense Trends",
        width=600,
        height=400
    ).interactive()

    return chart