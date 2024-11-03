from fastapi import APIRouter, File, UploadFile, Query, Response, Form
from typing import List, Optional, Dict
from fastapi import APIRouter, HTTPException, Depends
from model.model import OptionalModule, Student, Exercise, Profile, Material
from config.database import collection_student, collection_opmodule, collection_exercise, collection_student_profile, collection_material, db_m, collection_registration_auth
from fastapi.responses import FileResponse, HTMLResponse, Response, StreamingResponse
import gridfs
import os
import json

student_profile_manager = APIRouter()





# ST:  __~ STUDENT PROFILE ~__

# __ student profile creation __
@student_profile_manager.post("/profile", tags=["ST: Student PROFILE"])
async def student_profile_service_create(profile_data: Profile):
    if not profile_data.student_id or not profile_data.st_email:
        raise HTTPException(status_code=400, detail="student_id and st_email are required fields")
    existing_profile = collection_student_profile.find_one({"student_id": profile_data.student_id})
    if existing_profile:
        raise HTTPException(status_code=400, detail=f"Profile with student_id {profile_data.student_id} already exists")
    registration = collection_registration_auth.find_one({"st_email": profile_data.st_email, "student_id": profile_data.student_id})
    if not registration:
        raise HTTPException(status_code=400, detail="Given email and student ID do not exist in the registration collection")

    try:
        collection_student_profile.insert_one(dict(profile_data))
        save_student_from_profile(profile_data)
        return {"message": "Profile created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create profile: {str(e)}")
# __ student profile update __
@student_profile_manager.put("/profile/", tags=["ST: Student PROFILE"])
async def student_profile_service_update(student_id: int, profile_data: Profile):
    existing_student = collection_student_profile.find_one({"student_id": student_id})
    if existing_student:
        collection_student_profile.update_one({"student_id": student_id}, {"$set": dict(profile_data)})
        save_student_from_profile(profile_data)  # Call save_student_from_profile with profile_data
        return {"message": "Profile updated successfully"}
    else:
        return {"error": "Profile with the provided student_id does not exist, cannot update"}
def save_student_from_profile(profile: Profile) -> None:
    student_data = {
        "name": profile.full_name,
        "student_id": profile.student_id,
        "modules": profile.modules,
        "enrol": profile.enrol,
        "classes_std": profile.classes_std
    }
    
    existing_student = collection_student.find_one({"student_id": profile.student_id})
    if existing_student:
        collection_student.update_one({"student_id": profile.student_id}, {"$set": student_data})
    else:
        collection_student.insert_one(student_data)
# __ for downloading created student Profiles __
@student_profile_manager.get("/profile/download", tags=["ST: Student PROFILE"])
async def student_profile_service_download(student_id: int, response: Response):
    student = collection_student.find_one({"student_id": student_id})

    profile_data = collection_student_profile.find_one({"student_id": student_id})
    
    if not (profile_data or student):
        raise HTTPException(status_code=404, detail="Profile not found")
    elif profile_data is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    profile_data['_id'] = str(profile_data['_id'])
    profile_json = json.dumps(profile_data)
    # set response headers for downloading
    response.headers["Content-Disposition"] = f"attachment; filename=profile_{student_id}.json"
    response.headers["Content-Type"] = "application/json"

    return profile_json
@student_profile_manager.get("/profile/print", tags=["ST: Student PROFILE"])
async def student_profile_service_print(student_id: int, response: Response):
    student = collection_student.find_one({"student_id": student_id})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    profile_data = collection_student_profile.find_one({"student_id": student_id})
    if not profile_data:
        raise HTTPException(status_code=404, detail="Profile not found")
    profile_data['_id'] = str(profile_data['_id'])
    profile_json = json.dumps(profile_data, indent=4)  
    response.headers["Content-Type"] = "text/plain" 

    return profile_json

