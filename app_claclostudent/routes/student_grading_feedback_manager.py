from config.database import collection_student, collection_exercise, collection_exercise_marks, collection_student_profile, db_ex
from model.model import Exercise, ExerciseMarkFeedback, Student
from schemas.exercise_schema import exercise_list_serial
from schemas.exercise_marks_schema import list_serial_marks
from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from typing import List
from fastapi.responses import FileResponse, HTMLResponse, Response, StreamingResponse
import gridfs

# ~~~~ student_grading_feedback_manager
student_grading_feedback_manager = APIRouter()



# __ marks & feedback __
# ___ ST: for student ___
@student_grading_feedback_manager.get("/exercise/marks/", tags=["ST: Student Exercise"])
async def student_grading_feedback_service(student_id: int):
    exercise_marks_info = list_serial_marks(collection_exercise_marks.find({"student_id": student_id}))
    if exercise_marks_info:
        return exercise_marks_info
    else:
        return {"Student with given ID does not exists or marks are not assigned"}

# //MockAPI-for-input// CREATING MARKS AND FEEDBACK FROM TEACHER SIDE
@student_grading_feedback_manager.post("/exercise/{ex_id}",tags=["ExerciseMarksFeedback'CREATOR'"])
async def create_exercise_markNfeedback(student_id: int, data: ExerciseMarkFeedback):
    student = collection_student.find_one({"student_id": student_id})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    collection_exercise_marks.insert_one(data.dict())
    
    return {"message": "Marks and feedback of the exercise for the given student and module created!"}
@student_grading_feedback_manager.get("/exercise/{ex_id}",tags=["ExerciseMarksFeedback'CREATOR'"])
async def get_exercise_marksNfeedback():
    exercise_marks_info = list_serial_marks(collection_exercise_marks.find())
    return exercise_marks_info
