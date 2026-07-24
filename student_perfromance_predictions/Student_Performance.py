from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pycaret.classification import predict_model, load_model
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = load_model("student_performance_model")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/predict")
async def predict(
    Age: int=Query(..., description="Age of the student"),
    StudyTimeWeekly: float=Query(..., description="Average study time per week"),
    Absences: int=Query(..., description="Number of absences"),
    GPA: float=Query(..., description="GPA of the student"),
    Gender: int=Query(..., description="Gender of the student 1 for male and 0 for female"),
    Ethnicity: int=Query(..., description="Ethnicity of the student 1 Asian, 2 African American, 3 Caucasian, 4 Hispanic, 5 Other, 6 Unknown"),
    ParentalEducation: int=Query(..., description="Parental education of the student 1 for yes and 0 for no"),
    Tutoring: int=Query(..., description="Tutoring of the student 1 for yes and 0 for no"),
    ParentalSupport: int=Query(..., description="Parental support of the student 1 for yes and 0 for no"),
    Extracurricular: int=Query(..., description="Extracurricular activities of the student 1 for yes and 0 for no"),
    Sports: int=Query(..., description="Sports activities of the student 1 for yes and 0 for no"),
    Music: int=Query(..., description="Music activities of the student 1 for yes and 0 for no"),
    Volunteering: int=Query(..., description="Volunteering activities of the student 1 for yes and 0 for no"),
):
    data = {
        "Age": Age,
        "StudyTimeWeekly": StudyTimeWeekly,
        "Absences": Absences,
        "GPA": GPA,
        "Gender": Gender,
        "Ethnicity": Ethnicity,
        "ParentalEducation": ParentalEducation,
        "Tutoring": Tutoring,
        "ParentalSupport": ParentalSupport,
        "Extracurricular": Extracurricular,
        "Sports": Sports,
        "Music": Music,
        "Volunteering": Volunteering,
    }

    df = pd.DataFrame([data])

    prediction = predict_model(model, data=df)

    predicted_grade = int(prediction["prediction_label"].iloc[0])

    grade_map = {
        0: "A",
        1: "B",
        2: "C",
        3: "D",
        4: "F",
    }

    grade = grade_map.get(predicted_grade, "Unknown")

    return {
        "Grade": grade,
        "GradeClass": predicted_grade,
    }