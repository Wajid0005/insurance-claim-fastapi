import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, computed_field
from typing import Literal, Annotated
import pandas as pd
import joblib

# =====================================================
# LOAD MODEL
# =====================================================

try:
    model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
    model = joblib.load(model_path)
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# =====================================================
# CREATE FASTAPI APP
# =====================================================

app = FastAPI(
    title="Insurance Claim Prediction API",
    description="Predict Insurance Claim Category",
    version="1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# INPUT VALIDATION CLASS
# =====================================================

class InsuranceInput(BaseModel):

    # -----------------------------
    # BASIC DETAILS
    # -----------------------------

    gender: Literal["male", "female"]

    age: Annotated[
        int,
        Field(
            gt=0,
            le=120,
            description="Age of the user"
        )
    ]

    marital_status: Literal[
        "single",
        "married",
        "divorced",
        "widowed"
    ]

    state: Literal[
        "tamil nadu",
        "karnataka",
        "west bengal",
        "delhi",
        "uttar pradesh",
        "maharashtra"
    ]

    occupation_type: Literal[
        "salaried",
        "self_employed",
        "student",
        "retired",
        "business",
        "unemployed"
    ]

    # -----------------------------
    # FINANCIAL DETAILS
    # -----------------------------

    annual_income_inr: Annotated[
        float,
        Field(
            gt=0,
            description="Annual income in INR"
        )
    ]

    # -----------------------------
    # HEALTH DETAILS
    # -----------------------------

    weight_kg: Annotated[
        float,
        Field(
            gt=0,
            le=300,
            description="Weight in Kilograms"
        )
    ]

    height_m: Annotated[
        float,
        Field(
            gt=0.5,
            le=2.5,
            description="Height in Meters"
        )
    ]

    tobacco_usage: Literal[
        "both",
        "chewing",
        "none",
        "smoking"
    ]

    alcohol_units_per_week: Annotated[
        int,
        Field(
            ge=0,
            le=11,
            description="Alcohol units consumed per week"
        )
    ]

    physical_activity_level: Literal[
        "low",
        "medium",
        "high"
    ]

    has_diabetes_hypertension: Literal[
        "Neither",
        "Only Hypertension",
        "Only Diabetes",
        "Both Diabetes & Hypertension"
    ]

    # =====================================================
    # COMPUTED BMI
    # =====================================================

    @computed_field
    @property
    def bmi(self) -> float:

        bmi_value = self.weight_kg / (self.height_m ** 2)

        return round(bmi_value, 2)

# =====================================================
# ROOT ENDPOINT
# =====================================================

@app.get("/")
def home():

    return {
        "message": "Insurance Claim Prediction API Running Successfully"
    }

# =====================================================
# PREDICTION ENDPOINT
# =====================================================

@app.post("/predict")
def predict_claim(data: InsuranceInput):

    if model is None:
        return JSONResponse(
            status_code=500,
            content={"error": "Model not loaded"}
        )

    # ---------------------------------------------
    # CREATE INPUT DICTIONARY
    # ---------------------------------------------

    input_dict = {

        "gender": data.gender,

        "age": data.age,

        "marital_status": data.marital_status,

        "state": data.state,

        "occupation_type": data.occupation_type,

        "annual_income_inr": data.annual_income_inr,

        "bmi": data.bmi,

        "tobacco_usage": data.tobacco_usage,

        "alcohol_units_per_week": data.alcohol_units_per_week,

        "physical_activity_level": data.physical_activity_level,

        "has_diabetes_hypertension": data.has_diabetes_hypertension
    }

    # ---------------------------------------------
    # CONVERT TO DATAFRAME
    # ---------------------------------------------

    input_df = pd.DataFrame([input_dict])

    # ---------------------------------------------
    # MAKE PREDICTION
    # ---------------------------------------------

    prediction = model.predict(input_df)[0]

    # ---------------------------------------------
    # RESPONSE
    # ---------------------------------------------

    response = {

        "predicted_claim_category": prediction,

        "calculated_bmi": data.bmi
    }

    # ---------------------------------------------
    # PREDICTION PROBABILITIES
    # ---------------------------------------------

    if hasattr(model, "predict_proba"):

        probabilities = model.predict_proba(input_df)[0]

        response["prediction_probability"] = {

            str(cls): round(float(prob), 4)

            for cls, prob in zip(model.classes_, probabilities)
        }

    # ---------------------------------------------
    # RETURN RESPONSE
    # ---------------------------------------------

    return JSONResponse(
        status_code=200,
        content=response
    )

# =====================================================
# HEALTH CHECK
# =====================================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }
