import streamlit as st
import pandas as pd
import os
import re
from datetime import datetime

FILE_NAME = "expenses.csv"

# ==========================
# Init
# ==========================
if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=["date", "month", "description", "category", "amount"])
    df.to_csv(FILE_NAME, index=False)

# ==========================
# Helpers
# ==========================
def load_data():
    return pd.read_csv(FILE_NAME)


def save_data(df):
    df.to_csv(FILE_NAME, index=False)


def get_current_month():
    return datetime.now().strftime("%Y-%m")


def extract_amount(text):
    """
    Extracts first number from text like:
    'spent 5000 rs on petrol' -> 5000
    """
    match = re.search(r"(\d+\.?\d*)", text)
    if match:
        return float(match.group(1))
    return None

# ==========================
# UI
# ==========================
st.title("💰 Smart Expense Tracker (Auto Amount Detection)")

menu = st.sidebar.selectbox("Menu", [
    "Add Expense",
    "View Current Month",
    "View Previous Month",
    "Edit/Delete",
    "Analytics"
])

# ==========================
# Add Expense
# ==========================
if menu == "Add Expense":
    st.subheader("Add New Expense")

    desc = st.text_input("Describe your expense (e.g. 'spent 5000 rs on petrol')")
    category = st.selectbox("Category", ["Food", "Transport", "Shopping", "Bills", "Other"])

    if st.button("Add"):
        amount = extract_amount(desc)

        if amount is None:
            st.error("❌ Could not detect amount. Please include a number in description.")
        else:
            df = load_data()
            now = datetime.now()

            new_row = {
                "date": now.strftime("%Y-%m-%d"),
                "month": get_current_month(),
                "description": desc,
                "category": category,
                "amount": amount
            }

            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            save_data(df)

            st.success(f"✅ Expense Added! Detected Amount: {amount}")

# ==========================
# View Current Month
# ==========================
elif menu == "View Current Month":
    st.subheader("Current Month Expenses")

    df = load_data()
    current_month = get_current_month()

    filtered = df[df["month"] == current_month]

    if filtered.empty:
        st.info("No expenses this month")
    else:
        st.dataframe(filtered)
        st.write("Total:", filtered["amount"].sum())

# ==========================
# View Previous Month
# ==========================
elif menu == "View Previous Month":
    st.subheader("Previous Month Expenses")

    df = load_data()
    months = df["month"].unique()

    if len(months) == 0:
        st.info("No past data available")
    else:
        selected = st.selectbox("Select Month", months)
        filtered = df[df["month"] == selected]

        st.dataframe(filtered)
        st.write("Total:", filtered["amount"].sum())

# ==========================
# Edit/Delete
# ==========================
elif menu == "Edit/Delete":
    st.subheader("Edit or Delete Expenses")

    df = load_data()
    current_month = get_current_month()

    filtered = df[df["month"] == current_month]

    if filtered.empty:
        st.info("No data to edit")
    else:
        st.dataframe(filtered)
        idx = st.number_input("Enter row index", min_value=0, max_value=len(filtered)-1, step=1)

        if st.button("Delete"):
            df = df.drop(filtered.index[idx])
            save_data(df)
            st.success("🗑️ Deleted!")

        new_desc = st.text_input("New Description (include amount)")
        new_cat = st.selectbox("New Category", ["Food", "Transport", "Shopping", "Bills", "Other"])

        if st.button("Update"):
            new_amount = extract_amount(new_desc)

            if new_amount is None:
                st.error("❌ Could not detect amount in updated description")
            else:
                df.loc[filtered.index[idx], "description"] = new_desc
                df.loc[filtered.index[idx], "category"] = new_cat
                df.loc[filtered.index[idx], "amount"] = new_amount
                save_data(df)
                st.success("✏️ Updated!")

# ==========================
# Analytics (Graphs)
# ==========================
elif menu == "Analytics":
    st.subheader("📊 Spending Insights")

    df = load_data()

    if df.empty:
        st.info("No data for analysis")
    else:
        st.write("### Monthly Spending")
        monthly = df.groupby("month")["amount"].sum()
        st.line_chart(monthly)

        st.write("### Category Breakdown")
        category = df.groupby("category")["amount"].sum()
        st.bar_chart(category)

# ----------------------------------
# import streamlit as st
# import pandas as pd
# import os
# from datetime import datetime

# FILE_NAME = "expenses.csv"

# # ==========================
# # Init
# # ==========================
# if not os.path.exists(FILE_NAME):
#     df = pd.DataFrame(columns=["date", "month", "description", "category", "amount"])
#     df.to_csv(FILE_NAME, index=False)

# # ==========================
# # Helpers
# # ==========================
# def load_data():
#     return pd.read_csv(FILE_NAME)


# def save_data(df):
#     df.to_csv(FILE_NAME, index=False)


# def get_current_month():
#     return datetime.now().strftime("%Y-%m")


# # ==========================
# # UI
# # ==========================
# st.title("💰 Smart Expense Tracker")

# menu = st.sidebar.selectbox("Menu", [
#     "Add Expense",
#     "View Current Month",
#     "View Previous Month",
#     "Edit/Delete",
#     "Analytics"
# ])

# # ==========================
# # Add Expense
# # ==========================
# if menu == "Add Expense":
#     st.subheader("Add New Expense")

#     desc = st.text_input("Description")
#     category = st.selectbox("Category", ["Food", "Transport", "Shopping", "Bills", "Other"])
#     amount = st.number_input("Amount", min_value=0.0)

#     if st.button("Add"):
#         df = load_data()
#         now = datetime.now()

#         new_row = {
#             "date": now.strftime("%Y-%m-%d"),
#             "month": get_current_month(),
#             "description": desc,
#             "category": category,
#             "amount": amount
#         }

#         df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
#         save_data(df)

#         st.success("Expense Added!")

# # ==========================
# # View Current Month
# # ==========================
# elif menu == "View Current Month":
#     st.subheader("Current Month Expenses")

#     df = load_data()
#     current_month = get_current_month()

#     filtered = df[df["month"] == current_month]

#     if filtered.empty:
#         st.info("No expenses this month")
#     else:
#         st.dataframe(filtered)
#         st.write("Total:", filtered["amount"].sum())

# # ==========================
# # View Previous Month
# # ==========================
# elif menu == "View Previous Month":
#     st.subheader("Previous Month Expenses")

#     df = load_data()
#     months = df["month"].unique()

#     selected = st.selectbox("Select Month", months)

#     filtered = df[df["month"] == selected]

#     st.dataframe(filtered)
#     st.write("Total:", filtered["amount"].sum())

# # ==========================
# # Edit/Delete
# # ==========================
# elif menu == "Edit/Delete":
#     st.subheader("Edit or Delete Expenses")

#     df = load_data()
#     current_month = get_current_month()

#     filtered = df[df["month"] == current_month]

#     if filtered.empty:
#         st.info("No data to edit")
#     else:
#         idx = st.number_input("Enter row index", min_value=0, max_value=len(filtered)-1, step=1)

#         if st.button("Delete"):
#             df = df.drop(filtered.index[idx])
#             save_data(df)
#             st.success("Deleted!")

#         new_desc = st.text_input("New Description")
#         new_cat = st.selectbox("New Category", ["Food", "Transport", "Shopping", "Bills", "Other"])
#         new_amt = st.number_input("New Amount", min_value=0.0)

#         if st.button("Update"):
#             df.loc[filtered.index[idx], "description"] = new_desc
#             df.loc[filtered.index[idx], "category"] = new_cat
#             df.loc[filtered.index[idx], "amount"] = new_amt
#             save_data(df)
#             st.success("Updated!")

# # ==========================
# # Analytics (Graphs)
# # ==========================
# elif menu == "Analytics":
#     st.subheader("📊 Spending Insights")

#     df = load_data()

#     if df.empty:
#         st.info("No data for analysis")
#     else:
#         st.write("### Monthly Spending")
#         monthly = df.groupby("month")["amount"].sum()
#         st.line_chart(monthly)

#         st.write("### Category Breakdown")
#         category = df.groupby("category")["amount"].sum()
#         st.bar_chart(category)
