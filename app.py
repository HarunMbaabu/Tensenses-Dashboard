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
from boto3.dynamodb.conditions import Key, Attr


with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)



# columns = ["ConversationID", "amount",   "costperkg", "creationDate",    "mobileNumber", "OriginatorConversationID", "partnerId",    "ReferenceData",    "ResultCode",   "ResultDesc",   "ResultParameters", "ResultType", "TransactionID",  "transactionId",    "valuechain",   "weight"]


def get_data():
    path = r'results.csv'
    return pd.read_csv(path)
    df = get_data()


data = get_data()



st.sidebar.subheader("Select Date Range:")

db = boto3.resource("dynamodb", aws_access_key_id='AKIATHTMAO23VZXNEIOV', aws_secret_access_key='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', region_name='eu-west-1') 
table = db.Table("payment")


st.title("TSA Report Generator Dashboard")

col1, col2 = st.columns([1,1]) 

with col1:
    st.write(f"Total entries: {table.item_count}")
with col2:
    st.write(f"Current Gross Total: {data['amount'].sum():.2f} Ksh")



st.markdown("---")

data['creationDate'] = pd.to_datetime(data['creationDate']) 

data['creationDate'] = data['creationDate'].dt.strftime('%Y-%m')

summ = data.groupby(['creationDate'], as_index=False)['amount'].sum() 

# *********** Total Amount Per Month **********
st.subheader("Total Amount Per Month")

amount = summ["amount"]

st.write(f"January: {amount[0]:.2f} Ksh")

st.write(f"February: {amount[1]:.2f} Ksh")

st.write(f"March: {amount[2]:.2f} Ksh") 

st.write(f"April: {amount[3]:.2f} Ksh ")

st.markdown("---")
# *********** Total Amount Per Month **********


# *********** Value chain summary **********
valuechain = data.groupby(["valuechain"])["amount"].sum()
# st.dataframe(data)

st.subheader("Value chain summary")

col1, col2 = st.columns([1,1]) 

with col1:
    st.write(f"Macamadia: {valuechain.Macadamia:.2f} Ksh")
with col2:
    st.write(f"Cashew: {valuechain.Cashew:.2f} Ksh")
# *********** Value chain summary **********




option = st.sidebar.selectbox(
     'Select Your Target Month:',
     ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"))




# mask = (data['creationDate'] > start_date) & (data['creationDate'] <= end_date)
# mydf = data.loc[mask]


# st.title("View the selected data")
# st.dataframe(mydf)


st.sidebar.download_button( label="Download Data", data=data.to_csv().encode('utf-8'), mime="csv", file_name="selected_data.csv")

hide_st_style = """
            <style>
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)   
