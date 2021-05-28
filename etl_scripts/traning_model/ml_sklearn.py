import mlflow
import mlflow.sklearn
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
from urllib.parse import urlparse

iris = pd.read_csv('etl_scripts/featurestore/irisEncoder.txt', sep=",")

X_train, X_test, y_train, y_test = train_test_split(iris.drop(['classEncoder','class'], axis=1), iris['classEncoder'], test_size=0.33)

try:
    idExperiment = mlflow.create_experiment('IrisClassificacao')
except:
    idExperiment = mlflow.get_experiment_by_name('IrisClassificacao').experiment_id

with mlflow.start_run(experiment_id=idExperiment):
    mlflow.log_param("max_depth", 2)
    mlflow.log_param("random_state", 0)

    clf = RandomForestClassifier(max_depth=2, random_state=0)
    clf.fit(X_train, y_train)
    predictCLF  = clf.predict(X_test)

    mlflow.log_metric("accuracy_score", accuracy_score(y_test,predictCLF))


    tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

    if tracking_url_type_store != "file":
        mlflow.sklearn.log_model(clf, "model", registered_model_name='ModeloIris')
    else:
        mlflow.sklearn.log_model(clf, "model")