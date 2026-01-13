from fastapi import FastAPI, APIRouter, File, UploadFile, Query, Response, Form, HTTPException, Depends, Request
from typing import List, Optional, Dict
from model.model import OptionalModule, Student, Exercise, Profile, Material
from config.database import collection_student, collection_opmodule, collection_exercise, collection_student_profile, collection_material, db_m, db_auth, collection_registration_auth
from schemas.schema import   profile_list_serial
from schemas.enroll_schema import  list_serial, list_stdserial
from bson import ObjectId
from fastapi.responses import FileResponse, HTMLResponse, Response, StreamingResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from pymongo.errors import PyMongoError
from model.model import Registration
from schemas.registration_auth_schema import registration_auth_list_serial
from pymongo import InsertOne
from pydantic import ValidationError



app = FastAPI()
auth = APIRouter()
app.include_router(auth)
SECRET_KEY = '6aaa03e269095e651433976128e717e7601fab1ec7c0ab1fc1058be890ffea0a'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# STUDENT PROFILE AUTH SIGN UP LOGIN
# JWT token helper functions
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = collection_student_profile.find_one({"st_email": email})
    if user is None:
        raise credentials_exception
    return user

# route for creation of JSWT token __ login method __
@auth.post("/login", tags=["ST: Authentication for Student 🔐⌨️ "])
async def login_access(form_data: OAuth2PasswordRequestForm = Depends()):
    registration = collection_registration_auth.find_one({"st_email": form_data.username})
    if not registration or not pwd_context.verify(form_data.password, registration["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": registration["st_email"]}, expires_delta=access_token_expires
    )
    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer"
    }


# Authentication methods __ Sign Up Method __
@auth.post("/signup/", tags=["ST: Authentication for Student 🔐⌨️ "])
async def sign_up_access(registration: Registration):
    if registration.student_id <= 0:
        raise HTTPException(status_code=400, detail="Student ID must be greater than 0")
    try:
        if "@" not in registration.st_email:
            raise ValidationError("Invalid email format")
    except ValidationError:
        raise HTTPException(status_code=400, detail="Invalid email format")
    if not registration.password.strip():
        raise HTTPException(status_code=400, detail="Password cannot be empty")
    hashed_password = pwd_context.hash(registration.password)
    registration_data = {
        "st_email": registration.st_email,
        "student_id": registration.student_id,
        "password": hashed_password
    }
    result = collection_registration_auth.insert_one(registration_data)
    if result.inserted_id:
        return {"message": "User signed up successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to sign up user")


  