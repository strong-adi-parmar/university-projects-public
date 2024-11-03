from fastapi import APIRouter, File, UploadFile, Query, Response, Form, HTTPException, Depends
from typing import List, Optional, Dict
from config.database import collection_student, collection_opmodule, collection_exercise, collection_student_profile, collection_material, db_m
# from schemas.schema import list_serial, list_stdserial, exercise_list_serial, profile_list_serial
from schemas.enroll_schema import list_serial, list_stdserial
from fastapi.responses import FileResponse, HTMLResponse, Response, StreamingResponse
import pymongo

enroll = APIRouter()


# ST: __enroll modules__
@enroll.post("/student/{student_id}/enroll-modules/", tags=["ST: Enroll/Exit of Optional Module✅⛔"])
async def module_enrollment_service(student_id: int, mod_ids: list[int]):
    student = collection_student.find_one({"student_id": student_id})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    for mod_id in mod_ids:
        if not collection_opmodule.find_one({"mod_id": mod_id}):
            raise HTTPException(status_code=404, detail=f"Module with ID {mod_id} not found")
    enrolled_modules = set(student.get("enrol", []))
    enrolled_modules.update(mod_ids)

    result = collection_student.update_one({"student_id": student_id}, {"$set": {"enrol": list(enrolled_modules)}})

    if result.modified_count == 1:
        enrolled_student = collection_student.find_one({"student_id": student_id})
        enrolled_student["_id"] = str(enrolled_student["_id"])
        return {"message": "Modules enrolled successfully", "enrolled_student": enrolled_student}
    else:
        raise HTTPException(status_code=500, detail="Failed to enroll modules")
# ST: __ exit from enrolled modules __
@enroll.post("/student/{student_id}/exit-module/", tags=["ST: Enroll/Exit of Optional Module✅⛔"])
async def module_enrollment_service_exit(student_id: int, module_id: int):
    student = collection_student.find_one({"student_id": student_id})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    if not collection_opmodule.find_one({"mod_id": module_id}):
        raise HTTPException(status_code=404, detail=f"Module with ID {module_id} not found")
    enrolled_modules = set(student.get("enrol", []))
    if module_id in enrolled_modules:
        enrolled_modules.remove(module_id)
    else:
        raise HTTPException(status_code=404, detail=f"Student with ID {student_id} is not enrolled in module with ID {module_id}")
    result = collection_student.update_one({"student_id": student_id}, {"$set": {"enrol": list(enrolled_modules)}})
    print("JESUSB CODE WORKS TILL NOW", result)

    if result.modified_count == 1:
        enrolled_student = collection_student.find_one({"student_id": student_id})
        enrolled_student["_id"] = str(enrolled_student["_id"])
        return {"message": "Student enrollment removed successfully", "enrolled_student": enrolled_student}
    else:
        raise HTTPException(status_code=500, detail="Failed to remove student enrollment from module")

# ST: __selecting a class from an enrolled module__
@enroll.post("/student/{student_id}/select-class/", tags=["ST: Enroll/Exit of Optional Module✅⛔"])
async def class_selection_service(student_id: int, class_id: int):
    student = collection_student.find_one({"student_id": student_id})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    if not collection_opmodule.find_one({"classes_id": class_id}):
        raise HTTPException(status_code=404, detail=f"Class with ID {class_id} not found")

    selected_classes = set(student.get("classes_std", []))
    selected_classes.add(class_id)
    result = collection_student.update_one({"student_id": student_id}, {"$set": {"classes_std": list(selected_classes)}})

    if result.modified_count == 1:
        enrolled_student = collection_student.find_one({"student_id": student_id})
        enrolled_student["_id"] = str(enrolled_student["_id"])
        return {"message": "Student selected class(es) successfully", "enrolled_student": enrolled_student}
    else:
        raise HTTPException(status_code=500, detail="Failed to select class for student")

