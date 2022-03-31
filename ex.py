import datetime 
import  streamlit  as st 

d = st.date_input(
     "When's your birthday",
     datetime.date(2022, 10, 22))
st.write('Your birthday is:', d)