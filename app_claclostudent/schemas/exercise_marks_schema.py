def individual_serial_marks(ExerciseMarkFeedback) -> dict:
    return{
        "id": str(ExerciseMarkFeedback["_id"] ), 
        "mod_id": ExerciseMarkFeedback["mod_id"],
        "student_id": ExerciseMarkFeedback["student_id"],
        "ex_id": ExerciseMarkFeedback["ex_id"],
        "ex_feedback": ExerciseMarkFeedback["ex_feedback"],
        "ex_marks": ExerciseMarkFeedback["ex_marks"],
    }

def list_serial_marks(ExerciseMarkFeedbacks) -> list:
    return [individual_serial_marks(ExerciseMarkFeedback) for ExerciseMarkFeedback in ExerciseMarkFeedbacks]
