import pandas as pd
import json
from sklearn.linear_model import LogisticRegression
'''
import numpy as np
from sklearn import preprocessing
import matplotlib.pyplot as plt 
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split
import seaborn as sns
'''
weekday=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

df = pd.DataFrame(columns=['day', 'hour', 'percentage'])
data_json={}
with open('times.json') as json_data:
    data_json = json.load(json_data)

print (data_json)

i=0;
for data in data_json:
	day=weekday.index(data["name"])
	hour=0;
	for percentage in data["data"]:
		df.loc[i] = [day,hour,percentage]
		hour=hour+1
		i=i+1;

print(df)


X = df.iloc[:,0:2]
y = df.iloc[:,2]
print(X)
print (y)

classifier = LogisticRegression(random_state=0)
classifier.fit(X, y)
y_pred = classifier.predict(X)

print(y_pred)
#sklearn.linear_model.LinearRegression(fit_intercept=True, normalize=False, copy_X=True, n_jobs=1