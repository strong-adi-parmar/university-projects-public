def registration_auth_serial(Registration) -> dict:
    return{
        "id": str(Registration["_id"] ), 
        "student_id": Registration["student_id"],
        "st_email": Registration["st_email"],
        "password": Registration["password"]
    }

def registration_auth_list_serial(Registrations) -> list:
    return[registration_auth_serial(Registration) for Registration in Registrations]
