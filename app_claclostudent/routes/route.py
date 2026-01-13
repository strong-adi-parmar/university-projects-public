from fastapi import APIRouter, File, UploadFile, Query, Response, Form
from typing import List, Optional, Dict
from fastapi import APIRouter, HTTPException, Depends
from model.model import OptionalModule, Student, Exercise, Profile, Material
from config.database import collection_student, collection_opmodule, collection_exercise, collection_student_profile, collection_material, db_m
from schemas.schema import profile_list_serial
from schemas.enroll_schema import  list_serial, list_stdserial
from schemas.exercise_schema import  exercise_list_serial
from bson import ObjectId
from fastapi.responses import FileResponse, HTMLResponse, Response, StreamingResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import gridfs
from passlib.context import CryptContext
import pymongo
import os
import motor.motor_asyncio
import io
import json

router = APIRouter()
teaching_materials = []

# //MockAPI-for-input// GET request method
@router.get("/optionalmodule/")
async def read_optional_modules():
    modules = list_serial(collection_opmodule.find())
    return modules
@router.post("/")
async def create_optional_modules(om: OptionalModule):
    collection_opmodule.insert_one(dict(om))
    return {"om": om}
# ___ Upload materials ___



# STUDENT SIDE
@router.get("/student", tags=["Student basic"])
async def show_all_student():
    student = list_stdserial(collection_student.find())
    # find everything in this function and return it
    return student
@router.post("/student/{id}", tags=["Student basic"])
async def create_student(student: Student):
    collection_student.insert_one(dict(student))
    return {"student": student}



UPLOAD_DIR = "uploads" 
os.makedirs(UPLOAD_DIR, exist_ok=True)
fs = gridfs.GridFS(db_m, collection="material_collection")


