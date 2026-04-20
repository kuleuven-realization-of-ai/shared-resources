from random import gauss

from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "People"}


@app.get("/get_prediction")
def get_prediction(feature_a: float, feature_b: float):
    return {"predictions": [gauss(mu=feature_a, sigma=feature_b),
                            gauss(mu=feature_a, sigma=feature_b)]}


if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')
