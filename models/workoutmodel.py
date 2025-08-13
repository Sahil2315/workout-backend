from pydantic import BaseModel

class Exercise(BaseModel):
    exName: str
    exDesc: str
    exSets: int
    exReps: int
    exWeight: str

class ExercisePerDay(BaseModel):
    weekDay: str
    workout: list[Exercise]

class Workout(BaseModel):
    plan: list[ExercisePerDay]
    date: str
    