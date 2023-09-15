import os
import pandas as pd
import streamlit as st

# ...

# Move the code for reading data from CSV outside the get_data function
path = 'tsa data.csv'
data = pd.read_csv(path)

# ...

def download_data(start_date, end_date):
    mask = (data['creationDate'] > start_date) & (data['creationDate'] <= end_date)
    filtered_data = data.loc[mask]

    filtered_data["creationDate"] = pd.to_datetime(filtered_data["creationDate"])
    filtered_data = filtered_data.sort_values(by="creationDate", ascending=False)

    data_file_name = f'{start_date} to {end_date} TSA data.xlsx'
    filtered_data.to_excel(data_file_name)

    st.sidebar.download_button(label="Download Data", data=filtered_data.to_csv().encode('utf-8'),
                               mime="csv", file_name="selected_data.csv")

# ...

if 'July' in option:  # Potential typo, change one of these to 'August' if needed
    August_start_date1 = '2022-08-01'
    August_end_date1 = '2022-08-31'
    download_data(August_start_date1, August_end_date1)

# ...

if "May" in months:
    st.subheader("May: ")
    data = get_data()

    start_date = '2022-05-01'
    end_date = '2022-05-31'

    mask = (data['creationDate'] > start_date) & (data['creationDate'] <= end_date)
    data = data.loc[mask]

    data["creationDate"] = pd.to_datetime(data["creationDate"])
    data = data.sort_values(by="creationDate", ascending=False)

    st.write(f"Total entries: {data['amount'].count()}")
  
    st.write(f"Total amount in May: {data['amount'].sum()}")

    # *********** Monthly Value chain summary **********
    may_valuechain = data.groupby(["valuechain"])["amount"].sum()

    st.title("May Value chain summary")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.write(f"Macadamia: {may_valuechain.Macadamia:.2f} Ksh")
    with col2:
        st.write("In May only Macadamia is available")
    # *********** Value chain summary **********
