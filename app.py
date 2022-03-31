import os 
import io
import json
import boto3
import requests
import datetime 
import numpy as np
import pandas as pd
import  streamlit  as st 
import matplotlib.pyplot as plt
from pandas.io.json import json_normalize
from dynamodb_json import json_util as json 
from boto3.dynamodb.conditions import Key, Attr



columns = ["ConversationID", "amount",   "costperkg", "creationDate",    "mobileNumber", "OriginatorConversationID", "partnerId",    "ReferenceData",    "ResultCode",   "ResultDesc",   "ResultParameters", "ResultType", "TransactionID",  "transactionId",    "valuechain",   "weight"]
data = pd.read_csv("results.csv") 



st.sidebar.subheader("Select Date Range:")

db = boto3.resource("dynamodb") 

table = db.Table("payment")

start_date1 = st.sidebar.date_input(
     "Select the start date:",
     datetime.date(2022, 1, 1))


end_data1 = st.sidebar.date_input(
     "Select the end data:",
     datetime.date(2022, 12, 31))


st.title("TSA Report Generator Dashboard")

uploaded_files = pd.DataFrame(st.file_uploader("Choose the payment excel file", accept_multiple_files=False))


col1, col2 = st.columns([1,1]) 

with col1:
    st.write(f"Total entries: {table.item_count}")
with col2:
    st.write(f"Current Gross Total: {data['amount'].sum()}")



st.markdown("---")

data['creationDate'] = pd.to_datetime(data['creationDate']) 

data['creationDate'] = data['creationDate'].dt.strftime('%Y-%m')

summ = data.groupby(['creationDate'], as_index=False)['amount'].sum() 


st.subheader("Total Amout Per Month")

amount = summ["amount"]

st.write(f"January: {amount[0]}")

st.write(f"February: {amount[1]}")

st.write(f"March: {amount[2]}")

st.markdown("---")








#Update date  for the desired report 
start_date = end_data1
end_date = end_data1


# st.dataframe(table.scan())



st.sidebar.download_button(label="Download Data", data="", mime="text/csv", file_name="selected_data.xlsx")

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)   