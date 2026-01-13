# __ upload files __
def files_serial(Material) -> dict:
    return{
        "id": str(Material["_id"] ), 
        "student_id": Material["student_id"],
        "material_id": Material["material_id"],
        "filename": Material["filename"]
    }

def files_list_serial(Materials) -> list:
    return[files_serial(Material) for Material in Materials]
