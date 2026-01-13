# used for serialising/deserialising

# ___ profile ___
def profile_serial(Profile) -> dict:
    return{
        "id": str(Profile["_id"] ), 
        "full_name": Profile["full_name"],
        "student_id": Profile["student_id"],
        "modules": Profile["modules"],
        "enrol": Profile["enrol"],
        "classes_std": Profile["classes_std"],
        "st_email": Profile["st_email"],
        "st_address": Profile["st_address"],
        "st_phone": Profile["st_phone"],
        "course": Profile["course"],
        "course_id": Profile["course_id"],
        "marks": Profile["marks"]
    }

def profile_list_serial(Profiles) -> list:
    return[profile_serial(Profile) for Profile in Profiles]



