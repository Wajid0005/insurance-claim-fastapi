# 🏥 Insurance Claim Prediction API

<div align="center">

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-2C3E50?style=for-the-badge&logo=gunicorn&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-%23E11D48.svg?style=for-the-badge&logo=pydantic&logoColor=white)
![Railway](https://img.shields.io/badge/Railway-0B0D0E?style=for-the-badge&logo=railway&logoColor=white)

A production-ready, high-performance machine learning microservice that predicts health insurance claim categories using demographic, financial, and clinical health inputs.

🚀 **Live Production API:** [https://insurance-claim-fastapi-production.up.railway.app/](https://insurance-claim-fastapi-production.up.railway.app/)  
📖 **Interactive Swagger UI Docs:** [https://insurance-claim-fastapi-production.up.railway.app/docs](https://insurance-claim-fastapi-production.up.railway.app/docs)  
📕 **Alternative ReDoc Docs:** [https://insurance-claim-fastapi-production.up.railway.app/redoc](https://insurance-claim-fastapi-production.up.railway.app/redoc)

</div>

---

## ⚡ Deployment Challenges Faced (And How We Solved Them)

> [!WARNING]
> ### 😭 The Python 3.13 Builder Trap & The NXDOMAIN Nightmare
> Deploying machine learning models to the cloud can be highly frustrating. During this project's deployment to Railway, we faced a series of nerve-wrecking errors that almost made us cry:
>
> 1. **The Compiling-from-Source Error:**
>    Railway's default builder automatically selected the brand-new **Python 3.13.13**. Because older versions of `pandas` (`2.1.3`) and `scikit-learn` (`1.3.2`) do not have precompiled binaries (wheels) compatible with Python 3.13's updated internal C-API, `pip` was forced to compile them from source. This triggered a massive Cython compilation error:
>    `error: too few arguments to function ‘_PyLong_AsByteArray’`
>    The build failed repeatedly, and no web server started.
>
> 2. **The DNS Caching Illusion:**
>    Because the initial build failed, opening the live URL resulted in a `DNS_PROBE_FINISHED_NXDOMAIN` (domain name not found) error. Once we fixed the build, the site was **100% online**, but local Windows PCs and home routers kept serving the old cached negative DNS results, making it look like the deployment was still broken!
>
> ### 💡 The Heroic Solution:
> * **Python Version Pinning:** We created `.python-version` and `runtime.txt` files to explicitly pin the deployment environment to **Python 3.11**. On Python 3.11, pre-built binary wheels are readily available on PyPI. The build succeeded instantly in just seconds!
> * **DNS Cache Clearing:** We flushed the Windows DNS cache (`ipconfig /flushdns`) and cleared Chrome's secret host cache (`chrome://net-internals/#dns`) to force the local PC to look up the newly routed Railway live server.

---

## 🛠️ Tech Stack & Key Libraries

* **[FastAPI](https://fastapi.tiangolo.com/)**: Modern, fast (high-performance), web framework for building APIs with Python.
* **[Uvicorn](https://www.uvicorn.org/)**: A lightning-fast ASGI server implementation, serving our FastAPI app.
* **[Pandas](https://pandas.pydata.org/)**: High-performance data structure manipulation for converting incoming JSON data into DataFrames.
* **[Scikit-Learn](https://scikit-learn.org/)**: The underlying engine that powers `model.pkl` to produce instant machine learning classifications.
* **[Pydantic](https://docs.pydantic.dev/)**: Ensures robust, strict validation for every incoming request body, returning instant `422 Unprocessable Entity` responses for malformed data.
* **[Joblib](https://joblib.readthedocs.io/)**: Provides lightweight pipelining to deserialize and load the serialized ML model file.

---

## 🚀 Quick Start (Local Development)

### 1. Setup Environment & Clone
```bash
git clone https://github.com/Wajid0005/insurance-claim-fastapi.git
cd insurance-claim-fastapi
```

### 2. Create and Activate Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the API locally
```bash
uvicorn app:app --reload
```
The local API will load at `http://127.0.0.1:8000`. 

---

## 🚂 Railway Deployment Guide

This project is pre-configured for zero-config Railway deployment!

### ⚙️ Configuration Files Added:
* **`Procfile`**: Instructs Railway how to run the web server:
  `web: uvicorn app:app --host 0.0.0.0 --port $PORT`
* **`.python-version` / `runtime.txt`**: Pins the Python runtime environment to `3.11` to prevent C-compilation errors of Pandas and Scikit-Learn.

---

## 🛠️ API Reference & Request Signatures

### 1. Health Check
Checks if the API is running correctly.
* **Endpoint:** `GET /health`
* **Response:**
  ```json
  {
    "status": "healthy"
  }
  ```

### 2. Predict Claim Category
Predicts the claim category and outputs prediction probabilities for all classification brackets.
* **Endpoint:** `POST /predict`
* **Headers:** `Content-Type: application/json`
* **Request Payload Format:**
  ```json
  {
    "gender": "female",
    "age": 35,
    "marital_status": "married",
    "state": "karnataka",
    "occupation_type": "salaried",
    "annual_income_inr": 850000.0,
    "weight_kg": 68.5,
    "height_m": 1.65,
    "tobacco_usage": "none",
    "alcohol_units_per_week": 2,
    "physical_activity_level": "medium",
    "has_diabetes_hypertension": "Neither"
  }
  ```
* **Success Response:**
  ```json
  {
    "predicted_claim_category": "Moderate",
    "calculated_bmi": 25.16,
    "prediction_probability": {
      "Low": 0.1245,
      "Moderate": 0.7251,
      "High": 0.1504
    }
  }
  ```

---

## 📂 Project Directory Map

```
├── app.py                  # Core FastAPI application & ML request routing
├── model.pkl               # Serialized ML model
├── requirements.txt        # Pinned Python package dependencies
├── Procfile                # Tells Railway how to run your app
├── .python-version         # Pins Python 3.11 for Nixpacks
├── runtime.txt             # Compatibility fallback for Python versioning
└── README.md               # Visual Documentation (This file)
```
