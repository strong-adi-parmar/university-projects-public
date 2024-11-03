from fastapi import APIRouter, File, UploadFile, Query, Response, Form, HTTPException
from typing import List, Optional, Dict
from model.model import Material
from config.database import collection_material, db_m
from schemas.enroll_schema import  list_serial, list_stdserial
from schemas.files_schema import  files_list_serial
from fastapi.responses import FileResponse, HTMLResponse, Response, StreamingResponse
import gridfs
from pymongo import MongoClient, ReturnDocument

# ~~~~ learning_material_manager
learning_material_manager = APIRouter()
@learning_material_manager.get("/list_files", tags=["ST: Learning Material Service"])
async def learning_material_service_listfiles():
    filenames = []
    cursor = fs.find()
    for file in cursor:
        filename = file.filename
        filenames.append(filename)
    if filenames:
        return {"filenames": filenames}
    else:
        raise HTTPException(status_code=404, detail="No filenames found")

class MaterialInstance:
    def __init__(self):
        self.dictnames: Dict[int, List[str]] = {}

material_instance = MaterialInstance()

teach_material = APIRouter()
# //MockAPI-for-input// __ uploading teaching materials __
@teach_material.post("/store_filenames/{student_id}")
async def store_filenames(student_id: int, filename: str):
    if student_id not in material_instance.dictnames:
        material_instance.dictnames[student_id] = []
    material_instance.dictnames[student_id].append(filename)
    return {"message": f"Filename '{filename}' stored for student ID {student_id}"}

fs = gridfs.GridFS(db_m)
@teach_material.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    # saving the file into MongoDB
    fs.put(contents, filename=file.filename)
    return {"filename": file.filename}

# __ downloading teaching material 
@learning_material_manager.get("/downloadfile/{filename}", tags=["ST: Learning Material Service"])
async def learning_material_service_downloadfile(filename: str):
    file_data = fs.find_one({"filename": filename})
    if file_data is None:
        raise HTTPException(status_code=404, detail="File not found")
    file_content = file_data.read()
    response = Response(content=file_content, media_type='application/octet-stream')
    response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'

    return response




