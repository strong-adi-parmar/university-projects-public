# ___ exercise ___
def exercise_serial(Exercise) -> dict:
    return{
        "id": str(Exercise["_id"] ), 
        "ex_info": Exercise["ex_info"],
        "ex_id": Exercise["ex_id"]
    }

def exercise_list_serial(Exercises) -> list:
    return[exercise_serial(Exercise) for Exercise in Exercises]

# __ serial/derial for assigning exercise id with student id __
def exercise_student_serial(ExerciseStudentManager) -> dict:
    return{
        "id": str(ExerciseStudentManager["_id"] ), 
        "student_id": ExerciseStudentManager["student_id"],
        "ex_id": ExerciseStudentManager["ex_id"]
    }
def exercise_student_list_serial(ExerciseStudentManagers) -> list:
    return[exercise_student_serial(ExerciseStudentManager) for ExerciseStudentManager in ExerciseStudentManagers]
  