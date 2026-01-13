from pydantic import BaseModel, validator
from typing import List, Optional, Dict
from fastapi import File, UploadFile
from config.database import collection_student_profile

#  for INPUT data of APIs
class OptionalModule(BaseModel):
    name: str
    mod_id: int
    classes_id: list[int]
class Exercise(BaseModel):
    ex_info: str
    ex_id: int
class Material(BaseModel):
    material_id: str 
    student_id: int 
    filename: list[str]
class ExerciseMarkFeedback(BaseModel):
    mod_id: int
    student_id: int
    ex_id: list[int]
    ex_feedback: str
    ex_marks: int
class ExerciseStudentManager(BaseModel):
    student_id: int 
    ex_id: list[int]
# OUTPUT
class Student(BaseModel):
    name: str
    student_id: int
    modules: Optional[list[str]] = None
    enrol: Optional[list[int]] = None 
    classes_std: Optional[list[int]] = None
class Profile(BaseModel):
    full_name: str
    student_id: int
    modules: Optional[List[str]] = None
    enrol: Optional[List[int]] = None
    classes_std: Optional[List[int]] = None
    st_email: str
    st_phone: Optional[str] = None
    st_address: Optional[str] = None
    course: Optional[str] = None
    course_id: int
    marks: str

    @validator("student_id")
    def validate_student_id(cls, v, values):
        if "student_id" not in values:
            return v

        existing_student_id = values.get("student_id")
        if collection_student_profile.find_one({"student_id": existing_student_id}):
            raise ValueError("Student ID already exists")

        return v

    @validator("st_email")
    def validate_email(cls, v):
        if "@" not in v:
            raise ValueError("Invalid email format")
        return v

    class Config:
        validate_assignment = True  
class Registration(BaseModel):
    st_email: str
    student_id: int
    password: str
     