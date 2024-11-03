# ~~~~ assessment_upload_submit_manager.py
from config.database import collection_student, collection_exercise, collection_exercise_marks, collection_student_profile, db_ex, collection_exercise_student_manager
from model.model import Exercise, ExerciseMarkFeedback, Student
from schemas.exercise_schema import exercise_list_serial
from schemas.exercise_marks_schema import list_serial_marks
from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from typing import List
from fastapi.responses import FileResponse, HTMLResponse, Response, StreamingResponse
import gridfs

# exercise = APIRouter()
assessment_upload_submit_manager = APIRouter()
# //MockAPI-for-input// __ exercise info create __
@assessment_upload_submit_manager.post("/exercise", tags=["Student Exercise"])
async def create_exercise(exi: Exercise):
    collection_exercise.insert_one(dict(exi))
    return {"exercise creator": exi}

# __ ST: get exercise info
@assessment_upload_submit_manager.get("/exercise", tags=["ST: Student Exercise 📜"])
async def exercise_assessment_service_info():
    exercise_info = exercise_list_serial(collection_exercise.find())
    return exercise_info


# //MockAPI-for-input// Function for assigning an exercise to a student and storing their IDs
@assessment_upload_submit_manager.post("/exercise/assign/", tags=["Assign Exercise"])
async def assign_exercise_to_student(student_id: int, ex_id: int):
    student = collection_student.find_one({"student_id": student_id})
    exercise = collection_exercise.find_one({"ex_id": ex_id})
    if not student or not exercise:
        return {"detail": "Student or Exercise not found"}, 404

    assignment_data = {"student_id": student_id, "ex_id": ex_id}
    result = collection_exercise_student_manager.insert_one(assignment_data)
    if result.inserted_id:
        return {"message": "Exercise assigned to student successfully"}
    else:
        return {"detail": "Failed to assign exercise to student"}, 500

#__ ST: UPLOADING FILES FOR EXERCISES __
fs = gridfs.GridFS(db_ex)

@assessment_upload_submit_manager.post("/exercise/assign/upload/", tags=["ST: Student Exercise 📜"])
async def exercise_assessment_service_upload(student_id: int, ex_id: int, files: List[UploadFile] = File(...)):
    assignment = collection_exercise_student_manager.find_one({"student_id": student_id, "ex_id": ex_id})
    if assignment is None:
        return {"detail": "Exercise assignment not found for the student"}, 404

    # uploading files to database using GridFS
    file_ids = []
    for file in files:
        file_data = await file.read()
        file_id = fs.put(file_data, filename=file.filename, student_id=student_id, ex_id=ex_id)
        file_ids.append(str(file_id))

    return {"student_id": student_id, "ex_id": ex_id, "file_ids": file_ids}
