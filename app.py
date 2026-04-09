import streamlit as st
from database import create_table, add_expense, fetch_expenses
from budget_logic import calculate_budget, analyze_expenses, convert_currency
from gemini_chat import get_ai_response
from charts import create_pie_chart, create_bar_chart
from prompts import SYSTEM_PROMPT, EXAMPLE_PROMPTS

# Create DB table
create_table()

st.set_page_config(page_title="AI Budgeting Assistant", layout="wide")

st.title("💰 AI Budgeting Assistant (Gemini Powered)")

# Sidebar Menu
menu = [
    "🤖 Chatbot",
    "➕ Add Expense",
    "📋 View Expenses",
    "📊 Charts",
    "🧮 Budget Planner",
    "🌍 Currency Converter"
]

choice = st.sidebar.selectbox("Menu", menu)

# ---------------- CHATBOT ---------------- #

if choice == "🤖 Chatbot":

    st.subheader("Finance Chatbot")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.text_input(
        "Ask your budgeting question:"
    )

    if user_input:

        full_input = (
            SYSTEM_PROMPT
            + EXAMPLE_PROMPTS
            + "\nUser: "
            + user_input
        )

        response = get_ai_response(
            full_input,
            st.session_state.chat_history
        )

        st.session_state.chat_history.append(
            ("User", user_input)
        )

        st.session_state.chat_history.append(
            ("Assistant", response)
        )

    for role, msg in st.session_state.chat_history:
        st.write(f"**{role}:** {msg}")

# ---------------- ADD EXPENSE ---------------- #

elif choice == "➕ Add Expense":

    st.subheader("Add Expense")

    amount = st.number_input(
        "Amount (₹)",
        min_value=0.0
    )

    category = st.selectbox(
        "Category",
        ["Food", "Rent", "Travel", "Shopping", "Bills", "Other"]
    )

    description = st.text_input(
        "Description"
    )

    date = st.date_input("Date")

    if st.button("Add Expense"):

        add_expense(
            amount,
            category,
            description,
            str(date)
        )

        st.success("Expense Added Successfully!")

# ---------------- VIEW EXPENSES ---------------- #

elif choice == "📋 View Expenses":

    st.subheader("Expense List")

    expenses = fetch_expenses()

    if expenses:

        st.dataframe(
            expenses,
            use_container_width=True
        )

        analysis = analyze_expenses(expenses)

        st.info(analysis)

    else:
        st.warning("No expenses found.")

# ---------------- CHARTS ---------------- #

elif choice == "📊 Charts":

    st.subheader("Expense Visualization")

    expenses = fetch_expenses()

    if expenses:

        pie_chart = create_pie_chart(expenses)
        bar_chart = create_bar_chart(expenses)

        if pie_chart:
            st.pyplot(pie_chart)

        if bar_chart:
            st.pyplot(bar_chart)

    else:
        st.warning("No data to visualize.")

# ---------------- BUDGET PLANNER ---------------- #

elif choice == "🧮 Budget Planner":

    st.subheader("Budget Planner (50-30-20 Rule)")

    income = st.number_input(
        "Enter Monthly Income (₹)",
        min_value=0.0
    )

    if income:

        budget = calculate_budget(income)

        st.success("Recommended Budget:")

        st.write(f"Needs: ₹{budget['Needs']}")
        st.write(f"Wants: ₹{budget['Wants']}")
        st.write(f"Savings: ₹{budget['Savings']}")

# ---------------- CURRENCY CONVERTER ---------------- #

elif choice == "🌍 Currency Converter":

    st.subheader("Currency Converter")

    amount = st.number_input(
        "Amount",
        min_value=0.0
    )

    from_currency = st.selectbox(
        "From Currency",
        ["INR", "USD", "EUR", "GBP"]
    )

    to_currency = st.selectbox(
        "To Currency",
        ["USD", "INR", "EUR", "GBP"]
    )

    if st.button("Convert"):

        converted = convert_currency(
            amount,
            from_currency,
            to_currency
        )

        st.success(
            f"Converted Amount: {converted} {to_currency}"
        )