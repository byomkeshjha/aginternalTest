import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import os
st.write("Credential file found:", os.path.exists("agrimindstest-07296ef8be0esheet.json"))


# Google Sheets setup
def get_google_sheet(sheet_name):
    # Authenticate with Google Sheets
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("agrimindstest-d085ce911088.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).sheet1  # Open the first sheet
    return sheet

# Add entry to Google Sheet
def add_to_sheet(sheet, data):
    sheet.append_row(data)

# Fetch data from Google Sheet
def fetch_data(sheet):
    records = sheet.get_all_records()
    return pd.DataFrame(records)

# Streamlit App
def main():
    st.title("Daily Milk Collection App")

    # Google Sheet
    sheet_name = "Milk Collection"  # Replace with your sheet name
    sheet = get_google_sheet(sheet_name)

    # Sidebar for navigation
    menu = ["Add Entry", "Summary View"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add Entry":
        st.subheader("Add Farmer Details")

        # Form to collect data
        with st.form(key="entry_form"):
            date = st.date_input("Date")
            farmer_name = st.text_input("Farmer Name")
            farmer_number = st.text_input("Farmer Number")
            milk_sample = st.text_input("Milk Sample Number")
            milk_rate = st.number_input("Milk Rate (₹)", step=0.01)
            fat = st.number_input("Fat (%)", step=0.01)
            snf = st.number_input("SNF (%)", step=0.01)
            protein = st.number_input("Protein (%)", step=0.01)
            quantity = st.number_input("Quantity (liters)", step=0.01)

            submit = st.form_submit_button("Submit")

        # Add data to Google Sheet
        if submit:
            data = [
                str(date),
                farmer_name,
                farmer_number,
                milk_sample,
                milk_rate,
                fat,
                snf,
                protein,
                quantity,
            ]
            add_to_sheet(sheet, data)
            st.success("Entry added successfully!")

    elif choice == "Summary View":
        st.subheader("Summary View")
        # Fetch data
        data = fetch_data(sheet)
        if not data.empty:
            st.dataframe(data)
            st.write("### Summary Statistics")
            st.write(data.describe())
        else:
            st.warning("No data available.")

if __name__ == "__main__":
    main()
