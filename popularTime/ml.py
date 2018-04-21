import pandas as pd
import json
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import PolynomialFeatures
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
		if(hour+1>9 and hour+1<20):
			df.loc[i] = [day,hour+1,percentage]
			
			i=i+1;
		hour=hour+1


print(df)


X = df.iloc[:,0:2]
X = X.astype('int')
y = df.iloc[:,2]
y=y.astype('float')
print(X)
print (y)
poly = PolynomialFeatures(degree=5)
X= poly.fit_transform(X)
classifier = LogisticRegression(random_state=0,C=10)
classifier.fit(X, y)
y_pred = classifier.score(X,y)

print(y_pred)
#sklearn.linear_model.LinearRegression(fit_intercept=True, normalize=False, copy_X=True, n_jobs=1