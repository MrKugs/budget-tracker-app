import streamlit as st
import pandas as pd
from datetime import date

# 1. Initialize session state to store the list of expenses
if 'expenses_list' not in st.session_state:
    st.session_state.expenses_list = []

# Title of the app
st.title("Personal Budget Tracker")

# Form section to add a new expense
st.subheader("Add a New Expense")

# Create a container or visually group the inputs (optional, but matches the neat look)
with st.container():
    # Input fields
    expense_date = st.date_input("Date", value=date.today())
    expense_item = st.text_input("Expense Item")
    # Using text_input for amount to manually handle the "not a number" exception requirement
    amount_spent_str = st.text_input("Amount Spent (RM)") 
    
    # Submit button
    submit_btn = st.button("Add Expense")

    # Action when the button is clicked
    if submit_btn:
        if not expense_item:
            st.warning("Please enter an Expense Item.")
        else:
            # 3. Use exception handling
            try:
                # Try to convert the input string to a float (number)
                amount = float(amount_spent_str)
                
                # Check if the amount is negative
                if amount < 0:
                    st.error("Amount Spent cannot be negative.")
                else:
                    # If valid, save the expense to session state
                    new_expense = {
                        "Date": expense_date.strftime("%Y-%m-%d"),
                        "Expense Item": expense_item,
                        "Amount Spent (RM)": amount
                    }
                    st.session_state.expenses_list.append(new_expense)
                    st.success(f"Expense '{expense_item}' added successfully!")
                    
            except ValueError:
                # Catch the error if the conversion to float fails (e.g., user typed text)
                st.error("Invalid input. Please ensure Amount Spent is a number.")

st.markdown("---")

# 4. Display all expenses in a table
st.subheader("Expense Summary")

# Check if there are any expenses recorded yet
if st.session_state.expenses_list:
    # Convert the list of dictionaries into a Pandas DataFrame for easy table display
    df = pd.DataFrame(st.session_state.expenses_list)
    
    # Display the table with formatting for 2 decimal places
    st.table(df.style.format({"Amount Spent (RM)": "{:.2f}"}))
    
    # Calculate total amount
    total_expenses = df["Amount Spent (RM)"].sum()
    
    # Display total amount at the bottom
    st.markdown(f"**Total Expenses: RM {total_expenses:.2f}**")
else:
    st.info("No expenses recorded yet. Add an expense above to see the summary.")
