import pandas as pd
from sklearn import preprocessing


columns = ['sepal_length','sepal_width','petal_length','petal_width','class']

dfIris = pd.read_csv('etl_scripts/featurestore/iris.txt', names=columns)

le = preprocessing.LabelEncoder()

dfIris['classEncoder'] = le.fit_transform(dfIris['class'])

print(dfIris.classEncoder.unique())

dfIris.to_csv('etl_scripts/featurestore/irisEncoder.txt', index=False)