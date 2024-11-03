# ___ Modules ___
def individual_serial(OptionalModule) -> dict:
    return{
        "id": str(OptionalModule["_id"] ), # "_id" is a syntx to return keys
        "name": OptionalModule["name"],
        "mod_id": OptionalModule["mod_id"],
        "classes_id": OptionalModule["classes_id"]
    }

def list_serial(OptionalModules) -> list:
    return[individual_serial(OptionalModule) for OptionalModule in OptionalModules]



# ___ student ___
def individual_stdserial(Student) -> dict:
    return{
        # "_id" is a syntx to return keys
        "id": str(Student["_id"] ), 
        "name": Student["name"],
        "student_id": Student["student_id"],
        "modules": Student["modules"],
        "enrol": Student["enrol"],
        "classes_std": Student["classes_std"]
    }

def list_stdserial(Students) -> list:
    return[individual_stdserial(Student) for Student in Students]
