from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


class BMIOutput(BaseModel):
    bmi: float
    message: str


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "BMI API is running"}


@app.get("/bmi", response_model=BMIOutput)
def calculate_bmi(
    weight: float = Query(..., gt=20),
    height: float = Query(..., gt=0)
):
    bmi = weight / (height ** 2)

    if bmi < 18.5:
        message = "Underweight"
    elif bmi < 25:
        message = "Normal weight"
    elif bmi < 30:
        message = "Overweight"
    else:
        message = "Obese"

    return BMIOutput(
        bmi=round(bmi, 2),
        message=message
    )