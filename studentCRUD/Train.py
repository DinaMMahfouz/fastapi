import pandas as pd
from pycaret.classification import setup, compare_models, save_model

data = pd.read_csv("Student_performance_data _.csv")

print(data.columns.tolist())

clf = setup(
    data=data,
    target="GradeClass",
    session_id=123,

    numeric_features=[
        "Age",
        "StudyTimeWeekly",
        "Absences",
        
    ],

    categorical_features=[
        "Gender",
        "Ethnicity",
        "ParentalEducation",
        "Tutoring",
        "ParentalSupport",
        "Extracurricular",
        "Sports",
        "Music",
        "Volunteering"
    ],

    ignore_features=[
        "StudentID", "GPA"
    ]
)

best_model = compare_models()

save_model(best_model, "student_performance_model")

print("Model saved")

