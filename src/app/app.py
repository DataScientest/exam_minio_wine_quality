import sys
from pathlib import Path
# Add parent directory to path
parent_folder = str(Path(__file__).parent.parent.parent)
sys.path.append(parent_folder)

import os
import json
from hashlib import sha256
from datetime import datetime, timedelta
from typing import List

from fastapi import FastAPI, Form, HTTPException, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.requests import Request
from pydantic import BaseModel
from cryptography.fernet import Fernet
import jwt
import numpy as np

from src.pipeline_steps.prediction import PredictionPipeline

app = FastAPI()

# Constants
JSON_FILE_PATH = os.path.expanduser("./users/users.json")
SECRET_KEY = "your_jwt_secret_key"  # Use a secure secret key
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# Allowed ranges for variable values
ALLOWED_RANGES = {
    "fixed_acidity": (4.6, 15.9),
    "volatile_acidity": (0.12, 1.58),
    "citric_acid": (0.0, 1.66),
    "residual_sugar": (0.9, 15.5),
    "chlorides": (0.012, 0.611),
    "free_sulfur_dioxide": (1, 72),
    "total_sulfur_dioxide": (6, 289),
    "density": (0.99007, 1.00369),
    "pH": (2.74, 4.01),
    "sulphates": (0.33, 2.0),
    "alcohol": (8.4, 14.9)
}

templates = Jinja2Templates(directory="templates")

class User(BaseModel):
    username: str
    first_name: str
    last_name: str
    password: str

class UserOut(BaseModel):
    username: str
    first_name: str
    last_name: str

class UserInDB(User):
    password: str
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class WineFeatures(BaseModel):
    fixed_acidity: float
    volatile_acidity: float
    citric_acid: float
    residual_sugar: float
    chlorides: float
    free_sulfur_dioxide: float
    total_sulfur_dioxide: float
    density: float
    pH: float
    sulphates: float
    alcohol: float

def verify_password(plain_password, hashed_password):
    return sha256(plain_password.encode()).hexdigest() == hashed_password

def load_users():
    if os.path.exists(JSON_FILE_PATH):
        with open(JSON_FILE_PATH, "r") as file:
            users_data = json.load(file)
        return [UserInDB(**user) for user in users_data]
    return []

def save_user(user: UserInDB):
    users = load_users()
    users.append(user)
    with open(JSON_FILE_PATH, "w") as file:
        json.dump([user.dict() for user in users], file)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"username": payload["sub"]}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")

def validate_wine_features(features: WineFeatures):
    for feature_name, value in features.dict().items():
        min_val, max_val = ALLOWED_RANGES[feature_name]
        if not (min_val <= value <= max_val):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid value for {feature_name}: {value}. Must be between {min_val} and {max_val}."
            )

@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/token", response_class=HTMLResponse)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
    users = load_users()
    for user in users:
        if user.username == username and verify_password(password, user.password):
            token_data = {"sub": username}
            access_token = create_access_token(token_data, expires_delta=timedelta(minutes=30))
            return templates.TemplateResponse("index.html", {"request": {}, "token": access_token})
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

@app.post("/register", response_model=UserOut)
async def register(
    username: str = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    password: str = Form(...)
):
    hashed_password = sha256(password.encode()).hexdigest()
    user_data = {"username": username, "first_name": first_name, "last_name": last_name}
    user_in_db = UserInDB(**user_data, password=hashed_password)
    save_user(user_in_db)
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/predict", response_class=HTMLResponse)
async def predict(
    request: Request,
    fixed_acidity: float = Form(...),
    volatile_acidity: float = Form(...),
    citric_acid: float = Form(...),
    residual_sugar: float = Form(...),
    chlorides: float = Form(...),
    free_sulfur_dioxide: float = Form(...),
    total_sulfur_dioxide: float = Form(...),
    density: float = Form(...),
    pH: float = Form(...),
    sulphates: float = Form(...),
    alcohol: float = Form(...),
    token: str = Depends(oauth2_scheme)
):
    try:
        # Validate the user
        current_user = get_current_user(token)
        # Create a WineFeatures instance with the form data
        features = WineFeatures(
            fixed_acidity=fixed_acidity,
            volatile_acidity=volatile_acidity,
            citric_acid=citric_acid,
            residual_sugar=residual_sugar,
            chlorides=chlorides,
            free_sulfur_dioxide=free_sulfur_dioxide,
            total_sulfur_dioxide=total_sulfur_dioxide,
            density=density,
            pH=pH,
            sulphates=sulphates,
            alcohol=alcohol
        )
        # Validate the features
        validate_wine_features(features)
        # Proceed with the prediction
        data = np.array([
            fixed_acidity, volatile_acidity, citric_acid, residual_sugar, chlorides,
            free_sulfur_dioxide, total_sulfur_dioxide, density, pH, sulphates, alcohol
        ]).reshape(1, 11)
        obj = PredictionPipeline()
        prediction = obj.predict(data)
        return templates.TemplateResponse("results.html", {"request": request, "prediction": str(prediction)})
    except HTTPException as e:
        return templates.TemplateResponse("results.html", {"request": request, "prediction": e.detail})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
