from pymongo import MongoClient
client = MongoClient("mongodb+srv://19276544:onenine276544@cluster0.dpwcyqy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
# mongodb+srv://19276544:onenine276544@cluster0.dpwcyqy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0


import os

MONGODB_USERNAME = os.environ.get("19276544")
MONGODB_PASSWORD = os.environ.get("onenine276544")


db_s = client.student_db
db_t = client.optionalmodule_db 
db_ex = client.exercise_db 
db_p = client.student_profile_database
db_m = client.material_db
db_auth = client.registration_auth_db


collection_student = db_s["student_collection"]
collection_opmodule = db_t["optionalmodule_collection"]

collection_exercise = db_ex["exercise_collection"]
collection_exercise_marks = db_ex["exercise_marks_collection"]
collection_exercise_student_manager = db_ex["exercise_student_manager_collection"]

collection_student_profile = db_p["student_profile_collection"]
collection_material = db_m["material_collection"]
collection_registration_auth = db_auth["registration_auth_collection"]

