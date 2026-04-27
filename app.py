import streamlit as st
import pandas as pd
from database import create_table, add_expense, fetch_expenses, delete_expense, clear_all_expenses
from budget_logic import calculate_budget, analyze_expenses, convert_currency
from gemini_chat import get_ai_response
from charts import create_pie_chart, create_bar_chart
from prompts import SYSTEM_PROMPT, EXAMPLE_PROMPTS

# Initialize database on startup
create_table()

# Page configuration for a professional look
st.set_page_config(
    page_title="FinAI - Smart Budgeting",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Injection
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

try:
    local_css("assets/styles.css")
except FileNotFoundError:
    pass # Fallback to default if CSS is missing

# Sidebar Navigation with Icons
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/total-sales-1.png", width=100)
    st.title("FinAI Assistant")
    st.markdown("---")
    menu = {
        "🏠 Dashboard": "Home & Overview",
        "🤖 AI Chatbot": "Financial Advice",
        "➕ Add Expense": "Record Spending",
        "📋 View Expenses": "In-depth Analysis",
        "📊 Visual Insights": "Charts & Metrics",
        "🧮 Budget Rules": "50-30-20 Planner",
        "🌍 Currency Tool": "Global Exchange"
    }
    choice = st.radio("Navigate", list(menu.keys()))
    st.markdown("---")
    st.info("💡 Tip: Use the AI Chatbot to get personalized saving tips!")

# ---------------- DASHBOARD (HOME) ---------------- #

if choice == "🏠 Dashboard":
    st.title("🏠 Project Dashboard")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Welcome to FinAI Assistant! 🚀
        This project is a powerful, Gemini-powered financial tool designed to help you take control of your money. 
        Whether you're tracking daily coffee runs or planning for long-term savings, FinAI has you covered.

        #### ✨ Core Features:
        - **Intelligent Tracking**: Easily record and categorize every expense.
        - **AI Financial Coach**: Chat with our Gemini-powered bot for expert advice.
        - **Dynamic Insights**: Interactive charts showing exactly where your money goes.
        - **Smart Planning**: Auto-calculate budgets using the 50-30-20 rule.
        - **Global Ready**: Real-time currency conversion for international travelers.
        """)
        
    with col2:
        st.markdown("### 📈 Quick Stats")
        expenses = fetch_expenses()
        if expenses:
            total = sum(e[1] for e in expenses)
            count = len(expenses)
            st.metric("Total Expenses", f"₹{total:,.2f}")
            st.metric("Transactions", count)
            
            latest = expenses[-1]
            st.write(f"**Latest Item:** {latest[2]} ({latest[1]})")
        else:
            st.info("No data yet. Add an expense to see stats!")

    st.markdown("---")
    st.subheader("🛠️ Technology Stack")
    t1, t2, t3, t4 = st.columns(4)
    t1.code("Python / Streamlit")
    t2.code("Google Gemini AI")
    t3.code("SQLite3 Database")
    t4.code("Altair Visuals")

# ---------------- AI CHATBOT ---------------- #

elif choice == "🤖 AI Chatbot":
    st.title("🤖 AI Financial Coach")
    st.markdown("Ask anything about budgeting, saving, or investing.")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Chat interface container
    chat_container = st.container()
    
    with chat_container:
        for role, msg in st.session_state.chat_history:
            with st.chat_message("user" if role == "User" else "assistant"):
                st.write(msg)

    user_input = st.chat_input("How can I save ₹5000 this month?")

    if user_input:
        with st.chat_message("user"):
            st.write(user_input)
            
        with st.spinner("Analyzing financial strategies..."):
            # We now pass the SYSTEM_PROMPT separately as system_instruction
            # and only the user's specific query as user_input.
            # This prevents the model from being overwhelmed by long prompts in every turn.
            response = get_ai_response(
                user_input=user_input, 
                chat_history=st.session_state.chat_history,
                system_instruction=SYSTEM_PROMPT + "\n" + EXAMPLE_PROMPTS
            )
            
        with st.chat_message("assistant"):
            st.write(response)
            
        st.session_state.chat_history.append(("User", user_input))
        st.session_state.chat_history.append(("Assistant", response))

# ---------------- ADD EXPENSE ---------------- #

elif choice == "➕ Add Expense":
    st.title("➕ Record New Expense")
    
    col_add, col_recent = st.columns([1, 1])
    
    with col_add:
        st.subheader("New Entry")
        with st.form("expense_form", clear_on_submit=True):
            amount = st.number_input("Amount (₹)", min_value=0.0, step=10.0, format="%.2f")
            category = st.selectbox("Category", ["Food", "Rent", "Travel", "Shopping", "Bills", "Health", "Education", "Other"])
            date = st.date_input("Transaction Date")
            description = st.text_input("Short Description (e.g., Grocery at DMart)")
            
            submitted = st.form_submit_button("Add to Database")
            
            if submitted:
                if amount > 0:
                    add_expense(amount, category, description, str(date))
                    st.success(f"✅ Added ₹{amount} to {category}!")
                    st.rerun() # Refresh to show in recent
                else:
                    st.error("Please enter a valid amount.")

    with col_recent:
        st.subheader("Recent Entries (Quick Delete)")
        recent_expenses = fetch_expenses()
        if recent_expenses:
            # Show last 5 expenses
            for exp in reversed(recent_expenses[-5:]):
                with st.container():
                    c1, c2 = st.columns([3, 1])
                    c1.write(f"**₹{exp[1]}** | {exp[2]} | {exp[3][:20]}...")
                    if c2.button("🗑️", key=f"del_{exp[0]}"):
                        delete_expense(exp[0])
                        st.warning(f"Deleted entry!")
                        st.rerun()
        else:
            st.info("No recent entries to display.")

# ---------------- VIEW EXPENSES ---------------- #

elif choice == "📋 View Expenses":
    st.title("📋 Expense History")
    
    expenses = fetch_expenses()
    if expenses:
        df = pd.DataFrame(expenses, columns=["ID", "Amount (₹)", "Category", "Description", "Date"])
        
        # Metadata and Export
        col_meta, col_actions = st.columns([2, 1])
        with col_meta:
            analysis = analyze_expenses(expenses)
            st.info(analysis)
        
        with col_actions:
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Export CSV", data=csv, file_name="my_expenses.csv", mime="text/csv", use_container_width=True)
            
            # Danger Zone: Clear All
            if st.button("🧨 Clear All Data", type="secondary", use_container_width=True):
                st.session_state.confirm_delete = True
            
            if st.session_state.get('confirm_delete', False):
                st.warning("Are you sure? This cannot be undone.")
                c1, c2 = st.columns(2)
                if c1.button("Yes, Clear All", type="primary"):
                    clear_all_expenses()
                    st.session_state.confirm_delete = False
                    st.success("All data cleared!")
                    st.rerun()
                if c2.button("Cancel"):
                    st.session_state.confirm_delete = False
                    st.rerun()

        st.markdown("---")
        
        # Interactive Deletion via ID
        with st.expander("🛠️ Manage Records"):
            c1, c2 = st.columns([3, 1])
            selected_id = c1.selectbox("Select ID to Delete", df["ID"].tolist())
            if c2.button("Delete Selected", use_container_width=True):
                delete_expense(selected_id)
                st.success(f"ID {selected_id} deleted!")
                st.rerun()

        st.dataframe(df.sort_values(by="Date", ascending=False), use_container_width=True, hide_index=True)
    else:
        st.warning("No records found. Visit the 'Add Expense' tab to get started!")

# ---------------- VISUAL INSIGHTS ---------------- #

elif choice == "📊 Visual Insights":
    st.title("📊 Financial Data Visualization")
    
    expenses = fetch_expenses()
    if expenses:
        c1, c2 = st.columns([1, 1])
        
        with c1:
            st.subheader("Category Wise Split")
            pie = create_pie_chart(expenses)
            if pie:
                st.altair_chart(pie, use_container_width=True)
                
        with c2:
            st.subheader("Monthly Spending Trend")
            bar = create_bar_chart(expenses)
            if bar:
                st.altair_chart(bar, use_container_width=True)
    else:
        st.error("Not enough data to generate charts. Please add some expenses first.")

# ---------------- BUDGET RULES ---------------- #

elif choice == "🧮 Budget Rules":
    st.title("🧮 50-30-20 Budget Planner")
    st.markdown("""
    The **50-30-20 rule** is an easy way to budget your money:
    - **50%** for Needs (Must-haves)
    - **30%** for Wants (Treat yourself)
    - **20%** for Savings (Secure your future)
    """)
    
    income = st.number_input("Enter Your Monthly Income (₹)", min_value=0.0, step=1000.0)
    
    if income > 0:
        budget = calculate_budget(income)
        
        res1, res2, res3 = st.columns(3)
        res1.metric("🏠 Needs", f"₹{budget['Needs']:,.2f}")
        res2.metric("🎁 Wants", f"₹{budget['Wants']:,.2f}")
        res3.metric("💰 Savings", f"₹{budget['Savings']:,.2f}")
        
        st.progress(0.5) # Decorative progress
        st.info("💡 Try to prioritize the Savings category to build long-term wealth!")

# ---------------- CURRENCY TOOL ---------------- #

elif choice == "🌍 Currency Tool":
    st.title("🌍 Global Currency Converter")
    
    with st.container():
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            amount = st.number_input("Enter Amount", min_value=0.0)
        with c2:
            from_curr = st.selectbox("From", ["INR", "USD", "EUR", "GBP", "JPY", "CAD"])
        with c3:
            to_curr = st.selectbox("To", ["USD", "INR", "EUR", "GBP", "JPY", "CAD"], index=1)
            
        if st.button("Convert Now", use_container_width=True):
            with st.spinner("Fetching latest rates..."):
                result = convert_currency(amount, from_curr, to_curr)
                if isinstance(result, (int, float)):
                    st.success(f"### {amount} {from_curr} = {result:,.2f} {to_curr}")
                else:
                    st.error(result)