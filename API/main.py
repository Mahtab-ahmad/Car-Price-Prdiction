from fastapi import FastAPI
from  pydantic import BaseModel,Field
from typing import Annotated,Literal
import pickle
from fastapi.responses import JSONResponse
import numpy as np


with open('pipeline.pkl','rb') as f:
    model = pickle.load(f)

class Car(BaseModel):

    name: Annotated[str,Field(max_length=30,description='Enter the full name of the car',examples=['Maruti Swift VDI'])] 

    year: Annotated[int,Field(description='Enter the year',examples=['2004'])]

    km_driven: Annotated[int,Field('How many kms has been driven',examples=[75000])]

    fuel:Annotated[Literal['Petrol', 'Diesel', 'CNG'],Field(description='Enter the fuel type of the car',examples=['Diesel'])]

    seller_type: Annotated[Literal['Individual', 'Dealer', 'Trustmark Dealer'],Field(description='Enter the seller type',examples=['Dealer'])]

    transmission: Annotated[Literal['Manual', 'Automatic'],Field(description='Enter the transmission',examples=['Manual'])]

    owner: Annotated[Literal['Second Owner', 'First Owner', 'Fourth & Above Owner',
       'Third Owner'],Field(description='Enter the owner',examples=['Second Owner'])]

    mileage : Annotated[float,Field(description='Enter the mileage in km/ltr/kg',examples=[20.9])]

    engine: Annotated[float,Field(description='Enter the engine in cc(cubic centimeter)',examples=[992.2])]
    max_power: Annotated[float,Field(description='Enter the maximum engine power of the car in bhp',examples=[76.0])]
    seats: Annotated[int,Field(description='Number of seats', examples=[5])]



app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can later replace * with your frontend domain for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
@app.get('/home')
def home():
    return {'message':'Car Price Predictor'}

@app.post('/predict')
def predict(car: Car):

    input = np.array([[car.name,car.year,car.km_driven,car.fuel,car.seller_type,car.transmission,car.owner,car.mileage,car.engine,car.max_power,car.seats]])

    prediction = model.predict(input)[0]

    return JSONResponse(status_code = 200,content = {'Prediction': prediction})