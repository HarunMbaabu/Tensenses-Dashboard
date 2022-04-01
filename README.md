### Tensenses Dashboard for DigiFarm  

##### **Package:**

```
1). Boto3
2). Numpy 
3). Pandas 
4). Streamlit
5). Matplotlib
```
 


- Convert Payment table in AWS DynamoDB to a Data Frame 

```python
import json
import boto3
import numpy as np
import pandas as pd
import streamlit as st 
from pandas import json_normalize

db = boto3.resource("dynamodb", aws_access_key_id='*****', aws_secret_access_key='*****', region_name='*****') 

table = db.Table("payment") 

data = table.scan()

df = data["Items"] 

df1 = pd.DataFrame(df)

df1.to_csv('wholedata.csv', encoding='utf-8') 

```
