# 🏥 Insurance Claim Prediction API

A modern, high-performance **FastAPI** application that predicts insurance claim categories based on demographic, health, and financial data. The application utilizes a trained machine learning model (`model.pkl`) to run predictions in real-time.

---

## 🚀 Quick Start (Local Development)

### 1. Prerequisites
Ensure you have **Python 3.10+** installed on your system.

### 2. Setup Environment
Clone the repository and navigate into the project directory:
```bash
git clone <your-repo-url>
cd "Insurance Predictor"
```

Create and activate a virtual environment:
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

### 4. Run the Application
Start the FastAPI server using `uvicorn`:
```bash
uvicorn app:app --reload
```
The API will be available at `http://127.0.0.1:8000`. 
- Access the interactive documentation at `http://127.0.0.1:8000/docs`
- Access the alternative documentation at `http://127.0.0.1:8000/redoc`

---

## 🚂 Railway Deployment Guide

This project is pre-configured for seamless deployment to **Railway**!

### Method 1: Deploy via GitHub (Recommended)
1. **Push your code to GitHub**:
   Make sure you commit all files including the newly added `Procfile` and updated `requirements.txt`:
   ```bash
   git add .
   git commit -m "Configure project for Railway deployment"
   git push origin main
   ```
2. **Go to Railway**:
   - Log in to your [Railway Dashboard](https://railway.app/).
   - Click **+ New Project** -> **Deploy from GitHub repo**.
   - Select your repository.
3. **Automatic Deployment**:
   - Railway will auto-detect the Python project using `requirements.txt`.
   - It will automatically execute the command in your `Procfile`:
     `web: uvicorn app:app --host 0.0.0.0 --port $PORT`
   - Railway dynamically injects the `$PORT` environment variable, ensuring the app binds correctly.
4. **Generate a Domain**:
   - Once deployment completes, go to your service's **Settings** tab in Railway.
   - Under the **Networking** section, click **Generate Domain** (or set a custom domain).
   - Your API is now live!

### Method 2: Deploy via Railway CLI
If you prefer deploying directly from your local terminal:
1. Install the Railway CLI:
   ```bash
   npm i -g @railway/cli
   ```
2. Log in and link your project:
   ```bash
   railway login
   railway link
   ```
3. Deploy:
   ```bash
   railway up
   ```

---

## 🛠️ API Reference

### 1. Health Check
Checks if the API is running correctly.

* **URL**: `/health`
* **Method**: `GET`
* **Response**:
  ```json
  {
    "status": "healthy"
  }
  ```

### 2. Predict Claim Category
Predicts the claim category and returns probabilities.

* **URL**: `/predict`
* **Method**: `POST`
* **Headers**: `Content-Type: application/json`
* **Request Body Example**:
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
* **Response Example**:
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

## 📂 Project Structure

```
├── app.py                  # Core FastAPI application & prediction logic
├── model.pkl               # Pre-trained Scikit-Learn model
├── requirements.txt        # Python dependency list
├── Procfile                # Startup command configuration for Railway
└── README.md               # Documentation (this file)
```
