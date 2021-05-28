from fastapi import FastAPI, HTTPException
from util import getModel
import schemas

app = FastAPI(title="Iris Prediction API",
    description="Data Pipeline using jenkins + mlflow + Google cloud build + kubernetes + fastapi + github + python + linux \o/ :)",
    version="1.0.0",
)

modelFile = open("model.pkl", 'rb')
predictModel = getModel(modelFile).model()

Iris = ['Iris-setosa','Iris-versicolor', 'Iris-virginica']

@app.post("/predict'")
def predict(request:schemas.Iris):
    try:
        predictmodel = predictModel.predict([[
            request.sepal_length, 
            request.sepal_width, 
            request.petal_length, 
            request.petal_width
        ]])
        return {"Predict": Iris[predictmodel[0]]}
    except:
        raise HTTPException(status_code=404)
