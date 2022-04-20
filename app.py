import os 
import io
import json
import boto3
import requests
import datetime 
import numpy as np
import pandas as pd
import streamlit  as st 
import matplotlib.pyplot as plt
from pandas.io.json import json_normalize
from boto3.dynamodb.conditions import Key, Attr
from openpyxl.workbook import Workbook

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def get_data():
    path = r'results.csv'
    return pd.read_csv(path)
    df = get_data()


data = get_data()



st.sidebar.subheader("Select Date Range:")


st.title("TSA Report Generator Dashboard")

col1, col2 = st.columns([1,1]) 

with col1:
    st.write(f"Total entries: {len(data.index)}")
with col2:
    st.write(f"Current Gross Total: {data['amount'].sum():,.2f} Ksh")



st.markdown("---")

data['creationDate'] = pd.to_datetime(data['creationDate']) 

data['creationDate'] = data['creationDate'].dt.strftime('%Y-%m')

summ = data.groupby(['creationDate'], as_index=False)['amount'].sum() 

# *********** Total Amount Per Month **********
st.subheader("Total Amount Per Month")

amount = summ["amount"]

st.write(f"January: {amount[0]:,.2f} Ksh")

st.write(f"February: {amount[1]:,.2f} Ksh")

st.write(f"March: {amount[2]:,.2f} Ksh") 

st.write(f"April: {amount[3]:,.2f} Ksh ")

st.markdown("---")
# *********** Total Amount Per Month **********


# *********** Value chain summary **********
valuechain = data.groupby(["valuechain"])["amount"].sum()
# st.dataframe(data)

st.title("Value chain summary")

col1, col2 = st.columns([1,1]) 

with col1:
    st.write(f"Macamadia: {valuechain.Macadamia:,.2f} Ksh")
with col2:
    st.write(f"Cashew: { valuechain.Cashew:,.2f} Ksh")
# *********** Value chain summary **********




def download_data(start_date, end_date):
    data = get_data()
    mask = (data['creationDate'] > start_date) & (data['creationDate'] <= end_date)
    data = data.loc[mask]

    data["creationDate"] = pd.to_datetime(data["creationDate"]) 
    data = data.sort_values(by="creationDate", ascending=False) 

    data['creationDate'] = pd.to_datetime(data['creationDate']).dt.date


    data_file_name = '1st February to 28th February TSA data.xlsx'

    data.to_excel(data_file_name) 

    st.sidebar.download_button( label="Download Data", data=data.to_csv().encode('utf-8'), mime="csv", file_name="selected_data.csv")


option = st.sidebar.selectbox(
     'Select Month:',
     ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"))


if 'January' in option:
    start_date = '2021-12-31'
    end_date = '2022-02-01' 
    download_data(start_date, end_date) 

if 'February' in option:# 
    feb_start_date = '2022-02-01'
    feb_end_date = '2022-03-01' 
    download_data(feb_start_date, feb_end_date) 

if 'March' in option:# 
    march_start_date1 = '2022-03-01'
    march_end_date1 = '2022-04-01' 
    download_data(march_start_date1, march_end_date1) 


if 'April' in option:
    start_date1 = '2022-04-01'
    end_date1 = '2022-04-30' 
    download_data(start_date1,end_date1) 


if 'May' in option:
    st.write("May data is not yet available")



if 'June' in option:
    st.write("June data is not yet available")
    

        
st.markdown("---")
st.subheader("General Analysis:")
general_data = data[["amount", "costperkg", "weight"]]
st.table(general_data.describe())        

st.markdown("---")
st.subheader("Monthly Analysis:")

months = st.sidebar.selectbox(
    "Select the Month to Analysis:",

    ["January", "February", "March", "April", "May"])

if "January" in months:
    st.subheader("January:")
    data = get_data()

    start_date = '2021-12-31'
    end_date = '2022-02-01'

    mask = (data['creationDate'] > start_date) & (data['creationDate'] <= end_date)
    data = data.loc[mask]

    data["creationDate"] = pd.to_datetime(data["creationDate"]) 
    data = data.sort_values(by="creationDate", ascending=False) 

    st.write(f"Total entries: {data['amount'].count()}")
  
    st.write(f"Total amount in January: {data['amount'].sum()}")

    # *********** Monthly Value chain summary **********
    st.error("Value chain was not available in January")




if "February" in months:
    st.subheader("February:")
    data = get_data()

    start_date = '2022-02-01'
    end_date = '2022-03-01' 

    mask = (data['creationDate'] > start_date) & (data['creationDate'] <= end_date)
    data = data.loc[mask]

    data["creationDate"] = pd.to_datetime(data["creationDate"]) 
    data = data.sort_values(by="creationDate", ascending=False) 

    st.write(f"Total entries: {data['amount'].count()}")
  
    st.write(f"Total amount in February: {data['amount'].sum()}")

    # *********** Monthly Value chain summary **********
    st.error("Value chain was not available in February")

if "March" in months:
    st.subheader("March:")
    data = get_data()

    start_date = '2022-03-01'
    end_date = '2022-04-01' 

    mask = (data['creationDate'] > start_date) & (data['creationDate'] <= end_date)
    data = data.loc[mask]

    data["creationDate"] = pd.to_datetime(data["creationDate"]) 
    data = data.sort_values(by="creationDate", ascending=False) 

    st.write(f"Total entries: {data['amount'].count()}")
  
    st.write(f"Total amount in March: {data['amount'].sum()}")



    # *********** Monthly Value chain summary **********
    march_valuechain = data.groupby(["valuechain"])["amount"].sum()

    st.title("March Value chain summary")

    col1, col2 = st.columns([1,1]) 

    with col1:
        st.write(f"Macamadia: {march_valuechain.Macadamia:.2f} Ksh")
    with col2:
        st.write(f"Cashew: { march_valuechain.Cashew:.2f} Ksh")
    # *********** Value chain summary **********

if "April" in months:
    st.subheader("April:")
    data = get_data()

    start_date = '2022-04-01'
    end_date = '2022-04-30' 

    mask = (data['creationDate'] > start_date) & (data['creationDate'] <= end_date)
    data = data.loc[mask]

    data["creationDate"] = pd.to_datetime(data["creationDate"]) 
    data = data.sort_values(by="creationDate", ascending=False) 

    st.write(f"Total entries: {data['amount'].count()}")
  
    st.write(f"Total amount in April: {data['amount'].sum()}")

    # *********** Monthly Value chain summary **********
    april_valuechain = data.groupby(["valuechain"])["amount"].sum()

    st.title("April Value chain summary")

    col1, col2 = st.columns([1,1]) 

    with col1:
        st.write(f"Macamadia: {april_valuechain.Macadamia:.2f} Ksh")
    with col2:
        st.write(f"Cashew: { april_valuechain.Cashew:.2f} Ksh")
    # *********** Value chain summary **********



if "May" in months:
    st.write("May data is not yet available")
    
if "June" in months:
    st.write("June data is not yet available")


hide_st_style = """
            <style>
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)   
