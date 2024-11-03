from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from routes.route import router
from routes.auth import auth
from routes.module_enrollment_class_manager import enroll
from routes.student_grading_feedback_manager import student_grading_feedback_manager
from routes.learning_material_manager import teach_material, learning_material_manager
from routes.student_profile_manager import student_profile_manager
from routes.assessment_upload_submit_manager import assessment_upload_submit_manager
# from prometheus_fastapi_instrumentator import Instrumentator
from config.database import MONGODB_USERNAME, MONGODB_PASSWORD



app = FastAPI()

app.include_router(router)
app.include_router(auth)
app.include_router(enroll)
app.include_router(student_grading_feedback_manager)
app.include_router(teach_material)
app.include_router(student_profile_manager)
app.include_router(assessment_upload_submit_manager)
app.include_router(learning_material_manager)


